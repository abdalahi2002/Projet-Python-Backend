# Generated by Django 5.0.1 on 2024-02-12 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dons_des_sangs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='donateur',
            name='test',
            field=models.BooleanField(default=False),
        ),
    ]