# Generated by Django 2.2.16 on 2021-07-25 12:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authService', '0003_delete_assignment'),
        ('classroom', '0004_submission_remarks'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='submission',
            unique_together={('assignment', 'user')},
        ),
    ]
