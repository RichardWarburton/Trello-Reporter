from trollop import TrelloConnection
from settings import *
from datetime import datetime, timedelta
import pystache
import re

# NB: also includes actions from the past, deliberate behaviour
one_week = timedelta(days=7)
before = datetime.now() + one_week
conn = TrelloConnection(TRELLO_KEY, USER_TOKEN)

if locals().has_key('ONLY_BOARDS'):
    check = lambda board: board.name in ONLY_BOARDS
else:
    check = lambda board: True

class BoardView(pystache.View):
    
    template_name = 'plaintext'

    def boards(self):
        for board in conn.me.boards:
            if not board.closed and check(board):
                print board.name
                tasks = self._get_tasks(board)
                yield { 'tasks': tasks,
                        'empty': not tasks,
                        'board_name': board.name, }
        
    def _get_tasks(self, board):
        tasks = []
        for card in board.cards:
            if not card.closed and card._data.has_key('due') and conn.me.username in [m.username for m in card.members]:
                due = datetime(*map(int, re.split('[^\d]', card._data['due'])[:-1]))
                if due <= before:
                    tasks.append({'msg': card.name, 'date': due})
        return tasks

    def username(self):
        return conn.me.fullname

if __name__ == "__main__":
    print BoardView().render()

    # TODO: Email to USER_EMAIL
