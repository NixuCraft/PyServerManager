from dataclasses import dataclass


@dataclass
class GameType:
    name: str
    variant: str

    display_name: str
    room_icon: str
    
    min_protocol: int
    max_protocol: int

    min_players: int
    max_players: int

    plugins: list[str]

    def serialize(self):
        return {
            "name": self.name,
            "variant": self.variant,
            "display_name": self.display_name,
            "min_protocol": self.min_protocol,
            "max_protocol": self.max_protocol,
            "min_players": self.min_players,
            "max_players": self.max_players,
            "plugins": self.plugins
        }