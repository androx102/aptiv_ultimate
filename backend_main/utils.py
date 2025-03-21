import psutil
import datetime
import openpyxl
from django.http import JsonResponse, HttpResponse
from .models import *
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


def create_excel(snap_id):
    try:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Snapshot details"


        ws.append(["PID",
                   "Status",
                   "Start time",
                   "Duration",
                   "Name",
                   "Memory usage",
                   "CPU usage",
                   ]) 

        processes = ProcessObject.objects.filter(snapshot__snapshot_id=snap_id)  

        for proc in list(processes.values()):
            ws.append([proc["process_id"],
                       proc["process_status"],
                       proc["process_start_time"].replace(tzinfo=None),
                       proc["process_duration"],
                       proc["process_name"],
                       proc["process_memory_usage"],
                       proc["process_cpu_usage"],
                       ])  
        
        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = f'attachment; filename="snapshot_{snap_id}.xlsx"'
        wb.save(response)
        return True, response
    except Exception as e:
        return False, e
    