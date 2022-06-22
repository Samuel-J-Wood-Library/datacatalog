# Generated by Django 3.2 on 2022-06-14 22:48

import datacatalog.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('datacatalog', '0039_auto_20220525_1432'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataaccess',
            name='fileupload_log',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='dataaccess',
            name='multifiles',
            field=models.FileField(blank=True, help_text='upload files directly for archiving', null=True, upload_to=datacatalog.models.multifile_directory_path),
        ),
        migrations.AlterField(
            model_name='storagetype',
            name='record_author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]