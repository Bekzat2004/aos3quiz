import platform
import psutil
import os
import socket
import time
import matplotlib.pyplot as plt

from colorama import init, Fore, Style

# Define global variables for data collection
cpu_usage_data = []
memory_usage_data = []
disk_space_data = []


def collect_data(interval_minutes, duration_hours):
    """
    Collect system parameters at regular intervals over a specified duration.
    """
    end_time = time.time() + duration_hours * 3600  # Calculate end time

    while time.time() < end_time:
        # Collect CPU usage
        cpu_usage = psutil.cpu_percent(interval=1)
        cpu_usage_data.append(cpu_usage)

        # Collect memory usage
        memory_usage = psutil.virtual_memory().percent
        memory_usage_data.append(memory_usage)

        # Collect disk space
        disk_usage = psutil.disk_usage('/')
        available_disk_space_gb = round(disk_usage.free / (1024 ** 3), 2)
        disk_space_data.append(available_disk_space_gb)

        time.sleep(interval_minutes * 60)  # Wait for the next interval


def analyze_data():
    """
    Analyze collected data to find patterns.
    """
    # Calculate average CPU usage
    avg_cpu_usage = sum(cpu_usage_data) / len(cpu_usage_data)
    peak_cpu_time = cpu_usage_data.index(max(cpu_usage_data))

    # Find process with highest memory usage
    processes_info = psutil.process_iter(attrs=['pid', 'name', 'memory_percent'])
    max_memory_process = max(processes_info, key=lambda p: p.info['memory_percent'])

    # Plot CPU and memory usage over time
    plt.figure(figsize=(10, 5))
    plt.plot(cpu_usage_data, label='CPU Usage (%)')
    plt.plot(memory_usage_data, label='Memory Usage (%)')
    plt.xlabel('Time (minutes)')
    plt.ylabel('Usage (%)')
    plt.title('CPU and Memory Usage Over Time')
    plt.legend()
    plt.show()

    # Plot available disk space over time
    plt.figure(figsize=(10, 5))
    plt.plot(disk_space_data, label='Available Disk Space (GB)', color='green')
    plt.xlabel('Time (minutes)')
    plt.ylabel('Available Disk Space (GB)')
    plt.title('Available Disk Space Over Time')
    plt.legend()
    plt.show()

    # Print analysis results
    print("Analysis Results:")
    print(f"1. Average CPU Usage: {avg_cpu_usage:.2f}%")
    print(f"   Peak CPU Usage: {max(cpu_usage_data):.2f}% at {peak_cpu_time} minutes")
    print(f"2. Process with Highest Memory Usage: {max_memory_process.info['name']} "
          f"({max_memory_process.info['memory_percent']:.2f}%)")


if __name__ == "__main__":
    init()  # Initialize colorama for cross-platform colored output

    # Collect data for 1 hour at 1-minute intervals
    collect_data(interval_minutes=1, duration_hours=0.05)  # Collect data for 0.1 hours (6 minutes)

    # Analyze collected data
    analyze_data()