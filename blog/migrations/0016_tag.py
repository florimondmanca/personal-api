# Generated by Django 2.1.2 on 2018-10-20 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("blog", "0015_auto_20181008_1513")]

    operations = [
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20)),
                (
                    "posts",
                    models.ManyToManyField(related_name="tags_set", to="blog.Post"),
                ),
            ],
        )
    ]
