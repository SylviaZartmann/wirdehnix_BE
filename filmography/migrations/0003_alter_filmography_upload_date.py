# Generated by Django 5.0 on 2024-01-11 10:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filmography', '0002_filmography_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filmography',
            name='upload_date',
            field=models.DateTimeField(default=datetime.date.today),
        ),
    ]
