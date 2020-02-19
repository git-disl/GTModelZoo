# Generated by Django 2.2 on 2020-02-04 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20200203_0311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='data_model_file',
            field=models.FileField(blank=True, null=True, upload_to='Data_Set_Files'),
        ),
        migrations.AlterField(
            model_name='dlmodel',
            name='model_file',
            field=models.FileField(blank=True, null=True, upload_to='DL_Model_Files'),
        ),
    ]
