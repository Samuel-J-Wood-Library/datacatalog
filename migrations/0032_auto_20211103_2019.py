# Generated by Django 3.2 on 2021-11-04 01:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacatalog', '0031_auto_20211101_2007'),
    ]

    operations = [
        migrations.AddField(
            model_name='retentionrequest',
            name='milestone_pointer',
            field=models.CharField(default='Enter reference here', max_length=64),
        ),
        migrations.AlterField(
            model_name='retentionrequest',
            name='milestone_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]