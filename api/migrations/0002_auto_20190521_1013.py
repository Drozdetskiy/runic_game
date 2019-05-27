# Generated by Django 2.2.1 on 2019-05-21 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='status',
            field=models.TextField(choices=[('win', 'WIN'), ('loose', 'LOOSE'), ('draw', 'DRAW')], default='win', max_length=5),
        ),
    ]