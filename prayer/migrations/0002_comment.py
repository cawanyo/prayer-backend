# Generated by Django 4.2.23 on 2025-06-18 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prayer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('submiter_name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('prayer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='prayer.prayer')),
            ],
        ),
    ]
