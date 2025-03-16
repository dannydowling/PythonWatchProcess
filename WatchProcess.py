
import os
import signal
import psutil
import platform

def check_connections(port):
    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr.port == port and conn.status == 'ESTABLISHED':
            return True  # Active connections exist
    return False  # No active connections

def pause_process(pid):
    if platform.system() == "Windows":
        psutil.Process(pid).suspend()
    else:
        os.kill(pid, signal.SIGSTOP)

def resume_process(pid):
    if platform.system() == "Windows":
        psutil.Process(pid).resume()
    else:
        os.kill(pid, signal.SIGCONT)

pid = input("enter a process id to watch: ")
port = input("enter a port to watch for: ")
def monitor_process(pid, port):
    state = check_connections(port)
    if state == True:
        resume_process(pid)
    else:
        pause_process(pid)
