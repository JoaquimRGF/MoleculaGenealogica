# Generated by Django 2.2.4 on 2019-08-02 17:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pessoa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_modificacao', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Uniao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_modificacao', models.DateTimeField(auto_now=True)),
                ('data_inicio', models.DateField(default='1900-01-01')),
                ('data_final', models.DateField(default='2900-01-01')),
                ('pessoa_dois', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pessoa_dois_de', to='rest_api.Pessoa')),
                ('pessoa_um', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pessoa_um_de', to='rest_api.Pessoa')),
            ],
        ),
        migrations.CreateModel(
            name='Familia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_modificacao', models.DateTimeField(auto_now=True)),
                ('filhos', models.ManyToManyField(to='rest_api.Pessoa')),
                ('uniao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest_api.Uniao')),
            ],
        ),
    ]