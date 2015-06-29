# coding=utf8
"""
help.py - Willie Help Module
Copyright 2008, Sean B. Palmer, inamidst.com
Copyright © 2013, Elad Alfassa, <elad@fedoraproject.org>
Licensed under the Eiffel Forum License 2.

http://willie.dftba.net
"""
from __future__ import unicode_literals
from willie.module import commands, rule, example, priority
from willie.tools import iterkeys
from subprocess import check_output
import threading
import willie.module
import willie.tools
from willie.config import ConfigurationError
import os

def setup(bot):
   # locks for log files
    if not bot.memory.contains('greplog_locks'):
        bot.memory['greplog_locks'] = willie.tools.WillieMemoryWithDefault(threading.Lock)

@commands('greplogs')
@priority('low')
def greplogs(bot, trigger):
    """grep the logs!"""
    if trigger.is_privmsg:
        bot.reply("send this command from the main channel, please ;P")
        return
    channel = bot.origin.sender.lstrip('#')
    nick = trigger.nick
    query = trigger.group(2)
    logdir = bot.config.chanlogs.dir
    
    result = check_output(['/bin/sh', '-c', 'egrep -e "{}" {}/{}*.log'.format(query, logdir, channel)])
    fpath = os.path.expanduser('~/public_html/{}.txt'.format(nick))
    with bot.memory['greplog_locks'][fpath]:
        with open(fpath, 'w') as f:
            f.write(result)
    bot.reply("http://velvetandl.ace.gy/~willie_freenode/{}.txt".format(nick)) 
    
#    bot.say("channel: '{}'; query: '{}'".format(channel, query))
