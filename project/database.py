from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Date, \
    ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from . import config

engine = create_engine(config.DATABASE_URL, convert_unicode=True, **config.DATABASE_CONNECT_OPTIONS)
db_session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Model = declarative_base(name='Model')
Model.query = db_session.query_property()


def init_db():
    Model.metadata.create_all(bind=engine)


class Stock(Model):
    __tablename__ = 'stocks'
    code = Column(String(10), primary_key=True)
    name = Column(String(10))
    intro = Column(String(100))
    tag = Column(String(50))
    update_time = DateTime
    # 冗余交易字段
    price = Column(Float)  # 最后一个完结交易日收盘价
    volume = Column(Integer)  # 成交量
    change = Column(Float)  # 涨跌值，真实小数（非百分比）
    open = Column(Float)
    close = Column(Float)
    high = Column(Float)
    low = Column(Float)
    capitalization = Column(Integer)  # 市值
    pe = Column(Float)  # 市盈率
    pb = Column(Float)  # 市净率
    turnover_rate = Column(Float)  # 换手率


class DailyRecord(Model):
    __tablename__ = 'dailyrecords'
    code = Column(String(10))
    date = Column(Date)
    price = Column(Float)  # 收盘价
    volume = Column(Integer)  # 成交量
    change = Column(Float)  # 涨跌值，真实小数（非百分比）
    open = Column(Float)
    close = Column(Float)
    high = Column(Float)
    low = Column(Float)
    capitalization = Column(Integer)  # 市值
    pe = Column(Float)
    pb = Column(Float)
    turnover_rate = Column(Float)  # 换手率
    relative_ratio = Column(Float)  # 量比


class MinutelyRecord(Model):
    __tablename__ = 'minutelyrecords'
    code = Column(String(10))
    date = Column(Date)
    hour = Column(Integer)
    minute = Column(Integer)
    price = Column(Float)  # 当前价
    volume = Column(Integer)  # 成交量
    turnover_rate = Column(Float)  # 换手率
    relative_ratio = Column(Float)  # 量比


class Discovery(Model):
    __tablename__ = 'discovery'
    id = Column(Integer, primary_key=True)
    code = Column(String(10))
    date_time = Column(DateTime)
    type = Column(Integer)
    days = Column(Integer)
    gold_score = Column(Float)  # 黄金分数
    description = Column(String(100))


class UpdateLog(Model):
    __tablename__ = 'updatelogs'
    id = Column(Integer, primary_key=True)
    code = Column(String(10))
    date = Column(Date)
