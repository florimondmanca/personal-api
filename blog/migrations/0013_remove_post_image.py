# Generated by Django 2.1.1 on 2018-09-23 21:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("blog", "0012_post_modified")]

    operations = [migrations.RemoveField(model_name="post", name="image")]
