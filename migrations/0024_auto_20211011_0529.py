# Generated by Django 3.2 on 2021-10-11 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacatalog', '0023_auto_20210201_2349'),
    ]

    operations = [
        migrations.AddField(
            model_name='datauseagreement',
            name='public',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='dataset',
            name='access_requirements',
        ),
        migrations.AddField(
            model_name='dataset',
            name='access_requirements',
            field=models.ManyToManyField(blank=True, to='datacatalog.DataAccess'),
        ),
        migrations.RemoveField(
            model_name='datauseagreement',
            name='access_requirements',
        ),
        migrations.AddField(
            model_name='datauseagreement',
            name='access_requirements',
            field=models.ManyToManyField(blank=True, to='datacatalog.DataAccess'),
        ),
    ]
