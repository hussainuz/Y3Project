# Generated by Django 3.1.7 on 2021-04-04 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gymtracker', '0006_workout_owner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exercise',
            old_name='workout_id',
            new_name='workout',
        ),
    ]
