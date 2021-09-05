#!/usr/bin/env python3
#

import json
import re
import sys
from typing import Generator, List

from steam.steamid import SteamID as sid

with open("bans.txt") as f:
    bans = [line.strip("\n") for line in f]


class Player:
    def __init__(self, name, steamid_64):
        self.name = name
        self.steamid_64 = steamid_64

    @property
    def steamid(self):
        try:
            return sid(self.steamid_64).as_steam2
        except ValueError:
            return 0

    @property
    def valid_steamid(self):
        try:
            return sid.is_valid(sid(self.steamid_64))
        except ValueError:
            return False

    @property
    def is_banned(self):
        return self.steamid in bans

    @property
    def url(self):
        try:
            return sid(self.steamid_64).community_url
        except ValueError:
            return ""

    def __iter__(self) -> Generator:
        yield "name", self.name
        yield "steamid64", self.steamid_64
        yield "steamid", self.steamid
        yield "valid_steamid", self.valid_steamid
        yield "is_banned", self.is_banned
        yield "url", self.url


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


def parse_player(line) -> Player:
    # player info
    words = [
        word.strip()
        for word in re.split(r"[\[\]\n]+", line.strip("-"))
        if word.strip()
    ]
    player_name = words[0]
    try:
        steamid_64 = words[1]
    except IndexError:
        steamid_64 = "0"

    return Player(name=player_name, steamid_64=steamid_64)


def main():
    this_team = Team()
    teams = []

    with open("data.txt") as f:
        for line in f:
            if line[0] == "[":
                if this_team:
                    teams.append(this_team)
                this_team = parse_team(line)
            elif line[0] == "-":
                this_player = parse_player(line)
                if this_player.is_banned:
                    print(
                        "Omitting banned player: {} ({})".format(
                            this_player.name, this_player.steamid
                        ),
                        file=sys.stderr,
                    )
                elif not this_player.valid_steamid:
                    print(
                        "Omitting invalid steamid: {} ({})".format(
                            this_player.name, this_player.steamid
                        ),
                        file=sys.stderr,
                    )
                else:
                    this_team.players.append(this_player)

    if this_team.valid_size:
        teams.append(this_team)
    else:
        print(
            "Omitting team with invalid size: {} (size: {})".format(
                this_team.name, this_team.size
            ),
            file=sys.stderr,
        )

    # check for duplicate registrations
    all_steamids = [
        [player.steamid_64 for player in team.players] for team in teams
    ]
    all_steamids = [item for sublist in all_steamids for item in sublist]

    for team in teams:
        for player in team.players:
            reg_count = all_steamids.count(player.steamid_64)
            if reg_count > 1:
                print(
                    "SteamID {} ({}) is registered {} times!".format(
                        player.steamid_64, player.name, reg_count
                    ),
                    file=sys.stderr,
                )

    print(json.dumps(teams, default=dict))


if __name__ == "__main__":
    main()

# EOF
