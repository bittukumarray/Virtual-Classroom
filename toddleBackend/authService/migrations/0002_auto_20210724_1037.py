# Generated by Django 2.2.16 on 2021-07-24 10:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authService', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('published_at', models.DateTimeField()),
                ('deadline_at', models.DateTimeField()),
                ('description', models.CharField(max_length=1000)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher', to='authService.UserProfile')),
                ('created_for', models.ManyToManyField(related_name='students', to='authService.UserProfile')),
            ],
        ),
    ]
