# Generated by Django 5.1.6 on 2025-03-02 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laundry', '0005_remove_userprofile_unique_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
