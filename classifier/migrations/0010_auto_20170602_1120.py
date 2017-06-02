# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-02 16:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('classifier', '0009_auto_20170601_1520'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('file', models.FileField(upload_to='files/documents/%Y/%m/%d/%H_%M_%S')),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('edited_date', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('website', models.URLField(blank=True)),
                ('image', models.ImageField(default='profile_images/shadow_figure.jpeg', upload_to='user_images/%Y/%m/%d')),
                ('score', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='document',
            name='user_keywords',
            field=models.CharField(help_text='Please enter your tags separated by commas.', max_length=128),
        ),
        migrations.AddField(
            model_name='document',
            name='file',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='classifier.File'),
        ),
    ]
