# Generated by Django 2.1.4 on 2018-12-12 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20181211_2039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='name',
            field=models.CharField(blank=True, help_text='用户', max_length=50, null=True, unique=True, verbose_name='用户'),
        ),
    ]