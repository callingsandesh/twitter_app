# Generated by Django 2.2 on 2020-07-06 05:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0004_auto_20200706_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweetlike',
            name='tweet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tweets.Tweet'),
        ),
    ]