from trollop import TrelloConnection
from settings import *
import settings
from datetime import datetime, timedelta
import pystache
import re

# NB: also includes actions from the past, deliberate behaviour
one_week = timedelta(days=7)
before = datetime.now() + one_week
conn = TrelloConnection(TRELLO_KEY, USER_TOKEN)
all_settings = dir(settings)

def optional(before, name, func):
    if name in all_settings:
        return lambda x: before(x) and func(x)
    else:
        return before

check = lambda card: card._data.has_key('due')
check = optional(check, 'ONLY_BOARDS', lambda card: card.board.name in ONLY_BOARDS)
check = optional(check, 'IGNORE_LISTS', lambda card: card.list.name not in IGNORE_LISTS)

class BoardView(pystache.View):
    
    template_name = TEMPLATE

    def cards(self):
        for card in conn.me.cards:
            if check(card):
                due = datetime(*map(int, re.split('[^\d]', card._data['due'])[:-1]))
                if due <= before:
                    yield { 'msg': card.name, 'date': due, }

    def username(self):
        return conn.me.fullname

if __name__ == "__main__":
    print BoardView().render()

    # TODO: Email to USER_EMAIL
