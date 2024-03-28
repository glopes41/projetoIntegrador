# Generated by Django 3.2.19 on 2024-03-25 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidato',
            fields=[
                ('idCandidato', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(db_index=True, max_length=100)),
                ('aprovado', models.BooleanField()),
                ('habilitado', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Examinador',
            fields=[
                ('idExaminador', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(db_index=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Tipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idTipo', models.BigIntegerField()),
                ('peso', models.DecimalField(decimal_places=2, max_digits=5)),
                ('descricao', models.CharField(db_index=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Prova',
            fields=[
                ('idProva', models.AutoField(primary_key=True, serialize=False)),
                ('idConcurso', models.BigIntegerField()),
                ('numTipo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tipos', to='main.tipo')),
            ],
        ),
        migrations.CreateModel(
            name='Avaliacao',
            fields=[
                ('idAvaliacao', models.AutoField(primary_key=True, serialize=False)),
                ('nota', models.DecimalField(decimal_places=2, max_digits=4)),
                ('data', models.DateField()),
                ('numAvaliacao', models.ManyToManyField(to='main.Examinador')),
                ('numCandidato', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='candidatos', to='main.candidato')),
                ('numProva', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='provas', to='main.prova')),
            ],
        ),
    ]