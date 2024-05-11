# Generated by Django 5.0.2 on 2024-05-11 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookmodule', '0005_rename_title_geeksmodel_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='geeksmodel',
            old_name='name',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='geeksmodel',
            name='password',
        ),
        migrations.AddField(
            model_name='geeksmodel',
            name='description',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
    ]
