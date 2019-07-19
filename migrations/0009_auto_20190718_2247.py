# Generated by Django 2.1.4 on 2019-07-19 03:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0001_initial'),
        ('datacatalog', '0008_datauseagreement_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='expert',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='persons.Person'),
        ),
        migrations.AlterField(
            model_name='datauseagreement',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contact_person', to='persons.Person'),
        ),
        migrations.AlterField(
            model_name='datauseagreement',
            name='pi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pi_person', to='persons.Person'),
        ),
        migrations.AlterField(
            model_name='datauseagreement',
            name='users',
            field=models.ManyToManyField(to='persons.Person'),
        ),
    ]