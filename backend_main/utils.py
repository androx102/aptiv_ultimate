import psutil
import datetime
import json

def get_process_info():
    process_list = []

    for proc in psutil.process_iter(attrs=['pid', 'status', 'create_time', 'name', 'memory_info', 'cpu_percent']):
        try:
            process_info = {
                "process_id": proc.info['pid'],
                "process_status": proc.info['status'],
                "process_start_time": datetime.datetime.fromtimestamp(proc.info['create_time']).strftime("%Y-%m-%d %H:%M:%S"),
                "process_duration": str(datetime.datetime.now() - datetime.datetime.fromtimestamp(proc.info['create_time'])).split('.')[0],
                "process_name": proc.info['name'],
                "process_memory_usage": round(proc.info['memory_info'].rss / (1024 * 1024), 2),
                "process_cpu_usage": proc.cpu_percent()
            }
            if proc.info['pid'] != 0:
                process_list.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    return process_list 