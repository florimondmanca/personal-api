# Generated by Django 2.0.7 on 2018-09-22 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("blog", "0011_post_tags")]

    operations = [
        migrations.AddField(
            model_name="post",
            name="modified",
            field=models.DateTimeField(auto_now=True),
        )
    ]
