# Generated by Django 4.1 on 2022-08-09 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('author', models.CharField(default='알수없음', max_length=100)),
                ('publisher', models.CharField(default='알수없음', max_length=100)),
                ('price', models.IntegerField(default=0)),
            ],
        ),
    ]
