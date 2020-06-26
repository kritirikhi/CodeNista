# Generated by Django 3.0.7 on 2020-06-23 05:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0006_post_views'),
    ]

    operations = [
        migrations.CreateModel(
            name='bookmark',
            fields=[
                ('booksno', models.AutoField(primary_key=True, serialize=False)),
                ('postsno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]