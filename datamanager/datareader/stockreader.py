from ..database import  db_session,Stock

def get_all_stocks():
    return db_session.query(Stock).filter(Stock.isdel == False).all()

def get_stock(code):
    return db_session.query(Stock).filter(Stock.isdel == False, Stock.code == code).one()