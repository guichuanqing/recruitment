# Generated by Django 4.1 on 2022-11-16 10:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("interview", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="candidate",
            name="second_professional_competency",
        ),
    ]
