# Generated by Django 3.1.12 on 2021-06-21 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0003_auto_20210621_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='images/%Y/%m/%d'),
        ),
    ]