"""数据库操作模块, 用于存储用户的jj长度, 以及群聊是否允许银趴, 以及每天的被注入量"""
import os
import random
import time
from typing import Dict, List

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

# 数据库路径
DATA_PATH = "data/impact"

# 不存在则创建文件夹
if not os.path.exists("data"):
    os.mkdir("data")
if not os.path.exists(DATA_PATH):
    os.mkdir(DATA_PATH)


engine: Engine = create_engine(f"sqlite:///{DATA_PATH}/impact.db")
session = sessionmaker(engine)
Base = orm.declarative_base()


class UserData(Base):
    """用户数据表"""

    __tablename__: str = "userdata"

    userid = Column(Integer, primary_key=True, index=True)
    jj_length = Column(Float, nullable=False)
    last_masturbation_time = Column(Integer, nullable=False, default=0)


class GroupData(Base):
    """群数据表"""

    __tablename__: str = "groupdata"

    groupid = Column(Integer, primary_key=True, index=True)
    allow = Column(Boolean, nullable=False)


class EjaculationData(Base):
    """被注入数据表"""

    __tablename__: str = "ejaculation_data"

    id = Column(Integer, primary_key=True)
    userid = Column(Integer, nullable=False, index=True)
    date = Column(String(20), nullable=False)
    volume = Column(Float, nullable=False)


Base.metadata.create_all(engine)


def is_in_table(userid: int) -> bool:
    """传入一个userid，判断是否在表中"""
    with session() as s:
        return bool(s.query(UserData).filter(UserData.userid == userid).first())


def add_new_user(userid: int) -> None:
    """插入一个新用户, 默认长度是10.0"""
    with session() as s:
        s.add(
            UserData(
                userid=userid, jj_length=10.0, last_masturbation_time=int(time.time())
            )
        )
        s.commit()


def update_activity(userid: int) -> None:
    """更新用户活跃时间"""
    # 如果用户不在表中, 则插入一条记录
    if not is_in_table(userid):
        add_new_user(userid)
    with session() as s:
        s.query(UserData).filter(UserData.userid == userid).update(
            {UserData.last_masturbation_time: int(time.time())}
        )
        s.commit()


def get_jj_length(userid: int) -> float:
    """传入用户id, 返还数据库中对应的jj长度"""
    with session() as s:
        return s.query(UserData).filter(UserData.userid == userid).first().jj_length  # type: ignore


def set_jj_length(userid: int, length: float) -> None:
    """传入一个用户id以及需要增加的长度, 在数据库内累加, 用这个函数前一定要先判断用户是否在表中"""
    with session() as s:
        # 先获取当前的长度, 然后再累加
        current_length = (
            s.query(UserData).filter(UserData.userid == userid).first().jj_length
        )  # type: ignore
        s.query(UserData).filter(UserData.userid == userid).update(
            {
                UserData.jj_length: round(current_length + length, 3),
                UserData.last_masturbation_time: int(time.time()),
            }
        )
        s.commit()


def check_group_allow(groupid: int) -> bool:
    """检查群是否允许, 传入群号, 类型是int"""
    with session() as s:
        if s.query(GroupData).filter(GroupData.groupid == groupid).first():
            return s.query(GroupData).filter(GroupData.groupid == groupid).first().allow  # type: ignore
        else:
            return False


def set_group_allow(groupid: int, allow: bool) -> None:
    """设置群聊开启或者禁止银趴, 传入群号, 类型是int, 以及allow, 类型是bool"""
    with session() as s:
        # 如果群号不存在, 则插入一条记录, 默认是禁止
        if not s.query(GroupData).filter(GroupData.groupid == groupid).first():
            s.add(GroupData(groupid=groupid, allow=False))
        # 然后再根据传入的allow来更新
        s.query(GroupData).filter(GroupData.groupid == groupid).update(
            {GroupData.allow: allow}
        )
        s.commit()


def get_today() -> str:
    """获取当前年月日格式: 2023-02-04"""
    return time.strftime("%Y-%m-%d", time.localtime())


def insert_ejaculation(userid: int, volume: float) -> None:
    """插入一条注入的记录"""
    now_date = get_today()
    with session() as s:
        # 如果没有这个用户的记录, 则插入一条
        if (
            not s.query(EjaculationData)
            .filter(EjaculationData.userid == userid)
            .first()
        ):
            s.add(EjaculationData(userid=userid, date=now_date, volume=volume))
        # 如果有这个用户以及这一天的记录, 则累加
        elif (
            s.query(EjaculationData)
            .filter(EjaculationData.userid == userid, EjaculationData.date == now_date)
            .first()
        ):
            # 当前的值
            current_volume = (
                s.query(EjaculationData)
                .filter(
                    EjaculationData.userid == userid, EjaculationData.date == now_date
                )
                .first()
                .volume
            )  # type: ignore
            s.query(EjaculationData).filter(
                EjaculationData.userid == userid, EjaculationData.date == now_date
            ).update({EjaculationData.volume: round(current_volume + volume, 3)})
        # 如果有这个用户但是没有这一天的记录, 则插入一条
        else:
            s.add(EjaculationData(userid=userid, date=now_date, volume=volume))
        s.commit()


def get_ejaculation_data(userid: int) -> List[Dict]:
    """获取一个用户的所有注入记录"""
    with session() as s:
        return [
            {"date": i.date, "volume": i.volume}
            for i in s.query(EjaculationData).filter(EjaculationData.userid == userid)
        ]


def get_today_ejaculation_data(userid: int) -> float:
    """获取用户当日的注入量"""
    with session() as s:
        # 如果找得到这个用户的id以及今天的日期, 则返回注入量
        if (
            s.query(EjaculationData)
            .filter(
                EjaculationData.userid == userid, EjaculationData.date == get_today()
            )
            .first()
        ):
            return (
                s.query(EjaculationData)
                .filter(
                    EjaculationData.userid == userid,
                    EjaculationData.date == get_today(),
                )
                .first()
                .volume
            )  # type: ignore
        # 否则返回0
        else:
            return 0.0


def punish_all_inactive_users() -> None:
    """所有不活跃的用户, 即上次打胶时间超过一天的用户, 所有jj_length大于1将受到减少0--1随机的惩罚"""
    with session() as s:
        for i in s.query(UserData).all():
            if time.time() - i.last_masturbation_time > 86400 and i.jj_length > 1:
                i.jj_length = round(i.jj_length - random.random(), 3)
        s.commit()


def get_sorted() -> List[Dict]:
    """获取所有用户的jj长度, 并且按照从大到小排序"""
    with session() as s:
        return [
            {"userid": i.userid, "jj_length": i.jj_length}
            for i in s.query(UserData).order_by(UserData.jj_length.desc())
        ]
