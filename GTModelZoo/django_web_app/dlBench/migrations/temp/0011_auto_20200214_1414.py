# Generated by Django 2.2 on 2020-02-14 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20200213_2040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performancemetrics',
            name='accuracy_or_utilization',
            field=models.FloatField(),
        ),
    ]
