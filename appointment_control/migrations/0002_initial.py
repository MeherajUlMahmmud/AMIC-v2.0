# Generated by Django 4.0.3 on 2022-04-08 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_control', '0001_initial'),
        ('appointment_control', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentmodel',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_control.doctormodel'),
        ),
        migrations.AddField(
            model_name='appointmentmodel',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_control.patientmodel'),
        ),
    ]