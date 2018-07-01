# Generated by Django 2.0.6 on 2018-07-01 16:07

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
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('red_score', models.IntegerField()),
                ('submission_timestamp', models.DateTimeField()),
                ('ian_watched', models.BooleanField(default=False)),
                ('forced_team_selection', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Glider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='HandicapSnapshot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mario_stats.Game')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('handicap', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField()),
                ('red_team', models.BooleanField()),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mario_stats.Character')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mario_stats.Game')),
                ('glider', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mario_stats.Glider')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mario_stats.Person')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerHandicapSnapshot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('handicap', models.DecimalField(decimal_places=2, max_digits=4)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mario_stats.Person')),
                ('snapshot', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mario_stats.HandicapSnapshot')),
            ],
        ),
        migrations.CreateModel(
            name='StatDifference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('speed', models.DecimalField(decimal_places=2, max_digits=4)),
                ('acceleration', models.DecimalField(decimal_places=2, max_digits=4)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=4)),
                ('handling', models.DecimalField(decimal_places=2, max_digits=4)),
                ('grip', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='Tyre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('stat_difference', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mario_stats.StatDifference')),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('stat_difference', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mario_stats.StatDifference')),
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
            name='WeightClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('stat_difference', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mario_stats.StatDifference')),
            ],
        ),
        migrations.AddField(
            model_name='vehicle',
            name='vehicle_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mario_stats.VehicleClass'),
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
            model_name='glider',
            name='stat_difference',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mario_stats.StatDifference'),
        ),
        migrations.AddField(
            model_name='character',
            name='weight_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mario_stats.WeightClass'),
        ),
    ]
