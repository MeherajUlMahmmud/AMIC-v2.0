# Generated by Django 3.2.13 on 2022-05-10 14:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pharmacy_control', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicineordermodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='medicineorderitemmodel',
            name='medicine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pharmacy_control.medicinemodel'),
        ),
        migrations.AddField(
            model_name='medicineorderitemmodel',
            name='medicine_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pharmacy_control.medicineordermodel'),
        ),
        migrations.AddField(
            model_name='medicinemodel',
            name='medicine_section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pharmacy_control.medicinesectionmodel'),
        ),
        migrations.AddField(
            model_name='medicinecartmodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='medicinecartitemmodel',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pharmacy_control.medicinecartmodel'),
        ),
        migrations.AddField(
            model_name='medicinecartitemmodel',
            name='medicine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pharmacy_control.medicinemodel'),
        ),
    ]
