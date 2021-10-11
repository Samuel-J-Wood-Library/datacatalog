# Generated by Django 3.2 on 2021-10-11 12:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('datacatalog', '0024_auto_20211011_0529'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataset',
            name='access_requirements',
        ),
        migrations.RemoveField(
            model_name='datauseagreement',
            name='access_requirements',
        ),
        migrations.AddField(
            model_name='dataaccess',
            name='access_instructions',
            field=models.TextField(blank=True, help_text='Any additional instructions for accessing the data', null=True),
        ),
        migrations.AddField(
            model_name='dataaccess',
            name='filepaths',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dataaccess',
            name='metadata',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.PROTECT, to='datacatalog.dataset'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dataaccess',
            name='public_data',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='dataaccess',
            name='shareable_link',
            field=models.URLField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='dataaccess',
            name='steward_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='dataaccess',
            name='unique_id',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='dataaccess',
            name='curated',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='dataaccess',
            name='name',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='dataaccess',
            name='public',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='dataaccess',
            name='published',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.CreateModel(
            name='StorageType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_creation', models.DateField(auto_now_add=True)),
                ('record_update', models.DateField(auto_now=True)),
                ('name', models.CharField(max_length=128)),
                ('archive_instructions', models.TextField(blank=True)),
                ('record_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='dataaccess',
            name='storage_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='datacatalog.storagetype'),
        ),
    ]
