# Generated by Django 3.2.19 on 2024-04-01 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_prova_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Concurso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('descricao', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='prova',
            name='concurso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.concurso'),
        ),
    ]