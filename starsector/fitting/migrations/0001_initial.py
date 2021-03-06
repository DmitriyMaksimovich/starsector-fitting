# Generated by Django 2.1.7 on 2019-02-25 13:19

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fitting',
            fields=[
                ('variant_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('flux_capacitors', models.IntegerField()),
                ('flux_vents', models.IntegerField()),
                ('weapon_groups', django.contrib.postgres.fields.jsonb.JSONField()),
                ('goal_variant', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='HullMod',
            fields=[
                ('mod_name', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Ships',
            fields=[
                ('ship_name', models.CharField(max_length=100)),
                ('hull_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('sprite_name', models.CharField(blank=True, max_length=150, null=True)),
                ('width', models.FloatField(blank=True, null=True)),
                ('height', models.FloatField(blank=True, null=True)),
                ('hull_size', models.CharField(blank=True, max_length=50, null=True)),
                ('style', models.CharField(blank=True, max_length=50, null=True)),
                ('center', models.CharField(blank=True, max_length=15, null=True)),
                ('armor_rating', models.FloatField(blank=True, null=True)),
                ('acceleration', models.FloatField(blank=True, null=True)),
                ('field_8_6_5_4', models.FloatField(blank=True, null=True)),
                ('cargo', models.FloatField(blank=True, null=True)),
                ('deceleration', models.FloatField(blank=True, null=True)),
                ('flux_dissipation', models.FloatField(blank=True, null=True)),
                ('fuel', models.FloatField(blank=True, null=True)),
                ('fuel_ly', models.FloatField(blank=True, null=True)),
                ('hitpoints', models.FloatField(blank=True, null=True)),
                ('mass', models.FloatField(blank=True, null=True)),
                ('max_crew', models.IntegerField(blank=True, null=True)),
                ('max_flux', models.FloatField(blank=True, null=True)),
                ('max_speed', models.FloatField(blank=True, null=True)),
                ('max_turn_rate', models.FloatField(blank=True, null=True)),
                ('min_crew', models.IntegerField(blank=True, null=True)),
                ('ordnance_points', models.IntegerField(blank=True, null=True)),
                ('shield_arc', models.FloatField(blank=True, null=True)),
                ('shield_efficiency', models.FloatField(blank=True, null=True)),
                ('shield_type', models.CharField(blank=True, max_length=20, null=True)),
                ('shield_upkeep', models.FloatField(blank=True, null=True)),
                ('supplies_month', models.FloatField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('mod_name', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'ship',
                'verbose_name_plural': 'ships',
                'db_table': 'ships',
            },
        ),
        migrations.CreateModel(
            name='Weapons',
            fields=[
                ('weapon_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('weapon_name', models.CharField(blank=True, max_length=50, null=True)),
                ('ops', models.IntegerField(blank=True, null=True)),
                ('ammo', models.IntegerField(blank=True, null=True)),
                ('ammo_sec', models.FloatField(blank=True, null=True)),
                ('autocharge', models.BooleanField(blank=True, null=True)),
                ('requires_full_charge', models.BooleanField(blank=True, null=True)),
                ('burst_size', models.FloatField(blank=True, null=True)),
                ('damage_sec', models.FloatField(blank=True, null=True)),
                ('damage_shot', models.FloatField(blank=True, null=True)),
                ('emp', models.FloatField(blank=True, null=True)),
                ('energy_second', models.FloatField(blank=True, null=True)),
                ('energy_shot', models.FloatField(blank=True, null=True)),
                ('hardpoint_sprite', models.CharField(blank=True, max_length=100, null=True)),
                ('weapon_range', models.FloatField(blank=True, null=True)),
                ('size', models.CharField(blank=True, max_length=10, null=True)),
                ('spec_class', models.CharField(blank=True, max_length=15, null=True)),
                ('turn_rate', models.IntegerField(blank=True, null=True)),
                ('turret_sprite', models.CharField(blank=True, max_length=100, null=True)),
                ('proj_speed', models.IntegerField(blank=True, null=True)),
                ('weapon_type', models.CharField(blank=True, max_length=15, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('mod_name', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'weapon',
                'verbose_name_plural': 'weapons',
                'db_table': 'weapons',
            },
        ),
        migrations.CreateModel(
            name='WeaponSlots',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot_id', models.CharField(blank=True, max_length=30, null=True)),
                ('angle', models.FloatField(blank=True, null=True)),
                ('arc', models.FloatField(blank=True, null=True)),
                ('mount', models.CharField(blank=True, max_length=10, null=True)),
                ('size', models.CharField(blank=True, max_length=15, null=True)),
                ('slot_type', models.CharField(blank=True, max_length=15, null=True)),
                ('location', models.CharField(blank=True, max_length=80, null=True)),
                ('ship_name', models.ForeignKey(blank=True, db_column='ship_name', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='weapon_slots', to='fitting.Ships')),
                ('weapon', models.ForeignKey(blank=True, db_column='weapon', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='fitting.Weapons')),
            ],
            options={
                'verbose_name': 'weapon_slot',
                'verbose_name_plural': 'weapon_slots',
                'db_table': 'weapon_slots',
            },
        ),
        migrations.AddField(
            model_name='fitting',
            name='hull_id',
            field=models.ForeignKey(db_column='hull_id', on_delete=django.db.models.deletion.CASCADE, to='fitting.Ships'),
        ),
        migrations.AddField(
            model_name='fitting',
            name='hull_mods',
            field=models.ManyToManyField(blank=True, related_name='fit', to='fitting.HullMod'),
        ),
        migrations.AddField(
            model_name='fitting',
            name='permament_mods',
            field=models.ManyToManyField(blank=True, related_name='permament', to='fitting.HullMod'),
        ),
    ]
