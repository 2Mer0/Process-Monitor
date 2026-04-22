📌 Overview
This project is a lightweight system monitoring script written in Python.
It collects real‑time system metrics for CPU, RAM, GPU, and disk usage, evaluates their load levels, and outputs the results in JSON format.
The script is designed to be simple, fast, and suitable for automation, logging, or integration with other tools.

🧠 Features
The script gathers and reports:

✅ CPU usage and temperature
✅ RAM usage (percentage and GB)
✅ GPU usage, temperature, and VRAM (if available)
✅ Disk usage across mounted partitions
✅ Automatic load status classification:

light
medium
heavy


✅ JSON‑formatted output for easy parsing

⚙️ Load Thresholds
Each component is classified based on configurable thresholds.
The highest value (usage, temperature, or memory) determines the final status.

🧩 Components Explained
CPU Monitoring

Uses psutil to measure:

CPU usage percentage
CPU temperature (if supported by the system)


Returns a status based on usage/temperature

RAM Monitoring

Reports:

Percentage used
Used memory (GB)
Total memory (GB)



GPU Monitoring (Optional)

Uses nvidia-smi
Automatically detects if an NVIDIA GPU is available
Reports:

GPU name
Utilization %
Temperature
VRAM usage %



⚠️ If nvidia-smi is not present, GPU monitoring is automatically skipped.
Disk / I/O Monitoring

Iterates through mounted disk partitions
Reports used and total space for each disk
{
  "cpu": {
    "usage": 23.4,
    "temp": 45.0,
    "status": "light"
  },
  "ram": {
    "percent": 62.3,
    "used_gb": 9.12,
    "total_gb": 16.0,
    "status": "medium"
  },
  "gpu": {
    "available": false,
    "status": "light"
  },
  "io": {
    "disks": [
      {
        "device": "/dev/sda1",
        "percent": 71.2,
        "used_gb": 320.4,
        "total_gb": 450.0
      }
    ]
  }
}

🛠️ Libraries & Tools Used

Python 3
psutil
subprocess
json
nvidia-smi (optional, NVIDIA GPUs only)
📚 Educational Purpose
This project demonstrates:

System resource monitoring
Hardware status detection
External command execution
JSON data formatting
Defensive programming with error handling

It is suitable for systems programming, Linux utilities, or introductory DevOps concepts.


