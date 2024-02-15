import os
import re
import warnings

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=DeprecationWarning)


def parse_logfile(filename):
    """
    Parses a log file and retrieves the requests per second value.
    """
    with open(filename, "r") as f:
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
    raise ValueError("Could not find relevant data in log file")


def extract_info_from_filename(filename):
    # Split the filename by '.'
    parts = filename.split(".")

    # The framework name is the first part
    framework_name = parts[0].split("/")[-1].capitalize()

    # The benchmark name is the second part
    benchmark_name = parts[2].capitalize()

    return framework_name, benchmark_name


def count_files(directory, skip_dirs=None):
    """
    Counts the number of all files in a directory recursively.
    Returns a dictionary with the root folder name (first level) as the key and the count as the value.
    """
    if skip_dirs is None:
        skip_dirs = []

    count_dict = {}
    for root, dirs, files in os.walk(directory):
        # Skip directories in skip_dirs list
        dirs[:] = [d for d in dirs if d not in skip_dirs]

        if root == directory:
            for dir in dirs:
                count_dict[dir] = 0
        else:
            first_level_dir = root.split(directory)[-1].split(os.sep)[1]
            count_dict[first_level_dir] += len(files)
    return count_dict


# Function to calculate percentages
def calculate_percentages(values):
    max_value = max(values)
    percentages = [(value / max_value) * 100 for value in values]
    return percentages


def plot_total_number_of_files(total_files):
    """
    Plots the total number of files in each directory.
    Order by the number of files in descending order.
    """
    total_files = dict(
        sorted(total_files.items(), key=lambda item: item[1], reverse=True)
    )

    # Calculate the percentages
    max_value = max(total_files.values())
    percentages = [
        f"{value} ({(value / max_value) * 100:.2f}%)" for value in total_files.values()
    ]

    fig = go.Figure(
        data=[
            go.Bar(
                x=list(total_files.keys()),
                y=list(total_files.values()),
                text=percentages,
                textposition="auto",
            )
        ]
    )

    fig.update_layout(
        title_text="Framework size comparison<br>(excluding cache, logs, storage, var, writable...)",
        xaxis_title="Framework",
        yaxis_title="Number of Files",
    )

    # Export to a single HTML file
    export_file = "/results/total-number-of-files.html"
    fig.write_html(export_file)
    print(f"Framework size bar charts exported to {export_file}")


def plot_h2load(results_dir):
    """
    Creates a bar chart of requests per second for all log files in the specified directory.
    """
    filenames = [
        os.path.join(results_dir, f)
        for f in os.listdir(results_dir)
        if f.endswith(".h2load.log")
    ]

    # filenames are in the format: laravel.bench.info.h2load.log, symfony.bench.hello.h2load.log
    # we want to extract the framework name and the benchmark name by splitting the filename
    frameworks = []
    benchmarks = []
    for filename in filenames:
        framework_name, benchmark_name = extract_info_from_filename(filename)
        frameworks.append(framework_name)
        benchmarks.append(benchmark_name)

    labels = []
    req_per_sec_values = []
    for i, filename in enumerate(filenames):
        labels.append(frameworks[i] + " - " + benchmarks[i])
        rps, command_args = parse_logfile(filename)
        req_per_sec_values.append(rps)

    # Initialize dictionaries to hold requests per second values for each benchmark type
    req_per_sec_by_bench = {"Info": [], "Hello": []}
    labels_by_bench = {"Info": [], "Hello": []}

    # Populate the dictionaries
    for i, filename in enumerate(filenames):
        bench_type = benchmarks[i]
        label = frameworks[i]
        req_per_sec = req_per_sec_values[i]
        req_per_sec_by_bench[bench_type].append(req_per_sec)
        labels_by_bench[bench_type].append(label)

    # Sort the data by requests per second in descending order
    for bench_type in req_per_sec_by_bench:
        req_per_sec_by_bench[bench_type], labels_by_bench[bench_type] = zip(
            *sorted(
                zip(req_per_sec_by_bench[bench_type], labels_by_bench[bench_type]),
                reverse=True,
            )
        )

    # Create subplots: one row, two columns
    fig = make_subplots(
        rows=1, cols=2, subplot_titles=("Info Benchmark", "Hello Benchmark")
    )

    # Add percentage to each bar, taking the maximum value as 100%
    for benchmark_type in ["Info", "Hello"]:
        percentages = calculate_percentages(req_per_sec_by_bench[benchmark_type])
        text_values = [f"{percentage:.2f}%" for percentage in percentages]

        fig.add_trace(
            go.Bar(
                x=labels_by_bench[benchmark_type],
                y=req_per_sec_by_bench[benchmark_type],
                name=benchmark_type,
                text=text_values,
                textposition="auto",
            ),
            row=1,
            col=1 if benchmark_type == "Info" else 2,
        )

    # Update layout to adjust titles and axis labels
    fig.update_layout(
        title_text=f"Framework requests per second comparison<br>(h2load {command_args})",
        xaxis_title="Framework",
        yaxis_title="Requests per Second (RPS)",
    )

    # Export to a single HTML file
    export_file = "/results/h2load-charts.html"
    fig.write_html(export_file)
    print(f"h2load bar charts exported to {export_file}")


def plot_wrk2(results_dir):
    # Prepare an empty DataFrame to store all latency data
    latency_data = pd.DataFrame()
    command_args = ""

    # Loop through each file in the logs directory
    for filename in os.listdir(results_dir):
        if filename.endswith(".wrk2.log"):
            framework_name, benchmark_name = extract_info_from_filename(filename)
            # Construct the full file path
            file_path = os.path.join(results_dir, filename)

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
            title=f"Latency by percentile ({benchmark_name} benchmark)<br>(wrk2 {command_args})",
        )

        # Export the plot to a separate HTML file for each bench_name
        export_file = f"/results/wrk2-charts-{benchmark_name}.html"
        fig.write_html(export_file)
        print(f"Latency charts for {benchmark_name} exported to {export_file}")


def plot_wrk(results_dir):
    # Regular expression patterns to extract data
    latency_pattern = re.compile(r"Latency\s+(\d+\.\d+)ms")
    req_sec_pattern = re.compile(r"Req/Sec\s+(\d+\.\d+k?)")

    # Data structure to hold the parsed results
    results = {}

    # Iterate over each file in the results directory
    for filename in os.listdir(results_dir):
        if filename.endswith(".wrk.log"):
            framework_name, benchmark_name = extract_info_from_filename(filename)
            with open(
                os.path.join(results_dir, filename), "r", encoding="utf-8"
            ) as file:
                content = file.read()
                # The first line of the file contains the wrk command used
                command_args = content.split("\n")[0]
                # Extract the average latency and requests per second
                avg_latency = float(latency_pattern.search(content).group(1))
                avg_req_sec = req_sec_pattern.search(content).group(1)
                # Convert avg_req_sec to requests/sec if the value ends with 'k'
                if "k" in str(avg_req_sec):
                    avg_req_sec = float(avg_req_sec.replace("k", "")) * 1000
                if benchmark_name not in results:
                    results[benchmark_name] = {
                        "frameworks": [],
                        "latencies": [],
                        "req_secs": [],
                    }
                results[benchmark_name]["frameworks"].append(framework_name)
                results[benchmark_name]["latencies"].append(avg_latency)
                results[benchmark_name]["req_secs"].append(avg_req_sec)

    # Create subplots
    fig = make_subplots(
        rows=2,
        cols=len(results),
        subplot_titles=[f"Benchmark: {bench_name}" for bench_name in results.keys()],
    )

    # order latencies in ascending and req_secs descending order
    for benchmark_name, data in results.items():
        data["framework"], data["latencies"], data["req_secs"] = zip(
            *sorted(
                zip(data["frameworks"], data["latencies"], data["req_secs"]),
                key=lambda x: x[1],
            )
        )

    col = 1
    for benchmark_name, data in results.items():
        # Add the latency bar chart
        fig.add_trace(
            go.Bar(x=data["framework"], y=data["latencies"], name="Avg Latency (ms)"),
            row=1,
            col=col,
        )
        # Add the requests per second bar chart
        fig.add_trace(
            go.Bar(x=data["framework"], y=data["req_secs"], name="Avg Req/Sec"),
            row=2,
            col=col,
        )
        # Add x and y axis titles
        fig.update_xaxes(title_text="Framework", row=1, col=col)
        fig.update_yaxes(title_text="Avg Latency (ms), lower is better", row=1, col=col)
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
    export_file = f"/results/wrk_charts.html"
    fig.write_html(export_file)
    print(f"wrk charts exported to {export_file}")


if __name__ == "__main__":
    # Specify the directory containing the log files
    output_dir = "/results"
    plot_total_number_of_files(
        count_files("/www/html", ["storage", "var", "logs", "cache", "writable"])
    )
    plot_h2load(output_dir)
    plot_wrk(output_dir)
    plot_wrk2(output_dir)
