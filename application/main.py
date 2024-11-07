# main.py

import sys
import subprocess
import importlib.metadata

required_packages = [
    'boto3',
    'pandas',
    'plotly',
    'python-dotenv',
    'ttkthemes',
    'pygments',
    'kaleido'
]

def ensure_pip():
    try:
        import pip
    except ImportError:
        print("pip is not installed. Installing pip...")
        subprocess.check_call([sys.executable, '-m', 'ensurepip', '--default-pip'])

def install_packages(packages):
    python = sys.executable
    try:
        subprocess.check_call([python, '-m', 'pip', 'install', '--user', *packages])
    except subprocess.CalledProcessError:
        print(f"Failed to install packages: {packages}")
        sys.exit(1)

def check_and_install_packages():
    installed_packages = {pkg.metadata['Name'].lower() for pkg in importlib.metadata.distributions()}
    missing_packages = [pkg for pkg in required_packages if pkg.lower() not in installed_packages]
    if missing_packages:
        print(f"Installing missing packages: {missing_packages}")
        install_packages(missing_packages)
    else:
        print("All required packages are already installed.")

ensure_pip()
check_and_install_packages()

##################################################################################################

import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import os

from aws_credentials import save_credentials, check_and_fill_credentials
from query_execution import execute_query
from syntax_highlighting import apply_syntax_highlighting
from table_display import display_table
from chart_creation import populate_chart_options, create_chart
import utils

def main():
    query_result_df = None

    def update_query_result_df(new_df):
        nonlocal query_result_df
        query_result_df = new_df

    theme = "breeze"
    root = ThemedTk(theme)  
    root.title("Athena Charts")
    root.geometry("600x600")
    root.resizable(False, False)

    icon_path = os.path.join(os.path.dirname(__file__), 'aws-athena.ico')
    
    try:
        root.iconbitmap(icon_path)
    except tk.TclError:
        print("Warning: Icon file not found or format not supported.")

    style = ttk.Style()
    style.theme_use(theme) 

    tab_control = ttk.Notebook(root)

    query_tab = ttk.Frame(tab_control)
    tab_control.add(query_tab, text="Query")

    ttk.Label(query_tab, text="Catalog:").grid(column=0, row=0, padx=5, pady=5, sticky="e")
    catalog_entry = ttk.Entry(query_tab, width=40)
    catalog_entry.grid(column=1, row=0, padx=5, pady=5, sticky="w")
    catalog_entry.insert(0, 'AwsDataCatalog')

    ttk.Label(query_tab, text="Database:").grid(column=0, row=1, padx=5, pady=5, sticky="e")
    database_entry = ttk.Entry(query_tab, width=40)
    database_entry.grid(column=1, row=1, padx=5, pady=5, sticky="w")

    ttk.Label(query_tab, text="Query:").grid(column=0, row=2, padx=5, pady=5, sticky="ne")
    query_text = tk.Text(query_tab, wrap="word", height=10, width=60, bg='white')
    query_text.grid(column=1, row=2, padx=5, pady=5)
    query_text.bind("<KeyRelease>", lambda event: apply_syntax_highlighting(query_text))

    ttk.Label(query_tab, text="Limit:").grid(column=0, row=3, padx=5, pady=5, sticky="e")
    limit_entry = ttk.Entry(query_tab, width=10)
    limit_entry.insert(0,100)
    limit_entry.grid(column=1, row=3, padx=5, pady=5, sticky="w")

    def execute_query_callback(df):
        max_rows = int(limit_entry.get().strip() or '1000')
        display_table(df, table_frame, max_rows)
        populate_chart_options(df, x_column_menu, y_column_menu, value_column_menu,
                            color_column_menu, size_column_menu, names_column_menu, values_column_menu)
        update_query_result_df(df)
        tab_control.tab(results_tab, state="normal")
        tab_control.select(results_tab)

    ttk.Button(query_tab, text="Execute Query", command=lambda: execute_query(
    database_entry, catalog_entry, query_text, limit_entry,
    execute_query_callback,
    tab_control, results_tab)).grid(column=1, row=5, padx=5, pady=10, sticky="e")

    results_tab = ttk.Frame(tab_control)
    tab_control.add(results_tab, text="Results and Charts", state="disabled")

    table_frame = ttk.Frame(results_tab)
    table_frame.pack(fill="both", padx=10, pady=10)

    options_frame = ttk.LabelFrame(results_tab, text="Chart Options")
    options_frame.pack(fill="x", padx=10, pady=10)

    ttk.Label(options_frame, text="Chart Type:").grid(row=0, column=0, padx=5, pady=5)
    chart_type_menu = ttk.Combobox(options_frame, values=utils.chart_types, width=15)
    chart_type_menu.grid(row=0, column=1, padx=5, pady=5)
    chart_type_menu.set(utils.chart_types[0])

    ttk.Label(options_frame, text="Chart Title:").grid(row=1, column=0, padx=5, pady=5)
    chart_title_entry = ttk.Entry(options_frame, width=20)
    chart_title_entry.grid(row=1, column=1, padx=5, pady=5)

    x_column_menu = ttk.Combobox(options_frame, width=15)
    y_column_menu = ttk.Combobox(options_frame, width=15)
    value_column_menu = ttk.Combobox(options_frame, width=15)
    color_style_menu = ttk.Combobox(options_frame, values=utils.dashboard_styles, width=15)
    color_style_menu.set(utils.dashboard_styles[0])

    color_column_menu = ttk.Combobox(options_frame, width=15)
    size_column_menu = ttk.Combobox(options_frame, width=15)
    names_column_menu = ttk.Combobox(options_frame, width=15)
    values_column_menu = ttk.Combobox(options_frame, width=15)

    create_chart_button = ttk.Button(options_frame, text="Create Chart", command=lambda: create_chart(
        query_result_df, x_column_menu, y_column_menu, value_column_menu,
        chart_title_entry, color_style_menu, chart_type_menu, color_column_menu,
        size_column_menu, names_column_menu, values_column_menu))

    def update_parameter_inputs(event=None):
        chart_type = chart_type_menu.get()

        for widget in options_frame.winfo_children():
            widget.grid_remove()

        ttk.Label(options_frame, text="Chart Type:").grid(row=0, column=0, padx=5, pady=5)
        chart_type_menu.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(options_frame, text="Chart Title:").grid(row=1, column=0, padx=5, pady=5)
        chart_title_entry.grid(row=1, column=1, padx=5, pady=5)

        row_index = 2

        if chart_type == "Heatmap":
            ttk.Label(options_frame, text="X Column:").grid(row=row_index, column=0, padx=5, pady=5)
            x_column_menu.grid(row=row_index, column=1, padx=5, pady=5)
            row_index += 1

            ttk.Label(options_frame, text="Y Column:").grid(row=row_index, column=0, padx=5, pady=5)
            y_column_menu.grid(row=row_index, column=1, padx=5, pady=5)
            row_index += 1

            ttk.Label(options_frame, text="Value Column:").grid(row=row_index, column=0, padx=5, pady=5)
            value_column_menu.grid(row=row_index, column=1, padx=5, pady=5)
            row_index += 1

            ttk.Label(options_frame, text="Color Style:").grid(row=row_index, column=0, padx=5, pady=5)
            color_style_menu.grid(row=row_index, column=1, padx=5, pady=5)
            row_index += 1

        elif chart_type in ["Line Chart", "Bar Chart", "Box Plot"]:
            ttk.Label(options_frame, text="X Column:").grid(row=row_index, column=0, padx=5, pady=5)
            x_column_menu.grid(row=row_index, column=1, padx=5, pady=5)
            row_index += 1

            ttk.Label(options_frame, text="Y Column:").grid(row=row_index, column=0, padx=5, pady=5)
            y_column_menu.grid(row=row_index, column=1, padx=5, pady=5)
            row_index += 1

        elif chart_type == "Scatter Plot":
            ttk.Label(options_frame, text="X Column:").grid(row=row_index, column=0, padx=5, pady=5)
            x_column_menu.grid(row=row_index, column=1, padx=5, pady=5)
            row_index += 1

            ttk.Label(options_frame, text="Y Column:").grid(row=row_index, column=0, padx=5, pady=5)
            y_column_menu.grid(row=row_index, column=1, padx=5, pady=5)
            row_index += 1

            ttk.Label(options_frame, text="Color Column (Optional):").grid(row=row_index, column=0, padx=5, pady=5)
            color_column_menu.grid(row=row_index, column=1, padx=5, pady=5)
            row_index += 1

            ttk.Label(options_frame, text="Size Column (Optional):").grid(row=row_index, column=0, padx=5, pady=5)
            size_column_menu.grid(row=row_index, column=1, padx=5, pady=5)
            row_index += 1

        elif chart_type == "Pie Chart":
            ttk.Label(options_frame, text="Names Column:").grid(row=row_index, column=0, padx=5, pady=5)
            names_column_menu.grid(row=row_index, column=1, padx=5, pady=5)
            row_index += 1

            ttk.Label(options_frame, text="Values Column:").grid(row=row_index, column=0, padx=5, pady=5)
            values_column_menu.grid(row=row_index, column=1, padx=5, pady=5)
            row_index += 1

        elif chart_type == "Histogram":
            ttk.Label(options_frame, text="X Column:").grid(row=row_index, column=0, padx=5, pady=5)
            x_column_menu.grid(row=row_index, column=1, padx=5, pady=5)
            row_index += 1

        create_chart_button.grid(row=row_index, column=1, padx=5, pady=10)

    chart_type_menu.bind("<<ComboboxSelected>>", update_parameter_inputs)

    update_parameter_inputs()

    config_tab = ttk.Frame(tab_control)
    tab_control.add(config_tab, text="Settings")

    ttk.Label(config_tab, text="AWS Access Key").grid(column=0, row=0, padx=10, pady=10)
    aws_access_key_entry = ttk.Entry(config_tab, width=40)
    aws_access_key_entry.grid(column=1, row=0, padx=10, pady=10)

    ttk.Label(config_tab, text="AWS Secret Key").grid(column=0, row=1, padx=10, pady=10)
    aws_secret_key_entry = ttk.Entry(config_tab, width=40, show="*")
    aws_secret_key_entry.grid(column=1, row=1, padx=10, pady=10)

    ttk.Label(config_tab, text="AWS Region").grid(column=0, row=2, padx=10, pady=10)
    aws_region_entry = ttk.Entry(config_tab, width=40)
    aws_region_entry.grid(column=1, row=2, padx=10, pady=10)

    ttk.Label(config_tab, text="Query Results Bucket").grid(column=0, row=3, padx=10, pady=10)
    output_bucket_entry = ttk.Entry(config_tab, width=40)
    output_bucket_entry.grid(column=1, row=3, padx=10, pady=10)

    save_button = ttk.Button(config_tab, text="Save Credentials", command=lambda: save_credentials(
        aws_access_key_entry, aws_secret_key_entry, aws_region_entry, output_bucket_entry))
    save_button.grid(column=1, row=4, padx=10, pady=10)

    check_and_fill_credentials(aws_access_key_entry, aws_secret_key_entry, aws_region_entry, output_bucket_entry)

    tab_control.pack(expand=1, fill="both")

    root.mainloop()

if __name__ == "__main__":
    main()
