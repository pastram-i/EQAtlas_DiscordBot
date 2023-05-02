from pydantic import BaseModel
from typing import Literal

class Zone(BaseModel):
    name: str
    continent: str
    type: str
    url_name: str
    friendly_name: str
    name_in_who: str
    url: str
    above_45: bool
    key_required: bool
    firepot_port: bool
    shaman_port: bool
    druid_port: bool
    wizard_port: bool
    level_of_monsters: str
    zem_value: str
    succor_evac: str
    zone_spawn_timer: str
    class Config:
        orm_mode = True

class Connection(BaseModel):
    zone: str
    connected_to: str
    ocean_connection: bool
    one_way_connection: bool
    class Config:
        orm_mode = True

class Link(BaseModel):
    zone: str
    value: str
    type: Literal['monster', 'npc', 'item', 'quests', 'guilds', 'city race', 'tradeskill facility', 'guides']
    url: str
    class Config:
        orm_mode = True