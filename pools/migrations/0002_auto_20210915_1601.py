# Generated by Django 2.2.1 on 2021-09-15 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pools', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='text',
            new_name='text_q',
        ),
    ]