# Generated by Django 4.2.4 on 2023-09-02 11:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_comment_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='basketitem',
            old_name='many',
            new_name='quantity',
        ),
    ]