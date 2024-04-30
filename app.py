import tkinter as tk
from tkinter import messagebox, filedialog
import Data
import pandas as pd
import matplotlib.pyplot as plt

# Function to fetch data when the corresponding button is clicked
def fetch_data(fetch_func, success_msg):
    success, msg = fetch_func()
    if success:
        messagebox.showinfo("Success", success_msg)
    else:
        messagebox.showerror("Error", msg)

# Function to save datasets to CSV files
def save_datasets():
    success, msg = Data.save_datasets()
    if success:
        messagebox.showinfo("Success", msg)
    else:
        messagebox.showerror("Error", msg)

# Function to perform exploratory data analysis (EDA) and display in the notification panel
def perform_eda_and_display(df, eda_func):
    success, result = eda_func(df)
    if success:
        notification_text.set(result)
    else:
        messagebox.showerror("Error", result)

# Function to merge datasets
def merge_datasets():
    # Check if all datasets are available
    if Data.covid_df is not None and Data.who_df is not None and Data.population_df is not None and Data.quality_of_life_df is not None:
        # Merge the datasets
        merged_df = pd.merge(Data.covid_df, Data.who_df, on='Country', how='inner')
        merged_df = pd.merge(merged_df, Data.population_df, on='Country', how='inner')
        merged_df = pd.merge(merged_df, Data.quality_of_life_df, on='Country', how='inner')
        
        # Ask user to choose the save location
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=(("CSV files", "*.csv"), ("All files", "*.*")), initialfile="merged_dataset.csv")
        if file_path:
            success, msg = Data.save_to_csv(merged_df, file_path)
            if success:
                messagebox.showinfo("Success", msg)
            else:
                messagebox.showerror("Error", msg)
    else:
        messagebox.showerror("Error", "One or more datasets are missing. Please fetch all datasets first.")

# Function to check headers of a DataFrame
def check_headers():
    if Data.covid_df is not None:
        headers = Data.covid_df.columns.tolist()
        messagebox.showinfo("Headers", headers)
    else:
        messagebox.showerror("Error", "DataFrame is empty.")

# Function to display shape of a DataFrame
def display_shape(df):
    if df is not None:
        shape = df.shape
        return (True, f"DataFrame Shape: {shape}")
    else:
        return (False, "DataFrame is empty.")

# Function to display column names of a DataFrame
def display_columns():
    if Data.covid_df is not None:
        columns = Data.covid_df.columns.tolist()
        messagebox.showinfo("DataFrame Columns", columns)
    else:
        messagebox.showerror("Error", "DataFrame is empty.")

# Function to visualize merged dataset
def visualize_merged_dataset(df):
    if df is not None:
        # Sample visualization (you can replace this with your desired visualization)
        plt.figure(figsize=(10, 6))
        plt.scatter(df['Population'], df['Life Expectancy'], alpha=0.5)
        plt.title('Population vs Life Expectancy')
        plt.xlabel('Population')
        plt.ylabel('Life Expectancy')
        plt.grid(True)
        plt.show()
    else:
        messagebox.showerror("Error", "DataFrame is empty.")

# Create the main window
root = tk.Tk()
root.title("INTELLIGENT APPLICATION FOR DATA ANALYSIS")

# Create a frame to contain the buttons
button_frame = tk.Frame(root, bg="#f0f0f0")  # Set background color
button_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)  # Add padding

# Create the notification panel frame
notification_frame = tk.Frame(root, bg="#ffffff", bd=1, relief=tk.SUNKEN)
notification_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

# Variable to store notification text
notification_text = tk.StringVar()
notification_text.set("Notification Panel")

# Label to display notification text
notification_label = tk.Label(notification_frame, textvariable=notification_text, bg="#ffffff", anchor="nw", justify="left", padx=10, pady=10)
notification_label.pack(fill="both", expand=True)

# Create the "GET DATA" buttons
get_covid_button = tk.Button(button_frame, text="GET COVID-19 DATA", command=lambda: fetch_data(Data.get_covid_data, "COVID-19 data has been fetched successfully."), relief=tk.RAISED, padx=10, pady=5, anchor="w")
get_who_button = tk.Button(button_frame, text="GET WHO DATA", command=lambda: fetch_data(Data.get_who_data, "WHO health system ranking data has been fetched successfully."), relief=tk.RAISED, padx=10, pady=5, anchor="w")
get_population_button = tk.Button(button_frame, text="GET POPULATION DATA", command=lambda: fetch_data(Data.get_population_data, "World population data has been fetched successfully."), relief=tk.RAISED, padx=10, pady=5, anchor="w")
get_quality_of_life_button = tk.Button(button_frame, text="GET QUALITY OF LIFE DATA", command=lambda: fetch_data(Data.get_quality_of_life_data, "Quality of life ranking data has been fetched successfully."), relief=tk.RAISED, padx=10, pady=5, anchor="w")

# Create the "SAVE DATASETS" button
save_datasets_button = tk.Button(root, text="SAVE DATASETS", command=save_datasets, relief=tk.RAISED, padx=10, pady=5, anchor="w")

# Create the "EDA" button
eda_button = tk.Button(root, text="EXPLORATORY DATA ANALYSIS", command=lambda: perform_eda_and_display(Data.covid_df, display_shape), relief=tk.RAISED, padx=10, pady=5, anchor="w")

# Create the "MERGE DATASETS" button
merge_datasets_button = tk.Button(root, text="MERGE DATA", command=merge_datasets, relief=tk.RAISED, padx=10, pady=5, anchor="w")

# Create the buttons for displaying DataFrame information
check_headers_button = tk.Button(root, text="CHECK HEADERS", command=check_headers)
display_columns_button = tk.Button(root, text="CHECK COLUMN", command=display_columns)

# Create the button to visualize merged dataset
visualize_merged_button = tk.Button(root, text="VISUALIZE MERGED DATASET", command=lambda: visualize_merged_dataset(merged_df))

# Apply some style enhancements
get_covid_button.config(bg="#4CAF50", fg="white", font=('Helvetica', 10, 'bold'))  # Change background color, font color, and font style
get_who_button.config(bg="#2196F3", fg="white", font=('Helvetica', 10, 'bold'))
get_population_button.config(bg="#FFC107", fg="white", font=('Helvetica', 10, 'bold'))
get_quality_of_life_button.config(bg="#FF5722", fg="white", font=('Helvetica', 10, 'bold'))

save_datasets_button.config(bg="#607D8B", fg="white", font=('Helvetica', 10, 'bold'))
eda_button.config(bg="#9C27B0", fg="white", font=('Helvetica', 10, 'bold'))
merge_datasets_button.config(bg="#795548", fg="white", font=('Helvetica', 10, 'bold'))

check_headers_button.config(bg="#E91E63", fg="white", font=('Helvetica', 10, 'bold'))
display_columns_button.config(bg="#673AB7", fg="white", font=('Helvetica', 10, 'bold'))

visualize_merged_button.config(bg="#FF5722", fg="white", font=('Helvetica', 10, 'bold'))

# Arrange the widgets in the window
get_covid_button.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
get_who_button.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
get_population_button.grid(row=0, column=2, sticky="ew", padx=5, pady=5)
get_quality_of_life_button.grid(row=0, column=3, sticky="ew", padx=5, pady=5)
save_datasets_button.grid(row=1, column=0, columnspan=4, sticky="ew", padx=5, pady=5)
eda_button.grid(row=2, column=0, columnspan=4, sticky="ew", padx=5, pady=5)
merge_datasets_button.grid(row=3, column=0, columnspan=4, sticky="ew", padx=5, pady=5)
check_headers_button.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
display_columns_button.grid(row=4, column=1, sticky="ew", padx=5, pady=5)
visualize_merged_button.grid(row=4, column=2, sticky="ew", padx=5, pady=5)

# Run the main event loop
root.mainloop()
