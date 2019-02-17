from django.db import models


class Ships(models.Model):
    ship_name = models.CharField(primary_key=True, max_length=100)
    hull_id = models.CharField(max_length=100, blank=True, null=True)
    sprite_name = models.CharField(max_length=150, blank=True, null=True)
    width = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    hull_size = models.CharField(max_length=50, blank=True, null=True)
    style = models.CharField(max_length=50, blank=True, null=True)
    center = models.CharField(max_length=10, blank=True, null=True)
    armor_rating = models.FloatField(blank=True, null=True)
    acceleration = models.FloatField(blank=True, null=True)
    field_8_6_5_4 = models.FloatField(blank=True, null=True)
    cargo = models.FloatField(blank=True, null=True)
    deceleration = models.FloatField(blank=True, null=True)
    flux_dissipation = models.FloatField(blank=True, null=True)
    fuel = models.FloatField(blank=True, null=True)
    fuel_ly = models.FloatField(blank=True, null=True)
    hitpoints = models.FloatField(blank=True, null=True)
    mass = models.FloatField(blank=True, null=True)
    max_crew = models.IntegerField(blank=True, null=True)
    max_flux = models.FloatField(blank=True, null=True)
    max_speed = models.FloatField(blank=True, null=True)
    max_turn_rate = models.FloatField(blank=True, null=True)
    min_crew = models.IntegerField(blank=True, null=True)
    ordnance_points = models.IntegerField(blank=True, null=True)
    shield_arc = models.FloatField(blank=True, null=True)
    shield_efficiency = models.FloatField(blank=True, null=True)
    shield_type = models.CharField(max_length=20, blank=True, null=True)
    shield_upkeep = models.FloatField(blank=True, null=True)
    supplies_month = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'ships'
        verbose_name = 'ship'
        verbose_name_plural = 'ships'

    def __str__(self):
        return "{}".format(self.ship_name)


class WeaponSlots(models.Model):
    slot_info = models.TextField(blank=True, null=True)
    ship_name = models.ForeignKey(Ships, models.DO_NOTHING, db_column='ship_name', blank=True, null=True)

    class Meta:
        db_table = 'weapon_slots'
        verbose_name = 'weapon_slot'
        verbose_name_plural = 'weapon_slots'

    def __str__(self):
        return "WeaponSlot {} for {}".format(self.pk, self.ship_name)
