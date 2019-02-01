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
    center = Column(String(20))
    weapon_slots = relationship("WeaponSlot")
    builtInMods = relationship("HullMod", secondary=hull_mods_association_table)
    builtInWings = relationship("Wing", secondary=wings_association_table)
    builtInWeapons = relationship("Weapon", secondary=weapons_association_table)

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


class Wing(Base):
    __tablename__ = 'wings'

    id = Column(Integer, primary_key=True)
    wing_name = Column(String(100))

    def __repr__(self):
        return "<Wing(id={}, name={})>".format(self.id, self.wing)


class HullMod(Base):
    __tablename__ = 'hull_mods'

    id = Column(Integer, primary_key=True)
    hull_mod_name = Column(String(100))

    def __repr__(self):
        return "<HullMod(id={}, name={})>".format(self.id, self.hull_mod_name)


def create_models(engine):
    Base.metadata.create_all(engine)
