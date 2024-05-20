import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.dates import DateFormatter, MinuteLocator

def generate_line_chart_from_csv(csv_file_path):
    # Read the CSV file
    df = pd.read_csv(csv_file_path)
    
    # Convert SK to datetime
    df['SK'] = pd.to_datetime(df['SK'])
    
    # Plot the data
    plt.figure(figsize=(12, 6))
    plt.plot(df['SK'], df['rating'], marker='o', linestyle='-', color='b')
    plt.title("Ratings Over Time")
    plt.xlabel("Time")
    plt.ylabel("Rating")
    plt.grid(True)
    plt.xticks(rotation=45)
    
    # Format x-axis to display only hours and minutes
    ax = plt.gca()
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
    ax.xaxis.set_major_locator(MinuteLocator(interval=10))
    
    plt.tight_layout()
    
    # Show the plot
    plt.show()


# Example usage
csv_file_path = 'results.csv'
generate_line_chart_from_csv(csv_file_path)
