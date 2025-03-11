from django.db import models



#class Process_object(models.Model):
#    Process_ID = models.IntegerField(default=10)
#    Process_Status =  charfield / enum?
#    Process_Start_Time = datetime
#    Process_Duration = time
#    Process_Name = charfield
#    Process_Memory_Usage = float
#    Process_CPU_Usage = float / percent?
    

#class Snapshot_object(models.Model):
#    Snapshot_ID = uid ?
#    Snapshot_Timestamp = datetime
#    Snapshot_Author = charfield | many to one -> User_Name 
#    Snapshot_Processes_ID = int | one to many -> Process_ID


#class KillLog_object(models.Model):
#    KillLog_ID = uid ?
#    KillLog_Timestamp = datetime
#    KillLog_Author = charfield | one to many -> User_Name 
#    KillLog_Process_Name = charfield | one to many -> Process_ID. 
#    KillLog_Status = 0
