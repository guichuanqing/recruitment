# Generated by Django 4.1 on 2022-11-16 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("interview", "0002_remove_candidate_second_professional_competency"),
    ]

    operations = [
        migrations.AddField(
            model_name="candidate",
            name="second_professional_competency",
            field=models.DecimalField(
                blank=True,
                decimal_places=1,
                max_digits=2,
                null=True,
                verbose_name="专业能力得分",
            ),
        ),
        migrations.AddField(
            model_name="candidate",
            name="second_pursue_of_excellence",
            field=models.DecimalField(
                blank=True,
                decimal_places=1,
                max_digits=2,
                null=True,
                verbose_name="追求卓越得分",
            ),
        ),
    ]