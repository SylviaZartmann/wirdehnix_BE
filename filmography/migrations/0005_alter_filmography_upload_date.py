# Generated by Django 5.0 on 2024-01-11 11:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filmography', '0004_alter_filmography_upload_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filmography',
            name='upload_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]