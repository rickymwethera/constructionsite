# Generated by Django 3.1.6 on 2021-02-04 04:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('constructionapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='complete',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200, null=True)),
                ('city', models.CharField(max_length=200, null=True)),
                ('estate', models.CharField(max_length=200, null=True)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='constructionapp.order')),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='constructionapp.profile')),
            ],
        ),
    ]
