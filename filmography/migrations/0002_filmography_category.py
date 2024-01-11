# Generated by Django 5.0 on 2024-01-11 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filmography', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='filmography',
            name='category',
            field=models.CharField(choices=[('F', 'Fiction'), ('D', 'Documentary'), ('A', 'Animation'), ('H', 'Horror')], default='', max_length=50),
        ),
    ]
