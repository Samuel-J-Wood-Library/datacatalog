# Generated by Django 3.2 on 2021-11-26 22:42

import datacatalog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacatalog', '0035_auto_20211116_2008'),
    ]

    operations = [
        migrations.AddField(
            model_name='retentionrequest',
            name='methodfile',
            field=models.FileField(help_text='\n                                      Upload a document describing steps required to generate results files from \n                                      source data. \n                                      ', null=True, upload_to=datacatalog.models.method_directory_path),
        ),
        migrations.AlterField(
            model_name='datafield',
            name='scope',
            field=models.CharField(blank=True, help_text='\n                                       Descriptions of the scope of the data (eg. min, max, number of records, number\n                                       of null values, number of unique values)\n                                       ', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='title',
            field=models.CharField(help_text='\n                                       The name of the dataset, usually one sentence or short description of the dataset\n                                       ', max_length=256, unique=True),
        ),
    ]
