from trollop import TrelloConnection
from settings import *
import settings
from datetime import datetime, timedelta, date
import pystache
import re
import smtplib
from email.mime.text import MIMEText

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

def email_user():
    me = 'no-reply@localhost'
    you = USER_EMAIL
    msg = MIMEText(BoardView().render())
    msg['Subject'] = 'Your weekly email update for ' + str(date.today())
    msg['From'] = me
    msg['To'] = you

    s = smtplib.SMTP('localhost')
    s.sendmail(me, [you], msg.as_string())
    s.quit()

if __name__ == "__main__":
    email_user()

    # TODO: Email to USER_EMAIL
