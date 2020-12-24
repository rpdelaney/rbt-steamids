Reads in team data formatted like this:

```
[team name] [region (NA/EU/AU/etc)]

- fig newtons 76561197960845047 @fig newtons 
- player 2 [steam_ID] @discord_handle
- player 3 [steam_ID] @discord_handle
- player 4 [steam_ID] @discord_handle
- optional player 5 [steam_ID]
- optional player 6 [steam_ID]
```

And spits out a JSON formatted list of teams with some additional validations performed.
