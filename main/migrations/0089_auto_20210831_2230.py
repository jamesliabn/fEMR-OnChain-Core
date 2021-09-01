# Generated by Django 3.2.6 on 2021-09-01 02:30

from django.db import migrations, models
import django.db.models.deletion
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0088_auto_20210831_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='ethnicity',
            field=models.ForeignKey(blank=True, default=main.models.get_nondisclosed_ethnicity, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.ethnicity'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='ethnicity_text',
            field=models.CharField(blank=True, choices=[('1', 'Hispanic or Latinx'), ('2', 'Not Hispanic or Latinx'), ('3', 'Nondisclosed')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='race',
            field=models.ForeignKey(blank=True, default=main.models.get_nondisclosed_race, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.race'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='race_text',
            field=models.CharField(blank=True, choices=[('1', 'Native American or Native Alaskan'), ('2', 'Asian'), ('3', 'Black, African American'), ('4', 'Hispanic or Latinx'), ('5', 'Mixed Race'), ('6', 'White'), ('7', 'Nondisclosed')], max_length=30, null=True),
        ),
    ]
