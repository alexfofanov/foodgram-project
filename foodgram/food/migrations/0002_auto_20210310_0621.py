# Generated by Django 3.1.7 on 2021-03-10 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='time',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
