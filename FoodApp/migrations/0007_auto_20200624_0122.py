# Generated by Django 2.0 on 2020-06-24 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FoodApp', '0006_foods_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foods',
            name='image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
