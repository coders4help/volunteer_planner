# Generated by Django 2.0.5 on 2019-07-18 22:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0002_auto_20150926_2313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='region',
            field=models.ForeignKey(related_name='areas', to='places.Region',
                                    verbose_name='region',
                                    on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='place',
            name='area',
            field=models.ForeignKey(related_name='places', to='places.Area',
                                    verbose_name='area',
                                    on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='region',
            name='country',
            field=models.ForeignKey(related_name='regions', to='places.Country',
                                    verbose_name='country',
                                    on_delete=django.db.models.deletion.PROTECT),
        ),
    ]