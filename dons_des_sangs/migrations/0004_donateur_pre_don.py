# Generated by Django 5.0.1 on 2024-02-19 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dons_des_sangs', '0003_administrateur_delete_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='donateur',
            name='pre_don',
            field=models.BooleanField(default=True),
        ),
    ]
