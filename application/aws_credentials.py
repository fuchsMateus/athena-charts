# aws_credentials.py

import os
from dotenv import load_dotenv
from tkinter import messagebox

def save_credentials_to_env(aws_access_key, aws_secret_key, aws_region, output_bucket):
    with open(".env", "w") as f:
        f.write(f"AWS_ACCESS_KEY_ID={aws_access_key}\n")
        f.write(f"AWS_SECRET_ACCESS_KEY={aws_secret_key}\n")
        f.write(f"AWS_REGION={aws_region}\n")
        f.write(f"OUTPUT_BUCKET={output_bucket}\n")
    messagebox.showinfo("Configurations", "Credentials saved successfully")

def load_credentials_from_env():
    load_dotenv()
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION")
    output_bucket = os.getenv("OUTPUT_BUCKET")
    return aws_access_key, aws_secret_key, aws_region, output_bucket

def check_and_fill_credentials(aws_access_key_entry, aws_secret_key_entry, aws_region_entry, output_bucket_entry):
    aws_access_key, aws_secret_key, aws_region, output_bucket = load_credentials_from_env()
    if aws_access_key:
        aws_access_key_entry.insert(0, aws_access_key)
    if aws_secret_key:
        aws_secret_key_entry.insert(0, aws_secret_key)
    if aws_region:
        aws_region_entry.insert(0, aws_region)
    if output_bucket:
        output_bucket_entry.insert(0, output_bucket)

def save_credentials(aws_access_key_entry, aws_secret_key_entry, aws_region_entry, output_bucket_entry):
    aws_access_key = aws_access_key_entry.get()
    aws_secret_key = aws_secret_key_entry.get()
    aws_region = aws_region_entry.get()
    output_bucket = output_bucket_entry.get()
    if aws_access_key and aws_secret_key and aws_region and output_bucket:
        save_credentials_to_env(aws_access_key, aws_secret_key, aws_region, output_bucket)
    else:
        messagebox.showerror("Error", "Please fill in all AWS credentials")