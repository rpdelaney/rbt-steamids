#!/usr/bin/env python3
#

import re
from steam.steamid import SteamID as sid
from typing import Dict, Union
import json

bracketed = re.compile("\\[.+\\]")


def parse_team(line) -> Dict[str, str]:
    # this is a new team

    words = [
        word.strip() for word in re.split(r"[\[\]\n]+", line) if word.strip()
    ]
    team_name = words[0]
    team_region = words[1]

    return {
        "name": team_name,
        "region": team_region,
        "players": [],
    }


def add_team_metadata(team: Dict[str, str]) -> None:
    team["size"] = len(team["players"])
    team["valid_size"] = 4 <= team["size"] <= 6


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
    team = {}
    teams = []

    with open("data.txt") as f:
        for line in f:
            if line[0] == "[":
                if team:
                    add_team_metadata(team)
                    teams.append(team)
                team = parse_team(line)
            elif line[0] == "-":
                team["players"].append(parse_player(line))

    add_team_metadata(team)
    teams.append(team)

    print(json.dumps(teams, default=str))


if __name__ == "__main__":
    main()

# EOF
