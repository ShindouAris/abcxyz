import disnake
from disnake.ext import commands
from disnake.enums import ButtonStyle

from enum import Enum
from typing import Union
import random

NULL_EMOJI = ":white_large_square:"
PLAYER1_EMOJI = ":regional_indicator_x:"
PLAYER2_EMOJI = ":o2:"


class Player(int, Enum):
    NULL = 0
    PLAYER1 = 1
    PLAYER2 = 2

class Session():
    session_id: str = None
    choice_map = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    player1_id: int = None
    player2_id: int = None
    current_player = 0
    winner = Player.NULL


    def __init__(self, player1_id: int, player2_id: int):
        self.session_id = "".join(random.choices("0123456789", k=8))
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.current_player = random.randint(1, 2)


    def render_button(self, row: int, column: int) -> disnake.ui.Button:
        button = disnake.ui.Button()
        button.custom_id = f"xoxo_{self.session_id}_{row}_{column}"
        button.disabled = True
        value = self.choice_map[row][column]
        if value == Player.NULL:
            button.style = ButtonStyle.secondary
            button.emoji = NULL_EMOJI
            if self.winner == Player.NULL: button.disabled = False
        elif value == Player.PLAYER1:
            button.style = ButtonStyle.primary
            button.emoji = PLAYER1_EMOJI
        elif value == Player.PLAYER2:
            button.style = ButtonStyle.danger
            button.emoji = PLAYER2_EMOJI
        return button


    def validate_row(self, row: int) -> bool:
        if self.choice_map[row][0] != self.choice_map[row][1]: return False
        if self.choice_map[row][1] != self.choice_map[row][2]: return False
        self.winner = self.choice_map[row][0]
        return True
    
    
    def validate_column(self, column: int) -> bool:
        if self.choice_map[0][column] != self.choice_map[1][column]: return False
        if self.choice_map[1][column] != self.choice_map[2][column]: return False
        self.winner = self.choice_map[0][column]
        return True
    
    
    def validate_cross1(self) -> bool:
        if self.choice_map[0][0] != self.choice_map[1][1]: return False
        if self.choice_map[1][1] != self.choice_map[2][2]: return False
        self.winner = self.choice_map[1][1]
        return True
    
    
    def validate_cross2(self) -> bool:
        if self.choice_map[0][2] != self.choice_map[1][1]: return False
        if self.choice_map[1][1] != self.choice_map[2][0]: return False
        self.winner = self.choice_map[1][1]
        return True
    

    def render_view(self) -> disnake.ui.View:
        view = disnake.ui.View(timeout=60)
        for row in range(3):
            action_row = disnake.ui.ActionRow()
            for column in range(3): action_row.add_button(self.render_button(row, column))
            view.add_item(action_row)
        return view
    

    def select(self, row: int, column: int) -> None:
        if row not in [0, 1, 2]: return
        if column not in [0, 1, 2]: return
        if self.winner != Player.NULL: return
        if self.choice_map[row][column] != Player.NULL: return
        self.choice_map[row][column] = self.current_player
        self.current_player = 1 + (self.current_player + 1) % 2
        if self.validate_row(row): return
        if self.validate_column(column): return
        if row == column:
            if self.validate_cross1(): return
        if row + column == 2:
            if self.validate_cross2(): return
        

class Xoxo(commands.Cog):
    session: dict[str, Session] = {}
    # TODO: Tạo một tác vụ tự động xoá các session không hoạt động trong vòng 90 giây (để giải phóng RAM)

    @commands.slash_command(
        name="xoxo",
        description="Thách đấu bạn bè với trò chơi XOXO (Tic Tac Toe)"
        options=[
            disnake
        ]
    )
    async def xoxo(self, inter: disnake.ApplicationCommandInteraction, opponent: Union[disnake.User, disnake.Member]) -> None:
        if inter.author.bot(): return
        if inter.guild_id is None:
            inte


def setup(bot: commands.Bot):
    bot.add_cog()