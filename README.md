# System Scanner

A system scanner application built with PyQt6 to monitor system information, running processes, storage, network, and security services in real-time.

## Features

- **System Information**: Displays OS, architecture, processor, and uptime.
- **Processes**: Lists running processes with CPU and memory usage.
- **Storage**: Shows disk usage including total, used, and free space for each partition.
- **Network**: Displays network interfaces and addresses.
- **Security**: Displays basic security services like firewall and antivirus status.
- **Real-Time Monitoring**: Continuously monitors CPU and memory usage.
- **Customizable UI**: Modern, dark-themed interface with shadow effects and custom widgets.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/HuddyLatimer/system-scanner.git
    ```

2. Navigate to the project directory:
    ```bash
    cd system-scanner
    ```

3. Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment:
    - On Windows:
      ```bash
      .\venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

5. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the application:

1. Ensure you have Python 3.6 or higher installed.
2. Run the application:
    ```bash
    python main.py
    ```

3. The system scanner window will open, and you can start scanning your system information, processes, storage, and network.

## Dependencies

- `psutil`
- `platform`
- `PyQt6`
- `wmi`
- `datetime`
- `json`
- `os`

## Showcase


https://github.com/user-attachments/assets/c28981b7-8f42-4879-978d-e45024164ac8



## Acknowledgements

- **PyQt6**: For creating the GUI framework.
- **psutil**: For gathering system and process information.
