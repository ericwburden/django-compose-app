# Generated by Django 3.0.4 on 2020-04-01 19:06

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import dtd_request.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(unique=True)),
                ('label', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('contact', models.CharField(help_text='First Last', max_length=200, verbose_name='Your Name')),
                ('email', models.EmailField(blank=True, max_length=200, null=True, verbose_name='Your Email Address')),
                ('primary_phone', models.CharField(blank=True, help_text='###-###-####', max_length=17, null=True, validators=[django.core.validators.RegexValidator('^\\+?1?\\d{9,15}$')], verbose_name='Phone number where you can be reached')),
                ('secondary_phone', models.CharField(blank=True, help_text='###-###-####', max_length=17, null=True, validators=[django.core.validators.RegexValidator('^\\+?1?\\d{9,15}$')], verbose_name='Backup phone number')),
                ('domain_score', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)])),
                ('add_info', models.TextField(help_text="Share anything else you'd like for us to know", verbose_name='Please provide any additional information here')),
                ('type_of_need', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dtd_request.Domain', verbose_name='What kind of help are you looking for?')),
                ('confirmation_code', models.CharField(default=dtd_request.models.short_code, max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('RECEIVED', 'Received'), ('REVIEWED', 'Under Review'), ('CONTACTED', 'Contact Pending'), ('REFERRED', 'Referred'), ('CLOSED', 'Closed')], max_length=9)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='response_created_by', to=settings.AUTH_USER_MODEL)),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dtd_request.Request')),
            ],
        ),
        migrations.CreateModel(
            name='DomainAssessment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('description', models.TextField()),
                ('domain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dtd_request.Domain')),
            ],
        ),
    ]
