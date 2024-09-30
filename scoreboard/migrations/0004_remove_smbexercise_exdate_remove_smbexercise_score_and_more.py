# Generated by Django 5.1.1 on 2024-09-09 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scoreboard', '0003_smbexercise_exname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='smbexercise',
            name='exDate',
        ),
        migrations.RemoveField(
            model_name='smbexercise',
            name='score',
        ),
        migrations.AlterField(
            model_name='smbexercise',
            name='exName',
            field=models.CharField(default='SMB Exploitation Exercise (Win7 SP1)', max_length=255),
        ),
        migrations.AlterModelTable(
            name='smbexercise',
            table='scoreboard_smbexercise',
        ),
    ]