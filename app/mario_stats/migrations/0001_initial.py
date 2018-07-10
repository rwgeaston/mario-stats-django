# Generated by Django 2.0.6 on 2018-07-10 06:34

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('red_score', models.IntegerField(blank=True, null=True)),
                ('creation_timestamp', models.DateTimeField(default=datetime.datetime.now)),
                ('submission_timestamp', models.DateTimeField(blank=True, null=True)),
                ('ian_watched', models.BooleanField(default=False)),
                ('forced_team_selection', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='HandicapSnapshot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='handicap_snapshot', to='mario_stats.Game')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('handicap', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_position', models.IntegerField()),
                ('red_team', models.BooleanField()),
                ('outcome', models.IntegerField(choices=[(1, 'won'), (2, 'lost'), (3, 'draw'), (4, 'not played')], default=4)),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mario_stats.Character')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='players', to='mario_stats.Game')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mario_stats.Person')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerHandicapSnapshot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('handicap', models.DecimalField(decimal_places=2, max_digits=4)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mario_stats.Person')),
                ('snapshot', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='players', to='mario_stats.HandicapSnapshot')),
            ],
        ),
        migrations.CreateModel(
            name='VehicleClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_type', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='VehicleComponent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('speed', models.DecimalField(decimal_places=2, max_digits=4)),
                ('acceleration', models.DecimalField(decimal_places=2, max_digits=4)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=4)),
                ('handling', models.DecimalField(decimal_places=2, max_digits=4)),
                ('grip', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='Glider',
            fields=[
                ('vehiclecomponent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='mario_stats.VehicleComponent')),
            ],
            bases=('mario_stats.vehiclecomponent',),
        ),
        migrations.CreateModel(
            name='Tyre',
            fields=[
                ('vehiclecomponent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='mario_stats.VehicleComponent')),
            ],
            bases=('mario_stats.vehiclecomponent',),
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('vehiclecomponent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='mario_stats.VehicleComponent')),
                ('vehicle_class', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mario_stats.VehicleClass')),
            ],
            bases=('mario_stats.vehiclecomponent',),
        ),
        migrations.CreateModel(
            name='WeightClass',
            fields=[
                ('vehiclecomponent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='mario_stats.VehicleComponent')),
            ],
            bases=('mario_stats.vehiclecomponent',),
        ),
        migrations.AddField(
            model_name='player',
            name='glider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mario_stats.Glider'),
        ),
        migrations.AddField(
            model_name='player',
            name='tyres',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mario_stats.Tyre'),
        ),
        migrations.AddField(
            model_name='player',
            name='vehicle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mario_stats.Vehicle'),
        ),
        migrations.AddField(
            model_name='character',
            name='weight_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mario_stats.WeightClass'),
        ),
    ]
