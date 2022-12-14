from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from unit import BaseUnit


class SkillABC(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def stamina(self):
        pass

    @property
    @abstractmethod
    def damage(self):
        pass


class Skill(SkillABC):
    """
    Базовый класс умения
    """
    user = None
    target = None
    name = None
    stamina = None
    damage = None

    def skill_effect(self) -> str:
        """
        использование скилла, происходит уменьшение стамины у игрока применяющего умение и
        уменьшение здоровья цели
        """
        self.user.stamina -= self.stamina
        self.target.get_damage(self.damage)
        return f"{self.user.name} использует {self.name} и наносит {self.damage} урона сопернику."

    def _is_stamina_enough(self):
        """
        Проверка достаточно ли выносливости
        """
        return self.user.stamina > self.stamina

    def use(self, user: BaseUnit, target: BaseUnit) -> str:
        """
        Проверка, достаточно ли выносливости у игрока для применения умения.
        Для вызова скилла везде используем use
        """
        self.user = user
        self.target = target
        if self._is_stamina_enough:
            return self.skill_effect()
        return f"{self.user.name} попытался использовать {self.name} но у него не хватило выносливости."


class FuryPunch(Skill):
    name = "Лютый пинок"
    stamina = 6
    damage = 12


class HardShot(Skill):
    name = "Жуткий укол"
    stamina = 5
    damage = 15
