from rest_framework import serializers
from fitting.models import Ships


class ShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ships
        fields = '__all__'
        read_only_fields = [
            'ship_name',
            'hull_id',
            'sprite_name',
            'width',
            'height',
            'hull',
            'style',
            'center',
            'armor',
            'acceleration',
            'field',
            'cargo',
            'deceleration',
            'flux',
            'fuel',
            'fuel',
            'hitpoints',
            'mass',
            'max',
            'max',
            'max',
            'max',
            'min',
            'ordnance',
            'shield',
            'shield',
            'shield',
            'shield',
            'supplie'
        ]
