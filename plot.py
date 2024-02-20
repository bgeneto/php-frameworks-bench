"""Take log files from the results directory and create bar charts using Plotly.

Author: Bernhard Enders
Date: 2024-02-17
Modified by: bgeneto
Date: 2024-02-19
"""

import json
import os
import re

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class LogParser:
    def __init__(self, filename):
        self.filename = filename

    def parse_logfile(self):
        """
        Parses a log file and retrieves the requests per second value.
        """
        with open(self.filename, "r") as f:
            c = 0
            for line in f:
                c += 1
                # check if is the first line of the log file
                if c == 1:
                    command_args = line.strip()
                if "finished in" in line:
                    # Extract requests per second value
                    req_per_sec = float(line.split(", ")[1].split("req/s")[0])
                    return req_per_sec, command_args
        raise ValueError(f"Could not find relevant data in log file: {self.filename}")


class FilenameExtractor:
    def __init__(self, filename):
        self.filename = filename

    def extract_info_from_filename(self):
        # Split the filename by '.'
        parts = self.filename.split(".")

        # The framework name is the first part
        framework_name = parts[0].split("/")[-1].capitalize()

        # The benchmark name is the second part
        benchmark_name = parts[2].capitalize()

        return framework_name, benchmark_name


class FileCounter:
    def __init__(self, directory, skip_dirs=None):
        self.directory = directory
        self.skip_dirs = skip_dirs

    def count_files(self):
        """
        Counts the number of all files in a directory recursively.
        Returns a dictionary with the root folder name (first level) as the key and the count as the value.
        """
        if self.skip_dirs is None:
            self.skip_dirs = []

        count_dict = {}
        for root, dirs, files in os.walk(self.directory):
            # Skip directories in skip_dirs list
            dirs[:] = [d for d in dirs if d not in self.skip_dirs]

            if root == self.directory:
                for dir in dirs:
                    count_dict[dir] = 0
            else:
                first_level_dir = root.split(self.directory)[-1].split(os.sep)[1]
                count_dict[first_level_dir] += len(files)
        return count_dict


class PercentageCalculator:
    def __init__(self, values):
        self.values = values

    def calculate_percentages(self):
        max_value = max(self.values)
        percentages = [(value / max_value) * 100 for value in self.values]
        return percentages


class FilePlotter:
    def __init__(self, total_files):
        self.total_files = total_files

    def plot_total_number_of_files(self):
        """
        Plots the total number of files in each directory.
        Order by the number of files in descending order.
        """
        total_files = dict(
            sorted(self.total_files.items(), key=lambda item: item[1], reverse=True)
        )

        if len(total_files) == 0:
            print("No framework files found.")
            return

        # Calculate the percentages
        max_value = max(total_files.values())
        percentages = [
            f"{value} | {(value / max_value) * 100:.1f}%"
            for value in total_files.values()
        ]

        fig = go.Figure()

        for x_value, y_value, percentage in zip(
            list(total_files.keys()), list(total_files.values()), percentages
        ):
            fig.add_trace(
                go.Bar(
                    x=[x_value],
                    y=[y_value],
                    text=[percentage],
                    textposition="auto",
                    name=x_value,  # Set the legend text to the x-value
                )
            )

        fig.update_layout(
            title_text="framework size comparison (excluding folders: cache, logs, storage, var, writable...)",
            title_font=dict(size=20),
            xaxis_title="Framework",
            yaxis_title="Total Number of Files",
        )

        # Export to a single HTML file
        export_file = output_dir + "framework-size-chart.html"
        fig.write_html(export_file)
        print(f"Framework size bar charts exported to {export_file}")


class H2LoadPlotter:
    def __init__(self, results_dir):
        self.results_dir = results_dir

    def plot_h2load(self):
        """
        Creates a bar chart of requests per second for all log files in the specified directory.
        """
        filenames = [
            os.path.join(self.results_dir, f)
            for f in os.listdir(self.results_dir)
            if f.endswith(".h2load.log")
        ]

        frameworks = []
        benchmark_names = []
        for filename in filenames:
            extractor = FilenameExtractor(filename)
            framework_name, benchmark_name = extractor.extract_info_from_filename()
            frameworks.append(framework_name)
            benchmark_names.append(benchmark_name)

        req_per_sec_values = []
        for i, filename in enumerate(filenames):
            try:
                parser = LogParser(filename)
                rps, command_args = parser.parse_logfile()
            except ValueError as e:
                print(f"Error: {e}")
                continue
            req_per_sec_values.append(rps)

        # Initialize dictionaries to hold requests per second values and labels for each benchmark type
        req_per_sec_by_bench = {bench: [] for bench in benchmark_names}
        labels_by_bench = {bench: [] for bench in benchmark_names}

        # Populate the dictionaries
        for i, bench_type in enumerate(benchmark_names):
            label = frameworks[i]
            req_per_sec = req_per_sec_values[i]
            if bench_type in req_per_sec_by_bench:
                req_per_sec_by_bench[bench_type].append(req_per_sec)
                labels_by_bench[bench_type].append(label)

        # Sort the data by requests per second in descending order
        for bench_type in benchmark_names:
            if bench_type in req_per_sec_by_bench:
                sorted_pairs = sorted(
                    zip(req_per_sec_by_bench[bench_type], labels_by_bench[bench_type]),
                    reverse=True,
                )
                req_per_sec_by_bench[bench_type], labels_by_bench[bench_type] = (
                    zip(*sorted_pairs) if sorted_pairs else ([], [])
                )

        # Remove duplicates from the benchmark names list
        benchmark_names = list(set(benchmark_names))

        # Create subplots dynamically based on the number of benchmarks
        cols = len(benchmark_names)
        if cols == 0:
            print("No h2load log files found.")
            return
        fig = make_subplots(
            rows=1,
            cols=cols,
            subplot_titles=[f"Benchmark: {bench}" for bench in benchmark_names],
        )

        # Add traces for each benchmark
        for i, benchmark_type in enumerate(benchmark_names, start=1):
            if (
                benchmark_type in req_per_sec_by_bench
                and req_per_sec_by_bench[benchmark_type]
            ):
                percentages = PercentageCalculator(
                    req_per_sec_by_bench[benchmark_type]
                ).calculate_percentages()
                text_values = [
                    f"{y_value} | {percentage:.1f}%"
                    for y_value, percentage in zip(
                        req_per_sec_by_bench[benchmark_type], percentages
                    )
                ]

                for label, y_value, text_value in zip(
                    labels_by_bench[benchmark_type],
                    req_per_sec_by_bench[benchmark_type],
                    text_values,
                ):
                    fig.add_trace(
                        go.Bar(
                            x=[label],
                            y=[y_value],
                            name=label,  # Set the legend text to the label
                            text=[text_value],
                            textposition="auto",
                        ),
                        row=1,
                        col=i,
                    )

        # Update layout to adjust titles and axis labels
        fig.update_layout(
            title_text=f"h2load requests per second charts<br>(h2load {command_args})",
            title_font=dict(size=20),
            xaxis_title="Framework",
            yaxis_title="Requests per Second (RPS)",
        )

        # Export to a single HTML file
        export_file = work_dir + "h2load-charts.html"
        fig.write_html(export_file)
        print(f"h2load bar charts exported to {export_file}")


class Wrk2Plotter:
    def __init__(self, results_dir):
        self.results_dir = results_dir

    def plot_wrk2(self):
        # Prepare an empty DataFrame to store all latency data
        latency_data = pd.DataFrame()
        command_args = ""

        # Loop through each file in the logs directory
        for filename in os.listdir(self.results_dir):
            if filename.endswith(".wrk2.log"):
                extractor = FilenameExtractor(filename)
                framework_name, benchmark_name = extractor.extract_info_from_filename()
                # Construct the full file path
                file_path = os.path.join(self.results_dir, filename)

                # Initialize lists to store the extracted data
                percentiles = []
                latencies = []

                # Open and read the file
                with open(file_path, "r") as f:
                    lines = f.readlines()
                    c = 0
                    for line in lines:
                        c += 1
                        if c == 1:
                            command_args = line.strip()
                        if line.strip() and "Value" not in line and "inf" not in line:
                            # Extract latency and percentile values
                            parts = line.split()
                            if len(parts) >= 2:
                                try:
                                    latency = float(parts[0])
                                    percentile = float(parts[1])
                                    percentiles.append(percentile)
                                    latencies.append(latency)
                                except ValueError:
                                    # Handle the case where conversion to float fails
                                    continue

                # Create a DataFrame from the extracted data
                df = pd.DataFrame(
                    {
                        "Percentile": percentiles,
                        "Latency": latencies,
                        "File": filename.replace(
                            ".latency.log", ""
                        ),  # Use file name as identifier
                    }
                )

                # Remove the last 20 percentiles to avoid skewing the chart
                df = df[df["Percentile"] <= 0.992]

                # Append the data to the main DataFrame
                latency_data = pd.concat([latency_data, df], ignore_index=True)

        if len(latency_data) == 0:
            print("No wrk2 log files found.")
            return

        # Add two new columns to the DataFrame for bench_name and framework_name
        latency_data["BenchName"] = latency_data["File"].apply(
            lambda x: x.split(".")[2].capitalize()
        )
        latency_data["FrameworkName"] = latency_data["File"].apply(
            lambda x: x.split(".")[0]
        )

        # Group the DataFrame by bench_name
        grouped = latency_data.groupby("BenchName")

        # Loop through each group and create a plot
        for benchmark_name, group in grouped:
            fig = px.line(
                group,
                x="Percentile",
                y="Latency",
                color="FrameworkName",  # Use framework_name as legend
                markers=True,
                labels={"Latency": "Latency (ms)", "Percentile": "Percentile"},
                title=f"wrk2 latency by percentile | Benchmark: {benchmark_name}<br>(wrk2 {command_args})",
            )

            fig.update_layout(title={"font": dict(size=20)})

            # Export the plot to a separate HTML file for each bench_name
            export_file = work_dir + f"wrk2-{benchmark_name}-charts.html"
            fig.write_html(export_file)
            print(f"wrk2 charts for {benchmark_name} exported to {export_file}")


class WrkPlotter:
    def __init__(self, results_dir):
        self.results_dir = results_dir

    def convert_to_number(self, value):
        if "k" in value:
            return float(value.replace("k", "")) * 1000
        else:
            return float(value)

    def plot_wrk(self):
        # Regular expression patterns to extract data
        latency_pattern = re.compile(r"Latency\s+(\d+\.\d+m?s)")
        req_sec_pattern = re.compile(r"Req/Sec\s+(\d+\.\d+k?)?")

        # Data structure to hold the parsed results
        results = {}

        # Iterate over each file in the results directory
        for filename in os.listdir(self.results_dir):
            if filename.endswith(".wrk.log"):
                extractor = FilenameExtractor(filename)
                framework_name, benchmark_name = extractor.extract_info_from_filename()
                with open(
                    os.path.join(self.results_dir, filename), "r", encoding="utf-8"
                ) as file:
                    content = file.read()
                    # The first line of the file contains the wrk command used
                    command_args = content.split("\n")[0]
                    # Extract the average latency and requests per second
                    avg_latency = latency_pattern.search(content).group(1)
                    avg_req_sec = req_sec_pattern.search(content).group(1)
                    # Convert avg_req_sec to requests/sec if the value ends with 'k'
                    if "k" in str(avg_req_sec):
                        avg_req_sec = float(avg_req_sec.replace("k", "")) * 1000
                    else:
                        avg_req_sec = float(avg_req_sec)
                    if "ms" in str(avg_latency):
                        avg_latency = float(avg_latency.replace("ms", ""))
                    else:
                        avg_latency = float(avg_latency.replace("s", "")) * 1000
                    if benchmark_name not in results:
                        results[benchmark_name] = {
                            "frameworks": [],
                            "latencies": [],
                            "req_secs": [],
                        }
                    results[benchmark_name]["frameworks"].append(framework_name)
                    results[benchmark_name]["latencies"].append(avg_latency)
                    results[benchmark_name]["req_secs"].append(avg_req_sec)

        if len(results) == 0:
            print("No wrk log files found.")
            return

        # Create subplots
        fig = make_subplots(
            rows=2,
            cols=len(results),
            subplot_titles=[
                f"Benchmark: {bench_name}" for bench_name in results.keys()
            ],
        )

        # order latencies in ascending and req_secs descending order
        for benchmark_name, data in results.items():
            # Convert strings to numerical values
            # data["latencies"] = [convert_to_number(value) for value in data["latencies"]]
            # data["req_secs"] = [convert_to_number(value) for value in data["req_secs"]]

            # Sort the data by latency in ascending order
            (
                data["frameworks"],
                data["latencies"],
                data["req_secs"],
            ) = zip(
                *sorted(
                    zip(
                        data["frameworks"],
                        data["latencies"],
                        data["req_secs"],
                    ),
                    key=lambda x: x[1],
                )
            )

        col = 1
        for benchmark_name, data in results.items():
            # Add the latency bar chart
            for framework, latency in zip(data["frameworks"], data["latencies"]):
                fig.add_trace(
                    go.Bar(
                        x=[framework],
                        y=[latency],
                        name=framework,
                        text=f"{latency:.0f}",
                    ),
                    row=1,
                    col=col,
                )

            # Add the requests per second bar chart
            for framework, req_sec in zip(data["frameworks"], data["req_secs"]):
                fig.add_trace(
                    go.Bar(
                        x=[framework],
                        y=[req_sec],
                        name=framework,
                        text=f"{req_sec:.0f}",
                    ),
                    row=2,
                    col=col,
                )

            # Add x and y axis titles
            fig.update_xaxes(title_text="Framework", row=1, col=col)
            fig.update_yaxes(
                title_text="Avg Latency (ms), lower is better", row=1, col=col
            )
            fig.update_xaxes(title_text="Framework", row=2, col=col)
            fig.update_yaxes(title_text="Avg Req/Sec", row=2, col=col)
            col += 1

        # Update layout
        fig.update_layout(
            height=400 * len(results),
            title_text=f"Benchmark Results<br>(wrk {command_args}) ",
            barmode="group",
        )

        # Export to HTML
        export_file = work_dir + f"wrk-charts.html"
        fig.write_html(export_file)
        print(f"wrk charts exported to {export_file}")


class K6DataExtractor:
    def __init__(self, framework_name, benchmark_name):
        self.framework_name = framework_name
        self.benchmark_name = benchmark_name

    def extract_k6_data(self):
        """Extracts avg and rate data from a log file"""

        # convert framework_name and benchmark_name to lowercase
        framework_name = self.framework_name.lower()
        benchmark_name = self.benchmark_name.lower()

        file_path = os.path.join(
            work_dir, f"{framework_name}.bench.{benchmark_name}.k6.log"
        )

        with open(file_path, "r") as f:
            log_data = json.load(f)

        try:
            avg_duration = log_data["metrics"][
                "http_req_duration{expected_response:true}"
            ]["avg"]
            req_rate = log_data["metrics"]["http_reqs"]["rate"]
            checks_perc_value = log_data["metrics"]["checks"]["value"]
            vus_max = log_data["metrics"]["vus_max"]["value"]
        except KeyError:
            print(f"Error: Could not find relevant data in log file: {file_path}")
            return None, None

        return avg_duration, req_rate, checks_perc_value, vus_max


class K6DataGatherer:
    def __init__(self, results_dir):
        self.results_dir = results_dir

    def gather_k6_data(self):
        """Gathers data from all log files"""
        data = {}
        for filename in os.listdir(self.results_dir):
            if filename.endswith(".k6.log"):
                extractor = FilenameExtractor(filename)
                framework_name, benchmark_name = extractor.extract_info_from_filename()
                if benchmark_name not in data:
                    data[benchmark_name] = {
                        "frameworks": [],
                        "avg_durations": [],
                        "req_rates": [],
                        "checks_perc_value": [],
                        "vus_max": [],
                    }

                avg_duration, req_rate, checks_perc_value, vus_max = K6DataExtractor(
                    framework_name, benchmark_name
                ).extract_k6_data()
                if avg_duration is None or req_rate is None:
                    continue
                data[benchmark_name]["frameworks"].append(framework_name)
                data[benchmark_name]["avg_durations"].append(avg_duration)
                data[benchmark_name]["req_rates"].append(req_rate)
                data[benchmark_name]["checks_perc_value"].append(checks_perc_value)
                data[benchmark_name]["vus_max"].append(vus_max)

        return data


class K6Plotter:
    def __init__(self, results_dir):
        self.results_dir = results_dir

    def plot_k6(self):
        """Creates bar charts using Plotly"""
        data = K6DataGatherer(self.results_dir).gather_k6_data()
        if data is None:
            print("No k6 log files found.")
            return
        metrics = ["Avg Duration (ms)", "Req Rate (req/s)"]
        num_test_names = len(data)
        if num_test_names == 0:
            print("No k6 log files found.")
            return

        fig = make_subplots(
            rows=2,
            cols=num_test_names,
            subplot_titles=list(f"Benchmark: {x}" for x in data.keys()),
        )

        for i, test_name in enumerate(data):
            test_data = data[test_name]

            for j, metric in enumerate(metrics):
                y_data = (
                    sorted(
                        zip(
                            test_data["avg_durations"],
                            test_data["frameworks"],
                            test_data["checks_perc_value"],
                        )
                    )
                    if metric == "Avg Duration (ms)"
                    else sorted(
                        zip(
                            test_data["req_rates"],
                            test_data["frameworks"],
                            test_data["checks_perc_value"],
                        ),
                        reverse=True,
                    )
                )

                for value, framework, perc_value in y_data:
                    fig.add_trace(
                        go.Bar(
                            x=[framework],
                            y=[value],
                            name=framework,
                            text=f"{value:.1f} | OK: {100*perc_value:.1f}%",
                            textposition="auto",
                        ),
                        row=j + 1,
                        col=i + 1,
                    )

            # Add y-axis titles
            fig.update_yaxes(
                title_text="Avg. Duration / Latency (ms)", row=1, col=i + 1
            )
            fig.update_yaxes(title_text="Req. Rates (req/s)", row=2, col=i + 1)

        # Customize layout (optional)
        fig.update_layout(
            height=1080,
            title_text="k6 benchmark results (ramping-vus max. = "
            + str(data[test_name]["vus_max"][0])
            + ")",  # supposing that all tests have the same vus
        )

        # Export to a single HTML file
        export_file = work_dir + "k6-charts.html"
        fig.write_html(export_file)
        print(f"k6 bar charts exported to {export_file}")


if __name__ == "__main__":
    # Dockerfile.python work directory
    work_dir = "/usr/src/app"

    # Directory containing the log files
    output_dir = work_dir + "/results/"

    # Check if the output directory exists
    if not os.path.exists(output_dir):
        print(f"Error: Output directory {output_dir} not found.")
        exit(1)

    # Exclude the following directories from the count
    counter = FileCounter("/www/html", ["storage", "var", "logs", "cache", "writable"])
    total_files = counter.count_files()

    plotter = FilePlotter(total_files)
    plotter.plot_total_number_of_files()

    h2load_plotter = H2LoadPlotter(output_dir)
    h2load_plotter.plot_h2load()

    wrk_plotter = WrkPlotter(output_dir)
    wrk_plotter.plot_wrk()

    wrk2_plotter = Wrk2Plotter(output_dir)
    wrk2_plotter.plot_wrk2()

    k6_plotter = K6Plotter(output_dir)
    k6_plotter.plot_k6()
