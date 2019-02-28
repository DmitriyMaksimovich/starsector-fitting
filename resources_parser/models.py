from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, Boolean, Text
from sqlalchemy.orm import relationship


Base = declarative_base()


class Ship(Base):
    __tablename__ = 'ships'

    ship_name = Column(String(100))
    hull_id = Column(String(100), primary_key=True)
    sprite_name = Column(String(150))
    width = Column(Float)
    height = Column(Float)
    hull_size = Column(String(50))
    style = Column(String(50))
    center = Column(String(15))
    weapon_slots = relationship("WeaponSlot", cascade="save-update, merge, delete")
    armor_rating = Column(Float)
    acceleration = Column(Float)
    field_8_6_5_4 = Column(Float)
    cargo = Column(Float)
    deceleration = Column(Float)
    flux_dissipation = Column(Float)
    fuel = Column(Float)
    fuel_ly = Column(Float)
    hitpoints = Column(Float)
    mass = Column(Float)
    max_crew = Column(Integer)
    max_flux = Column(Float)
    max_speed = Column(Float)
    max_turn_rate = Column(Float)
    min_crew = Column(Integer)
    ordnance_points = Column(Integer)
    shield_arc= Column(Float)
    shield_efficiency = Column(Float)
    shield_type = Column(String(20))
    shield_upkeep = Column(Float)
    supplies_month = Column(Float)
    description = Column(Text)
    mod_name = Column(String(50))

    def __repr__(self):
        return "<Ship(ship_name={})>".format(self.ship_name)


class WeaponSlot(Base):
    __tablename__ = 'weapon_slots'

    id = Column(Integer, primary_key=True)
    slot_id = Column(String(30))
    angle = Column(Float)
    arc = Column(Float)
    mount = Column(String(10))
    size = Column(String(15))
    slot_type = Column(String(15))
    location = Column(String(80))
    ship_name = Column(String(100), ForeignKey('ships.hull_id'))
    weapon = Column(String(50), ForeignKey('weapons.weapon_id'), nullable=True)

    def __repr__(self):
        return "<WeaponSlot(id={}, for ship_name={})>".format(self.id, self.ship_name)


class Weapon(Base):
    __tablename__ = 'weapons'

    weapon_id = Column(String(50), primary_key=True)
    weapon_name = Column(String(50))
    ops = Column(Integer)
    ammo = Column(Integer)
    ammo_sec = Column(Float)
    autocharge = Column(Boolean)
    requires_full_charge = Column(Boolean)
    burst_size = Column(Float)
    damage_sec = Column(Float)
    damage_shot = Column(Float)
    emp = Column(Float)
    energy_second = Column(Float)
    energy_shot = Column(Float)
    hardpoint_sprite = Column(String(100))
    weapon_range = Column(Float)
    size = Column(String(10))
    spec_class = Column(String(15))
    turn_rate = Column(Integer)
    turret_sprite = Column(String(100))
    proj_speed = Column(Integer)
    weapon_type = Column(String(15))
    description = Column(Text)
    mod_name = Column(String(50))

    def __repr__(self):
        return "<Weapon(id={}, name={})>".format(self.weapon_id, self.weapon_name)


def create_models(engine):
    Base.metadata.create_all(engine)
