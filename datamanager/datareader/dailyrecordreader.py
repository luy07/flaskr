from ..database import  db_session,DailyRecord

def get_dailyrecords(code,begin_date,end_date):
    return db_session.query(DailyRecord).filter(DailyRecord.code==code,DailyRecord.date>=begin_date,DailyRecord.date<=end_date).all()
