# Generated by Django 3.1.7 on 2021-03-08 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tagging', '0002_auto_20210308_0355'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='bulk_id',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]