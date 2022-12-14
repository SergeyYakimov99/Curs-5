from __future__ import annotations
from abc import ABC
from equipment import Weapon, Armor
from classes import UnitClass
from random import uniform
from typing import Optional


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """

    def __init__(self, name: str, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = None
        self.armor = None
        self._is_skill_used = False

    @property
    def health_points(self):
        return round(self.hp, 1)

    @property
    def stamina_points(self):
        return round(self.stamina, 1)

    def equip_weapon(self, weapon: Weapon):
        """
        присваиваем нашему герою новое оружие
        """
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor):
        """
        одеваем новую броню
        """
        self.armor = armor
        return f"{self.name} экипирован броней {self.armor.name}"

    def _count_damage(self, target: BaseUnit) -> float:
        """
         логика расчета урона игрока, логика расчета брони цели,
         уменьшение выносливости атакующего при ударе
         и уменьшение выносливости защищающегося при использовании брони
        """
        self.stamina -= self.weapon.stamina_per_hit
        unit_damage = self.weapon.damage * self.unit_class.attack

        if target.stamina > target.armor.stamina_per_turn:
            target_armor = target.armor.defence * target.unit_class.armor
            target.stamina -= target.armor.stamina_per_turn
        else:
            target_armor = 0

        damage = unit_damage - target_armor
        target.get_damage(damage)
        return round(damage, 1)

    def get_damage(self, damage: int) -> Optional[int]:
        """
        получение урона целью, даем новое значение для аттрибута self.hp
        """
        if damage > 0:
            self.hp -= damage
            return round(damage, 1)
        return 0

    def hit(self, target: BaseUnit) -> str:
        """
        функция удар игрока,
        здесь происходит проверка достаточно ли выносливости для нанесения удара.
        """
        if self.stamina >= self.weapon.stamina_per_hit:
            damage = self._count_damage(target)
            if damage > 0:
                return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {damage} урона."
            else:
                return f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперник его останавливает."
        else:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

    def use_skill(self, target: BaseUnit) -> str:
        """
        метод использования умения.
        """
        if self._is_skill_used:
            return "Навык уже использован"
        else:
            if self.unit_class.skill._is_stamina_enough:
                self._is_skill_used = True
            return self.unit_class.skill.use(user=self, target=target)

    def add_stamina(self, stamina_point: float):
        stamina_growth = stamina_point * self.unit_class.stamina
        if self.stamina + stamina_growth > self.unit_class.max_stamina:
            self.stamina = self.unit_class.max_stamina
        else:
            self.stamina += stamina_growth


class PlayerUnit(BaseUnit):
    pass


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        функция удар соперника
        содержит логику применения соперником умения (только 1 раз)
        """
        if uniform(1, 100) in range(1, 10) and not self._is_skill_used:
            return self.use_skill(target)
        return super().hit(target)
