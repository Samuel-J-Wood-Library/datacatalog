# Generated by Django 3.2 on 2021-10-20 23:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('datacatalog', '0025_auto_20211011_0709'),
    ]

    operations = [
        migrations.CreateModel(
            name='RetentionRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_creation', models.DateField(auto_now_add=True)),
                ('record_update', models.DateField(auto_now=True)),
                ('name', models.CharField(max_length=256, verbose_name='Short description')),
                ('milestone', models.CharField(choices=[('PU', 'Publication'), ('CO', 'Project/Grant completion'), ('TR', 'Leaving Weill Cornell Medicine'), ('PR', 'Private backup'), ('OT', 'Other')], default='CO', max_length=2)),
                ('comments', models.TextField(blank=True, null=True)),
                ('ticket', models.CharField(max_length=32)),
                ('record_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('to_archive', models.ManyToManyField(related_name='retention_requests', to='datacatalog.DataAccess')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_creation', models.DateField(auto_now_add=True)),
                ('record_update', models.DateField(auto_now=True)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('sponsor', models.CharField(blank=True, max_length=128, null=True)),
                ('funding_id', models.CharField(blank=True, max_length=64, null=True)),
                ('completion', models.DateField(blank=True, null=True)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='admin_person', to='persons.person')),
                ('pi', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='pi_project_person', to='persons.person')),
                ('record_author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='record_author', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]