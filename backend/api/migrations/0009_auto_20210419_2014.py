# Generated by Django 3.2 on 2021-04-19 23:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_consulta_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='consulta',
            options={'ordering': ['agenda__dia', 'horario']},
        ),
        migrations.RemoveField(
            model_name='consulta',
            name='dia',
        ),
        migrations.RemoveField(
            model_name='consulta',
            name='medico',
        ),
    ]
