# Generated by Django 4.2.7 on 2024-11-03 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('set_main', '0004_bottoken_user_id_bottoken_user_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChanelGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=100)),
                ('group_id', models.BigIntegerField()),
                ('group_url', models.CharField(max_length=200)),
            ],
        ),
    ]