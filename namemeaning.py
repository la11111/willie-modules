# coding=utf8
"""
Name meaning lookup by Brenna
Copyright 2015 brenna kathryn sage CC 
Licensed under the gpl v2.
"""
from __future__ import unicode_literals
from sopel import web
from sopel.module import NOLIMIT, commands, example
from sopel.formatting import bold
import re
from lxml import html
import requests

def lookup_name(query):
    page = requests.get('http://www.sheknows.com/baby-names/name/{}'.format(query))
    tree = html.fromstring(page.text)
    result = tree.xpath('//title')[0].text
    if result == 'Errors':
        return
    ret_list = []
    meanings = tree.xpath("//p[@class='origin_descrip']")
    for m in meanings:
        mraw = m.text_content()
        ret_list.append(bold(' '.join(mraw.split(':')[0].split()) + ': ') + ' '.join(mraw.split(':')[2].split()))
    return query + ': ' + ' '.join(ret_list)



@commands('name', 'namemeaning', 'nm')
@example('.nm jennifer')
def name_meaning(bot, trigger):

    if trigger.group(2) is None:
        bot.reply("What name do you want me to look up?")
        return NOLIMIT

    query = trigger.group(2)

    if not query:
        bot.reply('What name do you want me to look up?')
        return NOLIMIT

    query = lookup_name(query)
    if not query:
        bot.reply("I can't find any results for that.")
        return NOLIMIT

    bot.say(query)
