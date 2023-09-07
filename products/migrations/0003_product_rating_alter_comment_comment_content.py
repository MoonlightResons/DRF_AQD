# Generated by Django 4.2.4 on 2023-09-01 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='rating',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=3),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_content',
            field=models.TextField(null=True),
        ),
    ]