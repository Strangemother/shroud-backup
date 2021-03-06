# Generated by Django 3.1.7 on 2021-03-03 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Drive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=255)),
                ('compressed', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('provider_name', models.CharField(max_length=255)),
                ('size', models.BigIntegerField()),
                ('system_name', models.CharField(max_length=255)),
                ('volume_name', models.CharField(max_length=255)),
            ],
        ),
    ]
