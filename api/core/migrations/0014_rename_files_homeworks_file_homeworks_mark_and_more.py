# Generated by Django 4.1.4 on 2023-05-13 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_homeworks'),
    ]

    operations = [
        migrations.RenameField(
            model_name='homeworks',
            old_name='files',
            new_name='file',
        ),
        migrations.AddField(
            model_name='homeworks',
            name='mark',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='homeworks',
            name='teacher_comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
