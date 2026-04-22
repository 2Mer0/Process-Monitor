#!/usr/bin/env python3
import psutil
import subprocess
import json

# Config
CPU_WARN, CPU_CRIT = 60, 85
RAM_WARN, RAM_CRIT = 70, 85
GPU_WARN, GPU_CRIT = 70, 90

def status(val, warn, crit):
    if val >= crit: return "heavy"
    if val >= warn: return "medium"
    return "light"

def get_cpu():
    usage = psutil.cpu_percent(interval=0.1)
    temp = 0
    try:
        temps = psutil.sensors_temperatures()
        for entries in temps.values():
            if entries:
                temp = entries[0].current
                break
    except:
        pass
    return {
        "usage": round(usage, 1),
        "temp": round(temp, 1),
        "status": status(max(usage, temp), CPU_WARN, CPU_CRIT)
    }

def get_ram():
    mem = psutil.virtual_memory()
    return {
        "percent": round(mem.percent, 1),
        "used_gb": round(mem.used / (1024**3), 2),
        "total_gb": round(mem.total / (1024**3), 2),
        "status": status(mem.percent, RAM_WARN, RAM_CRIT)
    }

def get_gpu():
    gpu = {"available": False, "status": "light"}
    try:
        r = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,utilization.gpu,temperature.gpu,memory.used,memory.total",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=3
        )
        if r.returncode == 0:
            v = [x.strip() for x in r.stdout.strip().split(",")]
            used, total = float(v[3]), float(v[4])
            vram_pct = round((used / total) * 100, 1) if total else 0
            gpu = {
                "available": True,
                "name": v[0],
                "usage": float(v[1]),
                "temp": float(v[2]),
                "vram_percent": vram_pct,
                "status": status(max(float(v[1]), float(v[2]), vram_pct), GPU_WARN, GPU_CRIT)
            }
    except:
        pass
    return gpu

def get_io():
    disks = []
    for p in psutil.disk_partitions():
        try:
            u = psutil.disk_usage(p.mountpoint)
            disks.append({
                "device": p.device,
                "percent": u.percent,
                "used_gb": round(u.used / (1024**3), 2),
                "total_gb": round(u.total / (1024**3), 2)
            })
        except:
            continue
    return {"disks": disks}

def get_metrics():
    return {
        "cpu": get_cpu(),
        "ram": get_ram(),
        "gpu": get_gpu(),
        "io": get_io()
    }

if __name__ == "__main__":
    print(json.dumps(get_metrics(), indent=2))