# Generated by Django 2.1.7 on 2019-03-19 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webscrap', '0002_auto_20190319_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='url',
            field=models.URLField(),
        ),
    ]
