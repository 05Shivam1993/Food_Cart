# Generated by Django 2.0 on 2020-06-27 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FoodApp', '0007_auto_20200624_0122'),
    ]

    operations = [
        migrations.CreateModel(
            name='Offers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupons', models.CharField(max_length=20)),
            ],
        ),
    ]