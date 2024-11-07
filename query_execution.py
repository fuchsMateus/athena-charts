# query_execution.py

import os
from dotenv import load_dotenv
from tkinter import messagebox
from athena_client import AthenaClient

athena_client = None

def execute_query(database_entry, catalog_entry, query_text, limit_entry, callback, tab_control, results_tab):
    global athena_client
    if athena_client is None:
        load_dotenv()
        aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        aws_region = os.getenv("AWS_REGION")
        output_bucket = os.getenv("OUTPUT_BUCKET")

        if not (aws_access_key and aws_secret_key and aws_region):
            messagebox.showerror("Error", "Please setup AWS credentials first.")
            return

        athena_client = AthenaClient(aws_access_key, aws_secret_key, aws_region, output_bucket)

    database = database_entry.get().strip()
    catalog = catalog_entry.get().strip()
    query = query_text.get("1.0", "end").strip()
    limit = limit_entry.get().strip()
    

    if not (database and catalog and query):
        messagebox.showerror("Error", "Please fill in Database and Query fields.")
        return

    if limit and 'limit' not in query.lower():
        query += f" LIMIT {limit}"

    max_rows = int(limit_entry.get().strip() or '1000')  

    try:
        query_result_df = athena_client.execute_query(query, database, catalog, max_rows)
        callback(query_result_df)
        tab_control.select(results_tab)
    except Exception as e:
        messagebox.showerror("Error", f"Error executing query: {e}")
