# Generated by Django 4.0.1 on 2023-05-25 22:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('adress', models.CharField(max_length=500)),
                ('hub', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.hub')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='adress',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='', max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='latitude',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='longitude',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='RideRequest',
        ),
        migrations.AddField(
            model_name='user',
            name='company',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='main.company'),
            preserve_default=False,
        ),
    ]