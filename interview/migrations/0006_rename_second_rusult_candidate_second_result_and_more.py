# Generated by Django 4.1 on 2022-11-17 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("interview", "0005_candidate_created_date_candidate_modified_date"),
    ]

    operations = [
        migrations.RenameField(
            model_name="candidate",
            old_name="second_rusult",
            new_name="second_result",
        ),
        migrations.AlterField(
            model_name="candidate",
            name="degree",
            field=models.CharField(
                choices=[("本科", "本科"), ("硕士", "硕士"), ("博士", "博士")],
                max_length=135,
                verbose_name="学历",
            ),
        ),
    ]
