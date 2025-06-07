# CSV Processor for Server Data

This Python script processes a CSV file containing server information to generate three summary reports: a count of unique operating systems, a count of unique hostnames, and a count of unique vulnerabilities.

## 📜 Description

The primary purpose of this tool is to provide a quick and easy way to get high-level summaries from a server data export. It reads a CSV file, extracts specific columns for hostnames, operating systems, and vulnerabilities, and then outputs three separate, timestamped CSV files with the aggregated data. This is particularly useful for system administrators, security analysts, or anyone needing a quick overview of their server fleet's composition and security posture.

## 🚀 Getting Started

### Prerequisites

* Python 3.6+
* Pandas library

### Installation

1.  Clone the repository:
    ```bash
    git clone [https://github.com/your-username/your-repository-name.git](https://github.com/jamiedarville/csv-processor.git)
    cd your-repository-name
    ```

2.  It's highly recommended to use a virtual environment:
    ```bash
    python3 -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3.  Install the required Python packages from the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```

### Usage

You can run the script from the command line, optionally providing the input file path and an output directory. The script defaults to using a file named `input_data.csv` in the same directory.

**Basic Usage**
```bash
python csv_processor.py
```

**Specifying an Input File**
```bash
python csv_processor.py /path/to/your/server_data.csv
```

**Specifying an Input File and Output Directory**
```bash
python csv_processor.py /path/to/your/server_data.csv /path/to/save/reports/
```

The script expects the input CSV to have data in at least these columns:
* **Column C (index 2):** Hostnames
* **Column E (index 4):** Operating Systems
* **Column H (index 7):** Vulnerabilities

## 📄 Output Files

The script will generate three CSV files in the specified output directory (or the input file's directory by default). Each filename is timestamped to prevent overwriting previous reports.

* `os_summary_YYYYMMDD_HHMMSS.csv`: A summary of the counts of each unique operating system.
* `hostname_summary_YYYYMMDD_HHMMSS.csv`: A summary of the counts of each unique hostname.
* `vuln_YYYYMMDD_HHMMSS.csv`: A summary of the counts of each unique vulnerability.

## 📝 License

This project is licensed under the MIT License - see the **LICENSE** file for details.
