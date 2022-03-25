# Generated by Django 2.0.5 on 2019-07-18 22:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0002_rename_news_model"),
    ]

    operations = [
        migrations.AlterField(
            model_name="newsentry",
            name="facility",
            field=models.ForeignKey(
                related_name="news_entries",
                blank=True,
                to="organizations.Facility",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
            ),
        ),
        migrations.AlterField(
            model_name="newsentry",
            name="organization",
            field=models.ForeignKey(
                related_name="news_entries",
                blank=True,
                to="organizations.Organization",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
            ),
        ),
    ]
