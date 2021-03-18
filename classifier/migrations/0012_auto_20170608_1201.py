# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-08 17:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classifier', '0011_tag_approved'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='keyword',
            name='community',
        ),
        migrations.AddField(
            model_name='keyword',
            name='document',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='classifier.Document'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='keyword',
            name='rating',
            field=models.FloatField(default=1.0),
        ),
        migrations.AlterField(
            model_name='relationship',
            name='relationship_type',
            field=models.CharField(choices=[('Subject category', 'Subject category'), ('History note', 'History note'), ('Related term', 'Related term'), ('Broader term', 'Broader term'), ('Narrower term', 'Narrower term'), ('Used for', 'Used for'), ('Use', 'Use'), ('Translation', 'Translation')], default='Related term', max_length=24),
        ),
    ]