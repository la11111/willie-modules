"""
lastfm.py - last.fm checker for willie bot
Written by Brenna Sage (unikitty11111@gmail.com)

loosely based on: https://github.com/mulcare/willie-modules
license: GPL2

To use this module, you'll need to get an api key from last.fm.
place the key in your willie .cfg file like so:
...
[lastfm]
api_key = <your_api_key_lsdkjo4ij4>
...
"""

from __future__ import unicode_literals
from willie import web
from willie.module import commands, example
import json
import sys
import re

def get_api_key(bot):
    if not bot.config.has_option('lastfm', 'api_key'):
        raise KeyError('Missing Last.fm API key')
    return bot.config.lastfm.api_key

def configure(config):
    if config.option('Configure Last.fm API', False):
        config.interactive_add(
            'lastfm', 
            'api_key', 
            'Last.fm API key'
        )

def query_lastfm(bot, **kwargs):
    args = []
    for k in kwargs:
        args.append("{}={}".format(k, kwargs[k]))
    args.append('api_key={}'.format(get_api_key(bot)))
    args.append('format=json')
    url = 'http://ws.audioscrobbler.com/2.0/?' + '&'.join(args)
    return web.get(url)

@commands('fmwhois','fmwho')
@example('.fmwhois')
@example('.fmwhois CoolIRCUser69')
def fmwhois(bot, trigger):
    """returns the lastfm username associated with a given IRC nick."""
    if trigger.group(2):
        nick = re.match(r'^\S+', trigger.group(2)).group()
    else:
        nick = trigger.nick
    fmuser = bot.db.get_nick_value(nick, 'lastfm_user')
    if fmuser:
        bot.say("{} is {} on last.fm.".format(nick, fmuser))
    else:
        bot.reply("unknown user for '{}'. use .fmset to set up your last.fm account name.".format(nick))

@commands('fmset')
@example('fmset my_lastfm_username69')
def update_lastfm_user(bot, trigger):
    """associates a lastfm username with your IRC nick. run this first."""
    if not trigger.group(2):
        bot.reply("usage: .fmset [last.fm username]")
        return
    user = re.match(r'^\S+', trigger.group(2)).group().lower()
    bot.db.set_nick_value(trigger.nick, 'lastfm_user', user)
    bot.reply('last.fm username set to "{}" :)'.format(user))

@commands('np', 'lastfm')
@example('.np')
@example('.np CoolIRCUser69')
def nowplaying(bot, trigger):
    """displays the most recent track played by a given IRC nick."""
    output = '' 
    notme = False
    if trigger.group(2):
        nick = re.match(r'^\S+', trigger.group(2)).group()
        notme = True
    else:
        nick = trigger.nick
    fmuser = bot.db.get_nick_value(nick, 'lastfm_user')
    if not fmuser:
        bot.reply("Invalid username given or no username set. Use .fmset to set a username.")
        return
    try:
        recent_tracks = query_lastfm(
            bot, 
            method = 'user.getrecenttracks', 
            user=web.quote(fmuser)
        )
    except Exception, e:
        bot.say("Couldn't contact last.fm :(")
        return
    try:
        last_track = json.loads(recent_tracks)['recenttracks']['track'][0]
    except KeyError:
        bot.say("Couldn't find user :(")
        return
    try:
        track_info = query_lastfm(
            bot, 
            method = "track.getInfo",
            artist = last_track['artist']['#text'],
            track = last_track['name'],
            username = fmuser
        )
    except Exception, e:
        bot.say("error looking up track :(")
        return
    try:
        track_data = json.loads(track_info)['track']
    except KeyError:
        bot.say("couldn't find track :(")
        return
    try:
        playcount = track_data['userplaycount']
    except KeyError:
        playcount = "unknown"
    loved = int(track_data['userloved'])
    track_name = last_track['name']
    track_url = last_track['url']
    artist = last_track['artist']['#text']
    album = last_track['album']['#text'] or 'unknown album'
    try:
        if notme:
            output += "{} is listening to: ".format(nick)
        if loved > 0:
            output += '\x035' + u'\u2665' +'\x03 ' # a little heart
        output += '{} - {} - ({}) ({} plays) {}'.format(artist, track_name, album, playcount, track_url)     
        bot.say(output)
    except KeyError:
        bot.say("Couldn't find any recent tracks :(")

nowplaying.rate = 0
nowplaying.priority = 'low'

@commands('fmcmp', 'fmcompare')
@example('.fmcmp IRCUser69')
@example('.fmcmp IRCNick1 IRCNick2')
def fmcmp(bot, trigger):
    """compares the music taste of two nicks via last.fm's 'tasteometer' function."""
    if not trigger.group(2):
        bot.reply('need a nick to compare to you, or two nicks to compare together.')
        return
    m = re.findall(r'\S+', trigger.group(2))
    if len(m) == 1:
        nick1 = trigger.nick
        nick2 = m[0]
    else:
        nick1,nick2 = m
    fmuser1 = bot.db.get_nick_value(nick1, 'lastfm_user')
    fmuser2 = bot.db.get_nick_value(nick2, 'lastfm_user')
    if not fmuser1:
        bot.reply('{} needs to run .fmset.'.format(nick1))
        return
    if not fmuser2:
        bot.reply('{} needs to run .fmset.'.format(nick2))
        return
    result_json = query_lastfm(
        bot,
        method = 'tasteometer.compare',
        type1 = 'user',
        type2 = 'user',
        value1 = fmuser1,
        value2 = fmuser2,
        limit = '10',
    )
    result = json.loads(result_json)
    artists = []
    score = str(int(float(result['comparison']['result']['score'])*100))
    try:
        result['comparison']['result']['artists']['artist']
    except KeyError:
        bot.say("no shared artists :(")
        return
    for a in result['comparison']['result']['artists']['artist']:
        artists.append(a['name'])
    output = 'comparing {} and {} | score: {}% | top 10 artists: [{}]'.format(
        nick1,
        nick2,
        score,
        ', '.join(artists)
    )
    bot.say(output)

@commands('fmtop')
@example('.fmtop')
@example('.fmtop week')
@example('.fmtop IRCUser69')
@example('.fmtop 6month IRCUser69')
def fmtop(bot, trigger):
    """shows the top played artists for a given IRC nick over a given time period."""
    times = {
        'overall':'overall', 
        'week':'7day', 
        'month':'1month', 
        '6month':'6month', 
        'year':'12month'
    }
    if not trigger.group(2):
        nick = trigger.nick
        time = 'overall'
    else: 
        m = re.findall(r'\S+', trigger.group(2))
        if len(m) == 1:
            if re.match(r'^overall|year|week|month$', m[0]):
                time = times[m[0]]
                nick = trigger.nick
            else:
                nick = m[0]
                time = 'overall'
        else: #len == 2+
            if not re.match(r'^overall|year|week|month|6month$', m[0]):
                bot.say('usage: .fmtop (overall|year|6month|month|week)? (nick)?')
                return
            else:
                time = times[m[0]]
                nick = m[1]
    fmuser = bot.db.get_nick_value(nick, 'lastfm_user')
    if not fmuser:
        bot.reply('{} needs to run .fmset.'.format(nick))
        return
    result_json = query_lastfm(
        bot,
        method = 'user.getTopArtists',
        user = fmuser,
        period = time,
        limit = '10'
    )
    result = json.loads(result_json)
    artists = []
    for a in result['topartists']['artist']:
        artists.append(a['name'])
    output = 'Top artists for {}, period: {}: [{}]'.format(
        nick, 
        time, 
        ', '.join(artists)
    )
    bot.say(output)
