# Generated by Django 3.1.6 on 2021-02-05 02:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('constructionapp', '0003_auto_20210204_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='constructionapp.product'),
        ),
    ]
