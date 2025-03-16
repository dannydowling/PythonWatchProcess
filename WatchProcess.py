import os
import signal
import psutil
import platform
import time

def check_connections(port):
    """Check if there are active connections on the given port."""
    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr.port == port and conn.status == 'ESTABLISHED':
            return True  # Active connections exist
    return False  # No active connections

def pause_process(pid):
    """Pause the process."""
    if platform.system() == "Windows":
        psutil.Process(pid).suspend()
    else:
        os.kill(pid, signal.SIGSTOP)
    print(f"Process {pid} paused.")

def resume_process(pid):
    """Resume the process."""
    if platform.system() == "Windows":
        psutil.Process(pid).resume()
    else:
        os.kill(pid, signal.SIGCONT)
    print(f"Process {pid} resumed.")

def monitor_process(pid, port, delay=10):
    """Monitor the process and pause it after a period of inactivity."""
    inactive_since = None

    while True:
        if check_connections(port):
            if inactive_since is not None:
                print("Active connection detected, resuming process.")
            inactive_since = None
            resume_process(pid)
        else:
            if inactive_since is None:
                inactive_since = time.time()
            elif time.time() - inactive_since >= delay:
                print(f"No connections for {delay} seconds, pausing process.")
                pause_process(pid)
                inactive_since = None  # Reset the timer after pausing

        time.sleep(1)  # Check every second

if __name__ == "__main__":
    pid = int(input("Enter a process ID to watch: "))
    port = int(input("Enter a port to watch: "))
    monitor_process(pid, port)
