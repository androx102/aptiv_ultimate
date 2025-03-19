# Generated by Django 5.1.3 on 2025-03-19 23:04

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='KillLog_object',
            fields=[
                ('KillLog_ID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('KillLog_Timestamp', models.DateTimeField(auto_now_add=True)),
                ('KillLog_Process_Name', models.CharField(max_length=255)),
                ('KillLog_Author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kills', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
