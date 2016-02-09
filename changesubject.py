# coding=utf8
"""
conversation starter by Brenna
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

def get_topic():
    page = requests.get('http://www.conversationstarters.com/generator.php')
    tree = html.fromstring(page.text)
    return tree.xpath("//div[@id='random']")[0].text_content()

@commands('changesubject', 'newtopic', 'nt')
def name_meaning(bot, trigger):
    query = get_topic() 
    if not query:
        bot.reply("Something bad happened. Try again later maybe.")
        return NOLIMIT
    bot.reply(query)
