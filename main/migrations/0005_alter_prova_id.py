# Generated by Django 3.2.19 on 2024-04-01 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_avaliacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prova',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
