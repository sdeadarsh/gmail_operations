# Generated by Django 4.2.11 on 2024-03-24 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gmail_script', '0002_rename_message_mails_message_body_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mails',
            name='created_by_id',
        ),
        migrations.RemoveField(
            model_name='mails',
            name='updated_by_id',
        ),
        migrations.AlterField(
            model_name='mails',
            name='mail_tag',
            field=models.CharField(default='inbox', max_length=100),
        ),
        migrations.AlterField(
            model_name='mails',
            name='read_status',
            field=models.BooleanField(default=False),
        ),
    ]
