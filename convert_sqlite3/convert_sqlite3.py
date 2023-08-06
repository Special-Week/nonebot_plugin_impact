import json
from typing import Dict

from loguru import logger
from sqlalchemy import (
    Boolean,
    Column,
    Engine,
    Float,
    Integer,
    String,
    create_engine,
    orm,
)
from sqlalchemy.orm import sessionmaker

engine: Engine = create_engine("sqlite:///impact.db")
session = sessionmaker(engine)
Base = orm.declarative_base()


class UserData(Base):
    __tablename__: str = "userdata"
    userid = Column(Integer, primary_key=True, index=True)
    jj_length = Column(Float, nullable=False)


class GroupData(Base):
    __tablename__: str = "groupdata"
    groupid = Column(Integer, primary_key=True, index=True)
    allow = Column(Boolean, nullable=False)


class EjaculationData(Base):
    __tablename__: str = "ejaculation_data"
    id = Column(Integer, primary_key=True)
    userid = Column(Integer, nullable=False, index=True)
    date = Column(String(20), nullable=False)
    volume = Column(Float, nullable=False)


Base.metadata.create_all(engine)


with open("userdata.json", "r", encoding="utf-8") as f:
    userdata: Dict[str, float] = json.load(f)

with open("groupdata.json", "r", encoding="utf-8") as f:
    groupdata: Dict[str, Dict[str, bool]] = json.load(f)

with open("ejaculation_data.json", "r", encoding="utf-8") as f:
    ejaculation_data: Dict[str, Dict[str, Dict[str, float]]] = json.load(f)


with session() as s:
    for userid, jj_length in userdata.items():
        if not s.query(UserData).filter(UserData.userid == userid).first():
            logger.info(f"插入用户 {userid}")
            s.add(UserData(userid=int(userid), jj_length=jj_length))
        else:
            logger.info(f"用户 {userid} 已存在, 跳过插入")

    for groupid, allow in groupdata.items():
        if not s.query(GroupData).filter(GroupData.groupid == groupid).first():
            logger.info(f"插入群组 {groupid}")
            s.add(GroupData(groupid=int(groupid), allow=allow["allow"]))
        else:
            logger.info(f"群组 {groupid} 已存在, 跳过插入")

    for userid, data in ejaculation_data.items():
        for date, volume in data.items():
            if (
                not s.query(EjaculationData)
                .filter(EjaculationData.userid == userid, EjaculationData.date == date)
                .first()
            ):
                logger.info(f"插入用户 {userid} 的射精数据 {date}")
                s.add(
                    EjaculationData(
                        userid=int(userid), date=date, volume=volume["ejaculation"]
                    )
                )
            else:
                logger.info(f"用户 {userid} 的射精数据 {date} 已存在, 跳过插入")
    s.commit()
