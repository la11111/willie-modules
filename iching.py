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
import json
import random
import string
import re


class Iching(object):
    def __init__(self):
        self.text = json.loads(
            open('/var/kitty/.willie/modules/texts_iching/iching2.json').read()
        )['hexagrams']
        self.hgtable =  {n['pattern']: int(n['hexnum']) for n in self.text}

    def cast(self):
        return ''.join(
            [str(random.randint(6,9)) for x in xrange(6)]
        )

    def hg_char(self, n):
        return unichr(n+19903)

    def get_hg(self, lines):
        n = self.hgtable[lines] - 1
        r = []
        r.append(u'~~ Hexagram: {} ( {} )'.format(n+1, self.hg_char(n+1)))
        r.append(u' | Title: {}'.format(self.text[n]['title']))
        r.append(u'  ({} above {})'.format(
            self.text[n]['above'], 
            self.text[n]['below']
        ))
        r.append(u' | Image: {}'.format(self.text[n]['image']))
        r.append(u' | Judgement: {}'.format(self.text[n]['judgement']))
        try:
            r.append(u' | **extra: {}'.format(self.text[n]['extra']))
        except (KeyError): 
            pass
        return ''.join(r)

    def reading(self):
        r = []
        cast = moving = changed = coins = self.cast() 
        cast = re.sub('[68]', '0', cast)
        cast = re.sub('[79]', '1', cast)
        moving = re.sub('[69]','1',moving)
        moving = re.sub('[78]','0',moving)
        changed = re.sub('[67]','1',changed)
        changed = re.sub('[89]','0',changed)
        r.append(u"  ~  I Ching Reading  ~  ")
        r.append(u"your cast: {}".format(coins))
        r.append('---')
        r.append(self.get_hg(cast))
        if moving == '000000':
            return ''.join(r)
        r.append('---')
        r.append("Moving Lines : {} | ".format(moving))
        for i in xrange(6):
            if moving[i] == '1':
                r.append(self.text[self.hgtable[cast]]['lines']['line'][i])
                r.append(' ')
        r.append('---')
        r.append(self.get_hg(changed))
        return ''.join(r)

i = Iching()

@commands('iching')
@priority('low')
def iching(bot, trigger):
    if not trigger.is_privmsg:
        bot.reply("Sending I Ching reading in PM ^.^")
    for m in i.reading().split('---'):
        bot.msg(trigger.nick, m, max_messages=10)
