# Generated by Django 2.2.16 on 2021-07-25 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0003_submission'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='remarks',
            field=models.CharField(default=1, max_length=2000),
            preserve_default=False,
        ),
    ]
