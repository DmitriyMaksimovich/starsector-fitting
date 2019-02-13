from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, Table
from sqlalchemy.orm import relationship

Base = declarative_base()


hull_mods_association_table = Table('hull_mods_associations', Base.metadata,
                                    Column('ship_id', Integer, ForeignKey('ships.id')),
                                    Column('hull_mod_id', Integer, ForeignKey('hull_mods.id')))


wings_association_table = Table('wings_associations', Base.metadata,
                                Column('ship_id', Integer, ForeignKey('ships.id')),
                                Column('wing_id', Integer, ForeignKey('wings.id')))


weapons_association_table = Table('weapons_associations', Base.metadata,
                                  Column('ship_id', Integer, ForeignKey('ships.id')),
                                  Column('weapon_id', Integer, ForeignKey('weapons.id')))


class Ship(Base):
    __tablename__ = 'ships'

    id = Column(Integer, primary_key=True)
    ship_name = Column(String(100))
    sprite_name = Column(String(150))
    width = Column(Float)
    height = Column(Float)
    hull_id = Column(String(100))
    hull_size = Column(String(50))
    style = Column(String(50))
    center = Column(String(10))
    weapon_slots = relationship("WeaponSlot")
    built_in_mods = relationship("HullMod", secondary=hull_mods_association_table)
    built_in_wings = relationship("Wing", secondary=wings_association_table)
    built_in_weapons = relationship("Weapon", secondary=weapons_association_table)
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

    def __repr__(self):
        return "<Ship(id={}, name={})>".format(self.id, self.ship_name)


class WeaponSlot(Base):
    __tablename__ = 'weapon_slots'

    id = Column(Integer, primary_key=True)
    slot_info = Column(Text)
    ship_id = Column(Integer, ForeignKey("ships.id"))

    def __repr__(self):
        return "<WeaponSlot(id={}, for ship_id={})>".format(self.id, self.ship_id)


class Weapon(Base):
    __tablename__ = 'weapons'

    id = Column(Integer, primary_key=True)
    weapon_id = Column(String(30))
    spec_class = Column(String(30))
    weapon_type = Column(String(20))
    weapon_size = Column(String(20))
    turret_sprite = Column(String(150), nullable=True)
    hardpoint_sprite = Column(String(150), nullable=True)

    def __repr__(self):
        return "<Weapon(id={}, name={})>".format(self.id, self.weapon_name)


wings_hull_mods_association_table = Table('wings_hull_mods_associations', Base.metadata,
                                          Column('wing_id', Integer, ForeignKey('wings.id')),
                                          Column('hull_mod_id', Integer, ForeignKey('hull_mods.id')))


wings_weapons_association_table = Table('wings_weapons_associations', Base.metadata,
                                        Column('wing_id', Integer, ForeignKey('wings.id')),
                                        Column('weapon_id', Integer, ForeignKey('weapons.id')))


class Wing(Base):
    __tablename__ = 'wings'

    id = Column(Integer, primary_key=True)
    wing_name = Column(String(100))
    sprite_name = Column(String(150))
    width = Column(Float)
    height = Column(Float)
    hull_id = Column(String(100))
    hull_size = Column(String(50))
    style = Column(String(50))
    center = Column(String(20))
    # weapon_slots = relationship("WeaponSlot")
    builtInMods = relationship("HullMod", secondary=wings_hull_mods_association_table)
    builtInWeapons = relationship("Weapon", secondary=wings_weapons_association_table)

    def __repr__(self):
        return "<Wing(id={}, name={})>".format(self.id, self.wing_name)


class HullMod(Base):
    __tablename__ = 'hull_mods'

    id = Column(Integer, primary_key=True)
    hull_mod_name = Column(String(100))

    def __repr__(self):
        return "<HullMod(id={}, name={})>".format(self.id, self.hull_mod_name)


class ShipSystem(Base):
    __tablename__ = 'ship_systems'

    id = Column(Integer, primary_key=True)
    system_id = Column(String(20))
    system_type = Column(String(20))
    ai_type = Column(String(20))


def create_models(engine):
    Base.metadata.create_all(engine)
