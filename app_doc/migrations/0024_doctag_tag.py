# Generated by Django 2.2.12 on 2020-08-18 22:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_doc', '0023_auto_20200620_2009'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='标签名')),
                ('create_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
            },
        ),
        migrations.CreateModel(
            name='DocTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('doc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_doc.Doc')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_doc.Tag')),
            ],
            options={
                'verbose_name': '手册标签',
                'verbose_name_plural': '手册标签',
            },
        ),
    ]
