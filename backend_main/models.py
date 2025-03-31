from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class UserObject(AbstractUser):
    class Role(models.IntegerChoices):
        ADMIN = 3, "Admin"
        MODERATOR = 2, "Read and kill"
        USER = 1, "Read only"

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    username = models.CharField(max_length=254, unique=True)
    email = models.EmailField(
        blank=True, max_length=254, verbose_name="email address", unique=True
    )
    user_role = models.IntegerField(choices=Role.choices, default=Role.USER)

    def __str__(self):
        return self.username


class SnapshotObject(models.Model):
    snapshot_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    snapshot_timestamp = models.DateTimeField(auto_now_add=True)
    snapshot_author = models.ForeignKey(
        UserObject, on_delete=models.CASCADE, related_name="snapshots"
    )

    def __str__(self):
        return f"Snapshot {self.snapshot_id} by {self.snapshot_author.username} at {self.snapshot_timestamp}"


class ProcessObject(models.Model):
    process_uid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    process_id = models.IntegerField(default=1000)
    process_status = models.CharField(max_length=254)
    process_start_time = models.DateTimeField()
    process_duration = models.DurationField()
    process_name = models.CharField(max_length=255, blank=True)
    process_memory_usage = models.FloatField()
    process_cpu_usage = models.FloatField(help_text="CPU usage percentage")

    snapshot = models.ForeignKey(
        SnapshotObject, on_delete=models.CASCADE, related_name="processes"
    )

    def __str__(self):
        return f"{self.process_name} (ID: {self.process_id})"


class KillLog_object(models.Model):
    KillLog_ID = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    KillLog_Timestamp = models.DateTimeField(auto_now_add=True)
    KillLog_Author = models.ForeignKey(
        UserObject, on_delete=models.CASCADE, related_name="kills"
    )
    KillLog_Process_Name = models.CharField(max_length=255)
    KillLog_Process_Id = models.IntegerField(default=1000)
