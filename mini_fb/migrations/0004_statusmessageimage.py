# Generated by Django 5.1.2 on 2024-10-21 23:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mini_fb', '0003_statusmessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusMessageImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(blank=True, upload_to='')),
                ('status_message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mini_fb.statusmessage')),
            ],
        ),
    ]