# Generated by Django 2.0.7 on 2018-07-29 21:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("blog", "0007_auto_20180726_2130")]

    operations = [
        migrations.RemoveField(model_name="reaction", name="post"),
        migrations.DeleteModel(name="Reaction"),
    ]
