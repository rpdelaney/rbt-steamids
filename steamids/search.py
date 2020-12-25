#!/usr/bin/env python3
#

import re
from steam.steamid import SteamID as sid
from typing import Dict
import json

bracketed = re.compile("\\[.+\\]")


def parse_team(line) -> Dict[str, str]:
    # this is a new team

    words = [
        word.strip()
        for word in re.split(r"[\[\]\n]+", line)
        if word.strip()
    ]
    team_name = words[0]
    team_region = words[1]

    return {
        "name": team_name,
        "region": team_region,
        "players": [],
    }


def main():
    team = {}
    teams = []

    with open("data.txt") as f:
        for line in f:
            if line[0] == "[":
                # this is a new team
                if team:
                    teams.append(team)
                team = parse_team(line)

            if line[0] == "-":
                # player info
                words = [
                    word.strip()
                    for word in re.split(r"[\[\]\n]+", line.strip("-"))
                    if word.strip()
                ]
                player_name = words[0]
                steamid64 = words[1]

                team["players"].append(
                    {
                        "name": player_name,
                        "steamid_64": steamid64,
                        "steamid": sid(steamid64).as_steam2,
                        "valid": sid.is_valid(sid(steamid64)),
                        "url": sid(steamid64).community_url,
                    }
                )
    teams.append(team)

    print(json.dumps(teams, default=str))


if __name__ == "__main__":
    main()

# EOF
