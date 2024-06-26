# Generated by Django 3.2.19 on 2024-03-30 13:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_candidato_examinador'),
    ]

    operations = [
        migrations.CreateModel(
            name='Avaliacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota', models.DecimalField(decimal_places=2, max_digits=4)),
                ('data', models.DateField()),
                ('avaliacao', models.ManyToManyField(to='main.Examinador')),
                ('candidato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.candidato')),
                ('prova', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.prova')),
            ],
        ),
    ]
