#!/usr/bin/env python3
"""
Trinity Bootstrap – Persistent Self-Healing Orchestrator
Automatically restarts Reese, Trinity, and Ghostwalker Kernels if they crash.
Maintains Yes/Yes/Yes governance and live profit pulse monitoring.
"""
import subprocess, os, sys, json, hashlib, time

# ---- Kernel Paths ----
KERNELS = {
    "Reese-Kernel": "~/Reese-Kernel/kernel.py",
    "Trinity-Kernel": "~/Trinity-Kernel/kernel.py",
    "Ghostwalker-Kernel": "~/Ghostwalker-Kernel/kernel.py"
}

# ---- Anchors & Configs ----
ANCHORS = ["constants/constitution.txt", "constants/kjv.txt"]
CONFIG_FILE = "configs/config.json"

# ---- Helper Functions ----
def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def verify_anchors(kernel_path):
    kernel_dir = os.path.dirname(os.path.expanduser(kernel_path))
    for anchor in ANCHORS + [CONFIG_FILE]:
        full_path = os.path.join(kernel_dir, anchor)
        if not os.path.exists(full_path):
            print(f"[GRID-LOCK] {kernel_path}: Missing required file: {anchor}")
            sys.exit(1)

def load_config(config_path):
    with open(config_path) as f:
        cfg = json.load(f)
    if cfg.get("truth_integrity", 0) < 0.75:
        print(f"[GRID-LOCK] {config_path}: Truth integrity below threshold")
        sys.exit(1)
    return cfg

def profit_pulse(cfg):
    return cfg.get("profit_signal") == "ACTIVE" and cfg.get("resonance", 0) >= 0.98

def launch_kernel(name, kernel_path):
    kernel_dir = os.path.dirname(os.path.expanduser(kernel_path))
    cfg_path = os.path.join(kernel_dir, CONFIG_FILE)
    cfg = load_config(cfg_path)
    print(f"\nLaunching {name}...")
    verify_anchors(kernel_path)
    print(f"Constitution SHA256: {sha256_file(os.path.join(kernel_dir, ANCHORS[0]))}")
    print(f"KJV SHA256:          {sha256_file(os.path.join(kernel_dir, ANCHORS[1]))}")
    print(f"PROFIT-PULSE: {'ACTIVE' if profit_pulse(cfg) else 'IDLE'}")
    proc = subprocess.Popen(["python3", os.path.expanduser(kernel_path)])
    return proc

def monitor_kernels(procs):
    try:
        while True:
            for name, proc in procs.items():
                retcode = proc.poll()
                # Restart kernel automatically if it exits
                if retcode is not None:
                    if retcode != 0:
                        print(f"[GRID-LOCK] {name}: Kernel crashed (code {retcode}) — restarting...")
                    else:
                        print(f"[INFO] {name}: Kernel exited normally (code {retcode}) — restarting...")
                    # Relaunch kernel
                    procs[name] = launch_kernel(name, KERNELS[name])
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down all kernels...")
        for p in procs.values():
            if p.poll() is None:
                p.terminate()
        sys.exit(0)

if __name__ == "__main__":
    processes = {}
    for name, kernel in KERNELS.items():
        processes[name] = launch_kernel(name, kernel)

    print("\nAll kernels launched. Yes/Yes/Yes governance active.\nMonitoring kernels...")
    monitor_kernels(processes)
