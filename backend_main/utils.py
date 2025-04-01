import psutil
import datetime
import openpyxl
from django.http import HttpResponse
from django.conf import settings
from .models import ProcessObject


def get_process_info():
    process_list = []
    if settings.DUMMY_PROCESS_DATA:
        process_info = {
            "process_id": 2137,
            "process_status": "sleeping",
            "process_start_time":"2025-03-20 20:43:30",
            "process_duration":2307000000,
            "process_name":"test_proc",
            "process_memory_usage":12,
            "process_cpu_usage":0.1,
        }
        process_list.append(process_info)
        process_list.append(process_info)
        process_list.append(process_info)
        return True, process_list




    try:
        for proc in psutil.process_iter(
            attrs=["pid", "status", "create_time", "name", "memory_info", "cpu_percent"]
        ):
            try:
                process_info = {
                    "process_id": proc.info["pid"],
                    "process_status": proc.info["status"],
                    "process_start_time": datetime.datetime.fromtimestamp(
                        proc.info["create_time"]
                    ).strftime("%Y-%m-%d %H:%M:%S"),
                    "process_duration": str(
                        datetime.datetime.now()
                        - datetime.datetime.fromtimestamp(proc.info["create_time"])
                    ).split(".")[0],
                    "process_name": proc.info["name"],
                    "process_memory_usage": round(
                        proc.info["memory_info"].rss / (1024 * 1024), 2
                    ),
                    "process_cpu_usage": proc.cpu_percent(),
                }
                if proc.info["pid"] != 0:
                    process_list.append(process_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        return True, process_list
    except Exception as e:
        return False, f"{e}"


def kill_proc_by_id(pid):
    if settings.DUMMY_PROCESS_DATA:
        if pid == 2137:
            return True, "Proc killed sucesfully"
        else:
            return False, f"Proc with PID: {pid} is not existing"


    try:
        # Get proc to kill by PID
        proc_to_kill = psutil.Process(pid)

        # Get his children
        children = proc_to_kill.children(recursive=True)

        # Send termination signal to children
        for proc in children:
            proc.terminate()

        # Check if chldren terminated
        _, survivors = psutil.wait_procs(children, timeout=5)

        # LET THEM DIE!
        for survivor in survivors:
            survivor.kill()

        # Kill main proc
        try:
            proc_to_kill.terminate()
            proc_to_kill.wait(5)
        except psutil.TimeoutExpired:
            proc_to_kill.kill()

        return True, "Proc killed sucesfully"

    except Exception as e:
        return False, f"{e}"


def create_excel(snap_id):
    try:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Snapshot details"

        ws.append(
            [
                "PID",
                "Status",
                "Start time",
                "Duration",
                "Name",
                "Memory usage",
                "CPU usage",
            ]
        )

        processes = ProcessObject.objects.filter(snapshot__snapshot_id=snap_id)

        for proc in list(processes.values()):
            ws.append(
                [
                    proc["process_id"],
                    proc["process_status"],
                    proc["process_start_time"].replace(tzinfo=None),
                    proc["process_duration"],
                    proc["process_name"],
                    proc["process_memory_usage"],
                    proc["process_cpu_usage"],
                ]
            )

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = (
            f'attachment; filename="snapshot_{snap_id}.xlsx"'
        )
        wb.save(response)
        return True, response
    except Exception as e:
        return False, e
