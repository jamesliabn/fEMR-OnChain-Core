# Generated by Django 3.2.5 on 2021-07-11 21:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0068_alter_patientencounter_body_height_primary'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='imaging_link',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.CreateModel(
            name='HistoryOfPresentIllness',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('onset', models.CharField(max_length=50)),
                ('quality', models.CharField(max_length=50)),
                ('radiation', models.CharField(max_length=50)),
                ('severity', models.CharField(max_length=50)),
                ('provokes', models.CharField(max_length=50)),
                ('palliates', models.CharField(max_length=50)),
                ('time_of_day', models.CharField(max_length=50)),
                ('narrative', models.CharField(max_length=50)),
                ('physical_examination', models.CharField(max_length=255)),
                ('chief_complaint', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='main.chiefcomplaint')),
                ('encounter', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='main.patientencounter')),
            ],
        ),
    ]