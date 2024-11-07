# Athena Charts

Athena Charts is a Python-based application for querying AWS Athena and visualizing data in a graphical user interface. It supports customizable charts to analyze data from AWS Athena, with easy configuration options for setting up credentials, query execution, and data display.

## Features
- Connects to AWS Athena for querying large datasets.
- Provides data visualization through various chart options.
- Easy configuration of AWS credentials and query parameters.
- Results are displayed within the application, allowing users to interact with data and create visual charts.

## .env File for AWS Credentials

This project uses a `.env` file to store AWS credentials required for executing queries and generating charts. Upon first run, you will be prompted to enter your AWS Access Key, Secret Key, and other configurations, which will then be saved in this `.env` file. 

### Important Notice

This `.env` file contains sensitive information and should be used strictly for personal purposes. Please take the following precautions:
- **Do not share** the `.env` file with others or commit it to any version control system (e.g., GitHub, GitLab).
- **Restrict access** to the `.env` file to ensure that your AWS credentials remain secure.

## Requirements
- Python 3.x installed on your system.
- The required Python packages will be automatically installed if they are not present.

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/fuchsMateus/athena-charts.git
    cd athena-charts
    ```

2. Run the application:

    - **Windows**: Run the script `run_app.bat` by double-clicking on it or from the command line with:
      ```cmd
      run_app.bat
      ```

    - **Linux**: Execute the `run_app.sh` script:
      ```bash
      ./run_app.sh
      ```

    The application will start and prompt for any required package installations if they are missing. The application will then open a window with options to input AWS credentials, configure query parameters, and view results.

## Configuration

### AWS Credentials
You can configure your AWS credentials directly in the application under the **Settings** tab. Make sure to provide:
- AWS Access Key
- AWS Secret Key
- AWS Region
- S3 Bucket for store query results

### Querying Data
In the **Query** tab, you can specify the Athena catalog, database, and query to execute. Additionally, set the **Limit** for the number of rows retrieved.

## Usage
- Open the **Query** tab to input and execute SQL queries.
- Use the **Results and Charts** tab to view and customize charts for your data.
- Save your AWS credentials in the **Settings** tab for future use.