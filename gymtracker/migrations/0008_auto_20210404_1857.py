# Generated by Django 3.1.7 on 2021-04-04 17:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gymtracker', '0007_auto_20210404_1718'),
    ]

    operations = [
        migrations.RenameField(
            model_name='set',
            old_name='exercise_id',
            new_name='exercise',
        ),
    ]
