# Generated by Django 3.1.7 on 2021-03-06 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appMR', '0006_auto_20210306_1748'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='content',
            new_name='comment',
        ),
        migrations.AddField(
            model_name='comment',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]