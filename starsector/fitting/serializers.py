from rest_framework import serializers
from fitting.models import Ships, Weapons, Fitting


class WeaponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weapons
        fields = '__all__'
        read_only_fields = [
            'weapon_id',
            'weapon_name',
            'ops',
            'ammo',
            'ammo_sec',
            'autocharge',
            'requires_full_charge',
            'burst_size',
            'damage_sec',
            'damage_shot',
            'emp',
            'energy_second',
            'energy_shot',
            'hardpoint_sprite',
            'weapon_range',
            'size',
            'spec_class',
            'turn_rate',
            'turret_sprite',
            'proj_speed',
            'weapon_type',
            'description',
            'mod_name'
        ]



class ShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ships
        ordering = ('ship_name',)
        fields = '__all__'
        read_only_fields = [
            'ship_name',
            'hull_id',
            'sprite_name',
            'width',
            'height',
            'hull_size',
            'style',
            'center',
            'weapon_slots',
            'armor_rating',
            'acceleration',
            'field_8_6_5_4',
            'cargo',
            'deceleration',
            'flux_dissipation',
            'fuel',
            'fuel_ly',
            'fighter_bays',
            'hitpoints',
            'mass',
            'max_crew',
            'max_flux',
            'max_speed',
            'max_burn',
            'max_turn_rate',
            'min_crew',
            'ordnance_points',
            'shield_arc',
            'shield_efficiency',
            'shield_type',
            'shield_upkeep',
            'supplies_month',
            'mod_name',
            'weapon_slots',
            'description'
        ]


class FittingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fitting
        fields = '__all__'
