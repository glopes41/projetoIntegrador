# Generated by Django 3.2.19 on 2024-04-01 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20240401_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concurso',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
