# Generated by Django 3.2.5 on 2021-08-05 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jokes', '0007_generators_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='generators',
            name='short_name',
            field=models.CharField(default='', max_length=50, verbose_name='Название'),
            preserve_default=False,
        ),
    ]
