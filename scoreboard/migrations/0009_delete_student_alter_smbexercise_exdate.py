# Generated by Django 5.1.1 on 2024-09-19 06:52

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scoreboard', '0008_alter_smbexercise_explayer'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Student',
        ),
        migrations.AlterField(
            model_name='smbexercise',
            name='exDate',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]