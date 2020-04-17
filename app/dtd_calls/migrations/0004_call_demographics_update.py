# Generated by Django 3.0.4 on 2020-04-17 22:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dtd_calls', '0003_call_call_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Agency Name')),
            ],
            options={
                'verbose_name_plural': 'Agencies',
                'ordering': ['-pk'],
            },
        ),
        migrations.AddField(
            model_name='call',
            name='caller_address',
            field=models.CharField(max_length=256, null=True, verbose_name='Caller Street Address'),
        ),
        migrations.AddField(
            model_name='call',
            name='caller_age',
            field=models.IntegerField(null=True, verbose_name='Caller Age'),
        ),
        migrations.AddField(
            model_name='call',
            name='caller_city',
            field=models.CharField(max_length=256, null=True, verbose_name='Caller City'),
        ),
        migrations.AddField(
            model_name='call',
            name='caller_email',
            field=models.EmailField(max_length=254, null=True, verbose_name='Caller Email Address'),
        ),
        migrations.AddField(
            model_name='call',
            name='caller_gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1, null=True, verbose_name='Caller Gender'),
        ),
        migrations.AddField(
            model_name='call',
            name='caller_household_size',
            field=models.IntegerField(null=True, verbose_name='Caller Household Size'),
        ),
        migrations.AddField(
            model_name='call',
            name='caller_name',
            field=models.CharField(max_length=256, null=True, verbose_name='Caller Name'),
        ),
        migrations.AddField(
            model_name='call',
            name='caller_state',
            field=models.CharField(help_text='TN', max_length=2, null=True, verbose_name='Caller State (2-Letter)'),
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.IntegerField(choices=[(1, 'Shelter/Housing'), (2, 'Employment'), (3, 'Income'), (4, 'Food and Nutrition'), (5, 'Childcare'), (6, "Children's Education"), (7, 'Adult Education'), (8, 'Healthcare'), (9, 'Life Skills'), (10, 'Family Relationships/Social Network'), (11, 'Transportation/Mobility'), (12, 'Community Involvement'), (13, 'Parenting Skills'), (14, 'Legal'), (15, 'Mental Health'), (16, 'Substance Abuse'), (17, 'Safety'), (18, 'Disability Services'), (19, 'Credit/Financial Management'), (20, 'Spirituality')], verbose_name='Service Domain(s)')),
                ('call', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dtd_calls.Call')),
            ],
        ),
        migrations.AddField(
            model_name='call',
            name='referred_agency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dtd_calls.Agency'),
        ),
    ]