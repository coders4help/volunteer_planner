# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    replaces = [(b'blueprint', '0001_initial'), (b'blueprint', '0002_needblueprint_slots'), (b'blueprint', '0003_auto_20151006_1341'), (b'blueprint', '0003_auto_20151003_2033'), (b'blueprint', '0004_merge'), (b'blueprint', '0005_demolish_blueprints')]

    dependencies = [
        ('scheduler', '0009_auto_20150823_1546'),
        ('organizations', '0002_migrate_locations_to_facilities'),
    ]

    operations = [
        migrations.CreateModel(
            name='BluePrintCreator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name=b'Name der Vorlage')),
                ('location', models.ForeignKey(verbose_name=b'Ort', to='scheduler.Location')),
            ],
            options={
                'verbose_name': 'Vorlage',
                'verbose_name_plural': 'Vorlagen',
            },
        ),
        migrations.CreateModel(
            name='NeedBluePrint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_time', models.CharField(max_length=5, verbose_name=b'Uhrzeit von')),
                ('to_time', models.CharField(max_length=5, verbose_name=b'Uhrzeit bis')),
                ('topic', models.ForeignKey(verbose_name=b'Hilfetyp', to='scheduler.Topics')),
                ('slots', models.IntegerField(default=4, verbose_name=b'Anz. benoetigter Freiwillige')),
            ],
            options={
                'verbose_name': 'Schicht Vorlage',
                'verbose_name_plural': 'Schicht Vorlagen',
            },
        ),
        migrations.AddField(
            model_name='blueprintcreator',
            name='needs',
            field=models.ManyToManyField(to=b'blueprint.NeedBluePrint', verbose_name=b'Schichten'),
        ),
        migrations.AlterModelOptions(
            name='blueprintcreator',
            options={'verbose_name': 'Blueprint', 'verbose_name_plural': 'Blueprints'},
        ),
        migrations.AlterModelOptions(
            name='needblueprint',
            options={'verbose_name': 'Blueprint Item', 'verbose_name_plural': 'Blueprint Items'},
        ),
        migrations.RenameField(
            model_name='blueprintcreator',
            old_name='location',
            new_name='facility',
        ),
        migrations.RemoveField(
            model_name='blueprintcreator',
            name='facility',
        ),
        migrations.RemoveField(
            model_name='blueprintcreator',
            name='needs',
        ),
        migrations.AlterField(
            model_name='blueprintcreator',
            name='title',
            field=models.CharField(max_length=255, verbose_name='blueprint title'),
        ),
        migrations.AlterField(
            model_name='needblueprint',
            name='from_time',
            field=models.CharField(max_length=5, verbose_name='from hh:mm'),
        ),
        migrations.AlterField(
            model_name='needblueprint',
            name='slots',
            field=models.IntegerField(verbose_name='number of volunteers needed'),
        ),
        migrations.AlterField(
            model_name='needblueprint',
            name='to_time',
            field=models.CharField(max_length=5, verbose_name='until hh:mm'),
        ),
        migrations.RemoveField(
            model_name='needblueprint',
            name='topic',
        ),
        migrations.DeleteModel(
            name='BluePrintCreator',
        ),
        migrations.DeleteModel(
            name='NeedBluePrint',
        ),
    ]
