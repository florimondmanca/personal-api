# Generated by Django 2.1.2 on 2018-10-20 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("blog", "0018_remove_post_tags")]

    operations = [
        migrations.AlterField(
            model_name="tag",
            name="posts",
            field=models.ManyToManyField(related_name="tags", to="blog.Post"),
        )
    ]
