# Generated by Django 5.1.1 on 2024-09-09 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scoreboard', '0002_smbexercise'),
    ]

    operations = [
        migrations.AddField(
            model_name='smbexercise',
            name='exName',
            field=models.CharField(default='SMB Module Exploitation Exercise (Win7 SP1)', max_length=100),
        ),
    ]