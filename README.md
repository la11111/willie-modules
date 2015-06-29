# willie-modules
my modules for the Willie IRC Bot

## lastfm.py
full-featured last.fm module for Willie IRC Bot

Re-written based (loosely) on last.fm by mulcare/meiccelli with a number of improvements.
Curently tested on: Willie v. 5.2.0

This module requires an api key, which can be obtained from last.fm. 
put it in your default.cfg like so:
```
[lastfm]
api_key = w4r8ijeoirjargkajgarbage
```

### commands:

**.fmset (lastfm_username)** - set your last.fm username for your IRC nick

**.fmwhois [IRCNick]** - get the last.fm username associated with a given nick

**.np [IRCNick|lastfm_username]** - get currently playing track for a given nick

**.fmcompare (IRCNick|lastfm_username) [IRCNick2|lastfm_username]** - tasteometer comparison between two last.fm users

**.fmtop [overall|week|month|6month|year] [IRCNick|lastfm_username]** - list top artists for a given time period
