# Generated by Django 4.1 on 2022-11-16 11:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("interview", "0004_candidate_creator_candidate_hr_advantage_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="candidate",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="创建时间",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="candidate",
            name="modified_date",
            field=models.DateTimeField(auto_now=True, null=True, verbose_name="更新时间"),
        ),
    ]
