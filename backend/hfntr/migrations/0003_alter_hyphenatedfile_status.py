# Generated by Django 4.0.4 on 2022-04-24 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hfntr', '0002_hyphenatedfile_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hyphenatedfile',
            name='status',
            field=models.IntegerField(choices=[(0, 'непознат'), (1, 'нов'), (2, 'у обради'), (3, 'завршен'), (4, 'грешка')], default=1),
        ),
    ]
