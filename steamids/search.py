#!/usr/bin/env python3
#

import re
from steam.steamid import SteamID as sid
import json

bracketed = re.compile("\\[.+\\]")


def main():
    team = {}
    teams = []
    with open("data.txt") as f:
        for line in f:
            if line[0] == "[":
                # this is a new team
                if team:
                    teams.append(team)
                team = {}

                words = [
                    word.strip() for word
                    in re.split(r"[\[\]\n]+", line)
                    if word.strip()
                ]
                team_name = words[0]
                team_region = words[1]

                team = {
                    "name": team_name,
                    "region": team_region,
                    "players": []
                }

            if line[0] == "-":
                # player info
                words = [
                    word.strip() for word
                    in re.split(r"[\[\]\n]+", line.strip("-"))
                    if word.strip()
                ]
                player_name = words[0]
                steamid64 = words[1][1:-1]
                steamid = sid(steamid64).as_steam2

                team["players"].append(
                    {
                        "name": player_name,
                        "steamid_64": steamid64,
                        "steamid": steamid
                    }
                )

    teams.append(team)
    print(json.dumps(teams, default=str))


if __name__ == "__main__":
    main()

# EOF
