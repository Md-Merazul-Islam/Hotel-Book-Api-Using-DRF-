# Generated by Django 5.0.4 on 2024-06-25 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_deposit'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='account/images'),
        ),
    ]