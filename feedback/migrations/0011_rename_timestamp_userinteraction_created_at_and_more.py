# Generated by Django 5.1.4 on 2024-12-25 10:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0010_userinteraction_feedback_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinteraction',
            old_name='timestamp',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='userinteraction',
            old_name='details',
            new_name='interaction_details',
        ),
    ]
