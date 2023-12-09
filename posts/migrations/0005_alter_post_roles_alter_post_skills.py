# Generated by Django 4.2 on 2023-12-09 05:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("skills", "0001_initial"),
        ("roles", "0001_initial"),
        ("posts", "0004_post_content_alter_post_is_private"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="roles",
            field=models.ManyToManyField(related_name="posts", to="roles.role"),
        ),
        migrations.AlterField(
            model_name="post",
            name="skills",
            field=models.ManyToManyField(related_name="posts", to="skills.skill"),
        ),
    ]
