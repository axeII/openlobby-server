# Generated by Django 2.0 on 2017-12-18 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OpenIdClient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('is_shortcut', models.BooleanField(default=False)),
                ('client_id', models.CharField(max_length=255)),
                ('client_secret', models.CharField(max_length=255)),
                ('issuer', models.CharField(max_length=255)),
                ('authorization_endpoint', models.CharField(max_length=255)),
                ('token_endpoint', models.CharField(max_length=255)),
                ('userinfo_endpoint', models.CharField(max_length=255)),
            ],
        ),
    ]
