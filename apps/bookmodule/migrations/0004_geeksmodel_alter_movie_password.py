# Generated by Django 5.0.2 on 2024-05-11 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookmodule', '0003_movie_delete_task'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeeksModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='movie',
            name='password',
            field=models.CharField(max_length=200),
        ),
    ]
