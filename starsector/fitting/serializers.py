from rest_framework import serializers
from fitting.models import Ships, WeaponSlots, Weapons, Fitting


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


class WeaponSlotsSerializer(serializers.ModelSerializer):
    weapon = WeaponSerializer(many=False, read_only=True)

    class Meta:
        model = WeaponSlots
        fields = '__all__'
        read_only_fields = [
            'id',
            'slot_id',
            'angle',
            'arc',
            'mount',
            'size',
            'slot_type',
            'location',
            'ship_name',
            'weapon'
        ]


class ShipSerializer(serializers.ModelSerializer):
    weapon_slots = WeaponSlotsSerializer(many=True, read_only=True)

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
            'hitpoints',
            'mass',
            'max_crew',
            'max_flux',
            'max_speed',
            'max_turn_rate',
            'min_crew',
            'ordnance_points',
            'shield_arc',
            'shield_efficiency',
            'shield_type',
            'shield_upkeep',
            'supplies_month',
            'description',
            'mod_name'
        ]


class FittingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fitting
        fields = '__all__'
