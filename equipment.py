from dataclasses import dataclass
from typing import List
from random import uniform
import marshmallow_dataclass
import marshmallow
import json


@dataclass
class Armor:
    id: int
    name: str
    defence: float
    stamina_per_turn: float


@dataclass
class Weapon:
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    @property
    def damage(self) -> float:
        return round(uniform(self.min_damage, self.max_damage), 1)


@dataclass
class EquipmentData:
    """
    содержит 2 списка - с оружием и с броней
    """
    weapons: List[Weapon]
    armors: List[Armor]


class Equipment:

    def __init__(self):
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name) -> Weapon:
        """
        возвращает объект оружия по имени
        """
        return next(filter(lambda weapon: weapon_name == weapon_name, self.equipment.weapons))

    def get_armor(self, armor_name) -> Armor:
        """
        возвращает объект брони по имени
        """
        return next(filter(lambda _: _.name == armor_name, self.equipment.armors))

    def get_weapons_names(self) -> list:
        """
        возвращаем список с оружием
        """
        return [weapon.name for weapon in self.equipment.weapons]

    def get_armors_names(self) -> list:
        """
        возвращаем список с броней
        """
        return [armor.name for armor in self.equipment.armors]

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        """
        этот метод загружает данные из json в EquipmentData
        """
        with open("./data/equipment.json", encoding='utf-8') as equipment_file:
            data = json.load(equipment_file)
        equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
        try:
            return equipment_schema().load(data)
        except marshmallow.exceptions.ValidationError:
            raise ValueError
