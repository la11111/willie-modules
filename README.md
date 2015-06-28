# willie-modules
my modules for the Willie IRC Bot

## lastfm.py
full-featured last.fm module for Willie IRC Bot
curently tested on: Willie v. 5.2.0

This module requires an api key, which can be obtained from last.fm. 
put it in your default.cfg like so:
```
[lastfm]
api_key = w4r8ijeoirjargkajgarbage
```

### commands:

**.fmset (lastfm_username)** - set your last.fm username for your IRC nick

**.fmwhois [IRCNick]** - get the last.fm username associated with a given nick

**.np [IRCNick]** - get currently playing track for a given nick

**.fmcompare (IRCNick) [IRCNick2]** - tasteometer comparison between two last.fm users

**.fmtop [overall|week|month|6month|year] [IRCNick]** - list top artists for a given time period
