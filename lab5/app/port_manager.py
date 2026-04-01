import os
import subprocess
import signal
import time


def find_process_on_port(port):
    """Находит PID процесса, который использует указанный порт"""
    try:
        result = subprocess.run(
            ['lsof', '-i', f':{port}'],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            return None
        lines = result.stdout.strip().split('\n')
        if len(lines) <= 1:
            return None
        for line in lines[1:]:
            parts = line.split()
            if len(parts) >= 2:
                try:
                    pid = int(parts[1])
                    return pid
                except ValueError:
                    continue
        return None
    except FileNotFoundError:
        print("lsof command not found. Please install lsof first.")
        return None
    except Exception as e:
        print(f"Error finding process on port {port}: {e}")
        return None


def kill_process(pid):
    """Завершает процесс по PID"""
    try:
        os.kill(pid, signal.SIGTERM)
        time.sleep(1)
        try:
            os.kill(pid, 0)
            os.kill(pid, signal.SIGKILL)
            time.sleep(0.5)
        except OSError:
            pass
        return True
    except ProcessLookupError:
        return True
    except PermissionError:
        print(f"Permission denied to kill process {pid}")
        return False
    except Exception as e:
        print(f"Error killing process {pid}: {e}")
        return False


def free_port(port):
    """Освобождает порт, завершая процесс, который его использует"""
    print(f"Checking port {port}...")
    pid = find_process_on_port(port)
    if pid is None:
        print(f"Port {port} is already free.")
        return True
    print(f"Found process using port {port}: PID={pid}")
    if kill_process(pid):
        time.sleep(1)
        pid_check = find_process_on_port(port)
        if pid_check is None:
            print(f"Successfully freed port {port}")
            return True
        else:
            print(f"Failed to free port {port}")
            return False
    else:
        print(f"Failed to kill process {pid}")
        return False


def run_server_with_port_check(port=5000, app=None):
    """Запускает сервер, предварительно освобождая порт если он занят"""
    free_port(port)
    if app:
        app.run(debug=True, port=port)
    else:
        from registration import app
        app.run(debug=True, port=port)