# Generated by Django 5.0.2 on 2024-05-11 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookmodule', '0004_geeksmodel_alter_movie_password'),
    ]

    operations = [
        migrations.RenameField(
            model_name='geeksmodel',
            old_name='title',
            new_name='name',
        ),
    ]