# Generated by Django 3.2.7 on 2021-10-03 03:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bike', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bike',
            name='need_repair',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='bike',
            name='available',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='bike',
            name='unique',
            field=models.CharField(default='0d8ddaaedea6', max_length=12, unique=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='unique',
            field=models.CharField(default='bb36c528', max_length=8, unique=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='record',
            name='unique',
            field=models.CharField(default='79f2dca47ab54530b8d3e7434d3d12c3', max_length=16, unique=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='finish_time',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='unique',
            field=models.CharField(default='6fb520db67b94594b314a254bffa2341', max_length=16, unique=True, verbose_name='ID'),
        ),
    ]
