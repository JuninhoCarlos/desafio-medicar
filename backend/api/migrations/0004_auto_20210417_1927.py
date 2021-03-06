# Generated by Django 3.2 on 2021-04-17 22:27

import api.validations
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20210417_0934'),
    ]

    operations = [
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horario', models.TimeField()),
            ],
            options={
                'ordering': ['horario'],
            },
        ),
        migrations.AlterField(
            model_name='agenda',
            name='dia',
            field=models.DateField(validators=[api.validations.no_past]),
        ),
        migrations.RemoveField(
            model_name='agenda',
            name='horarios',
        ),
        migrations.AddField(
            model_name='agenda',
            name='horarios',
            field=models.ManyToManyField(to='api.Horario'),
        ),
    ]
