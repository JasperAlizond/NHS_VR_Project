# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-27 15:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, verbose_name='Project Title')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.IntegerField(verbose_name='X Position')),
                ('y', models.IntegerField(verbose_name='Y Position')),
                ('width', models.IntegerField(verbose_name='Tag Width')),
                ('height', models.IntegerField(verbose_name='Tag Height')),
                ('time_start', models.IntegerField(verbose_name='Time Start')),
                ('time_end', models.IntegerField(verbose_name='Time End')),
                ('remote', models.BooleanField(verbose_name='Remote?')),
                ('local_content', models.TextField(blank=True, verbose_name='Local Content')),
                ('remote_url', models.CharField(blank=True, max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, verbose_name='Title')),
                ('uploaded_video', models.FileField(upload_to='videos/', verbose_name='Video File')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tagger.Project')),
            ],
        ),
        migrations.AddField(
            model_name='tag',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tagger.Video'),
        ),
    ]
