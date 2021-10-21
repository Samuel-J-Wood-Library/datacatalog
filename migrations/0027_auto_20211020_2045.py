# Generated by Django 3.2 on 2021-10-21 01:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('datacatalog', '0026_project_retentionrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataaccess',
            name='project',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.PROTECT, to='datacatalog.project'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='retentionrequest',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='datacatalog.project'),
        ),
        migrations.AlterField(
            model_name='retentionrequest',
            name='record_author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]