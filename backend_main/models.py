from django.db import models
from django.contrib.auth.models import AbstractUser



    



class User_object(AbstractUser):   
    class Role(models.IntegerChoices):
        ADMIN = 3, 'Admin'
        MODERATOR = 2, 'Read and kill'
        USER = 1, 'Read only'
        
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    
    username = models.CharField(max_length=254,unique=True)
    email= models.EmailField(blank=True, max_length=254, verbose_name='email address',unique=True)
    user_role = models.IntegerField(choices=Role.choices, default=1)



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
