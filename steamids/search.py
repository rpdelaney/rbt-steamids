#!/usr/bin/env python3
#

import re
from steam.steamid import SteamID as sid
from typing import Dict, Union, List, Generator
import json

bracketed = re.compile("\\[.+\\]")


class Player:
    def __init__(self, name, steamid_64):
        self.name = name
        self.steamid_64 = steamid_64

    @property
    def steamid(self):
        return sid(self.steamid_64).as_steam2

    @property
    def valid_steamid(self):
        return sid.is_valid(sid(self.steamid_64))


class Team:
    def __init__(
        self, name: str = "", region: str = "", players: List[Player] = []
    ):
        self.name = name
        self.region = region
        self.players: List[Player] = players

    @property
    def size(self):
        return len(self.players)

    @property
    def valid_size(self):
        return 4 <= self.size <= 6

    def __iter__(self) -> Generator:
        yield "name", self.name
        yield "region", self.region
        yield "players", self.players
        yield "size", self.size
        yield "valid_size", self.valid_size


def parse_team(line: str) -> Team:
    # this is a new team

    words = [
        word.strip() for word in re.split(r"[\[\]\n]+", line) if word.strip()
    ]
    team_name = words[0]
    team_region = words[1]

    return Team(name=team_name, region=team_region, players=[])


def parse_player(line) -> Dict[str, Union[str, bool]]:
    # player info
    words = [
        word.strip()
        for word in re.split(r"[\[\]\n]+", line.strip("-"))
        if word.strip()
    ]
    player_name = words[0]
    try:
        steamid64 = words[1]
    except IndexError:
        steamid64 = "0"

    return {
        "name": player_name,
        "url": sid(steamid64).community_url,
        "steamid_64": steamid64,
        "steamid": sid(steamid64).as_steam2,
        "valid_steamid": sid.is_valid(sid(steamid64)),
    }


def main():
    this_team = {}
    teams = []

    with open("data.txt") as f:
        for line in f:
            if line[0] == "[":
                if this_team:
                    teams.append(this_team)
                this_team = parse_team(line)
            elif line[0] == "-":
                this_team.players.append(parse_player(line))

    teams.append(this_team)

    print(json.dumps(teams, default=dict))


if __name__ == "__main__":
    main()

# EOF
