# Generated by Django 3.2 on 2021-11-02 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacatalog', '0030_retentionrequest_locked'),
    ]

    operations = [
        migrations.AddField(
            model_name='retentionrequest',
            name='milestone_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retentionrequest',
            name='verified',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='retentionrequest',
            name='locked',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
