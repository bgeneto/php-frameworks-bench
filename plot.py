import os

import plotly.graph_objects as go
from plotly.subplots import make_subplots


def parse_logfile(filename):
    """
    Parses a log file and retrieves the requests per second value.
    """
    with open(filename, "r") as f:
        for line in f:
            if "finished in" in line:
                # Extract requests per second value
                req_per_sec = float(line.split(", ")[1].split("req/s")[0])
                return req_per_sec
    raise ValueError("Could not find relevant data in log file")


def extract_info_from_filename(filename):
    # Split the filename by '.'
    parts = filename.split(".")

    # The framework name is the first part
    framework_name = parts[0].split("/")[-1].capitalize()

    # The benchmark name is the second part
    benchmark_name = parts[2].capitalize()

    return framework_name, benchmark_name


# Function to calculate percentages
def calculate_percentages(values):
    max_value = max(values)
    percentages = [(value / max_value) * 100 for value in values]
    return percentages


def create_bar_chart(log_directory):
    """
    Creates a bar chart of requests per second for all log files in the specified directory.
    """
    filenames = [
        os.path.join(log_directory, f)
        for f in os.listdir(log_directory)
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
        req_per_sec_values.append(parse_logfile(filename))

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
        title_text="Framework Requests per Second Comparison",
        xaxis_title="Framework",
        yaxis_title="Requests per Second (RPS)",
    )

    # Export to a single HTML file
    export_file = "/results/requests-per-second-charts.html"
    fig.write_html(export_file)
    print(f"Bar chart exported to {export_file}")

# Specify the directory containing the log files
log_directory = "/results"
create_bar_chart(log_directory)


