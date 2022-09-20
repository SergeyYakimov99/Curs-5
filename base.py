from typing import Optional

from unit import BaseUnit


class BaseSingleton(type):
    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 1
    player = None
    enemy = None
    game_is_running = False
    battle_result = "Бой не закончен"

    def start_game(self, player: BaseUnit, enemy: BaseUnit) -> None:
        # TODO НАЧАЛО ИГРЫ
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self) -> Optional[str]:
        """
        ПРОВЕРКА ЗДОРОВЬЯ ИГРОКА И ВРАГА
        """
        if self.player.hp <= 0 and self.enemy.hp <= 0:
            self.battle_result = "Ничья"
            return self._end_game()
        elif self.enemy.hp <= 0:
            self.battle_result = "Вы победили"
            return self._end_game()
        elif self.player.hp <= 0:
            self.battle_result = "Вы проиграли"
            return self._end_game()

    def _stamina_regeneration(self) -> None:
        """
        регенерация здоровья и стамины для игрока и врага за ход
        """
        self.player.add_stamina(self.STAMINA_PER_ROUND)
        self.enemy.add_stamina(self.STAMINA_PER_ROUND)

    def next_turn(self) -> str:
        """
        СЛЕДУЮЩИЙ ХОД
        срабатывает когда игрок пропускает ход или когда игрок наносит удар.
        """
        result = self._check_players_hp()
        if result:
            return result
        self._stamina_regeneration()
        return self.enemy.hit(self.player)

    def _end_game(self) -> str:
        """
        КНОПКА ЗАВЕРШЕНИЕ ИГРЫ
        """
        self._instances = {}
        self.game_is_running = False
        return self.battle_result

    def player_hit(self) -> str:
        """
        КНОПКА УДАР ИГРОКА
        """
        result = f"{self.player.hit(self.enemy)} {self.next_turn()}"
        return result

    def player_use_skill(self) -> str:
        """
        КНОПКА: ИГРОК ИСПОЛЬЗУЕТ УМЕНИЕ
        """
        result = self.player.use_skill(self.enemy)
        self.next_turn()
        return result
