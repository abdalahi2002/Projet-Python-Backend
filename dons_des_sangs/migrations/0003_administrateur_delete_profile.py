# Generated by Django 5.0.1 on 2024-02-13 18:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dons_des_sangs', '0002_donateur_test'),
    ]

    operations = [
        migrations.CreateModel(
            name='Administrateur',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to=settings.AUTH_USER_MODEL)),
                ('id_A', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('dons_des_sangs.user',),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]