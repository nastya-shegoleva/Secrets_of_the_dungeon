from data_db import db_session
from data_db.game_func import Game


def add_game(score, level):
    game = Game()
    game.score = score
    game.level = level
    db_sess = db_session.create_session()
    db_sess.add(game)
    db_sess.commit()
    db_sess.close()
