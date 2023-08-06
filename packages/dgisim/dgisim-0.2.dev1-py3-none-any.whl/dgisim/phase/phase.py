from __future__ import annotations
from abc import abstractmethod
from typing import Optional, TYPE_CHECKING

from ..helper.level_print import level_print_single

if TYPE_CHECKING:
    from ..state.game_state import GameState
    from ..action.action import PlayerAction
    from ..action.action_generator import ActionGenerator
    from ..state.enums import PID

__all__ = [
    "Phase",
]


class Phase:
    @abstractmethod
    def step(self, game_state: GameState) -> GameState:
        raise NotImplementedError

    @abstractmethod
    def step_action(self, game_state: GameState, pid: PID, action: PlayerAction) -> Optional[
            GameState]:
        raise NotImplementedError

    def waiting_for(self, game_state: GameState) -> Optional[PID]:
        players = [game_state.get_player1(), game_state.get_player2()]
        for player in players:
            if player.get_phase().is_action_phase():
                return game_state.get_pid(player)
        return None

    @abstractmethod
    def action_generator(self, game_state: GameState, pid: PID) -> None | ActionGenerator:
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Phase)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __str__(self) -> str:
        return self.to_string(0)

    def to_string(self, indent: int = 0) -> str:
        return level_print_single(self.__class__.__name__, indent)

    def dict_str(self) -> dict | str:
        return self.__class__.__name__
