# Generated by Django 5.1.5 on 2025-02-09 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('name_ru', models.CharField(max_length=200, null=True)),
                ('name_uz', models.CharField(max_length=200, null=True)),
                ('name_en', models.CharField(max_length=200, null=True)),
                ('slug', models.SlugField(max_length=250)),
                ('slug_ru', models.SlugField(max_length=250, null=True)),
                ('slug_uz', models.SlugField(max_length=250, null=True)),
                ('slug_en', models.SlugField(max_length=250, null=True)),
                ('description', models.TextField()),
                ('description_ru', models.TextField(null=True)),
                ('description_uz', models.TextField(null=True)),
                ('description_en', models.TextField(null=True)),
            ],
        ),
    ]
