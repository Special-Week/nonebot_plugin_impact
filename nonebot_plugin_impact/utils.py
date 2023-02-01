import os
import json
import time
import random
import nonebot
from nonebot.adapters.onebot.v11 import GroupMessageEvent,Bot


# 读取用户数据
if os.path.exists("data/impact/userdata.json"):  # 读取用户数据
    with open("data/impact/userdata.json", "r", encoding="utf-8") as f:
        userdata = json.load(f)
else:   # 不存在则创建
    if not os.path.exists("data/impact"):
        os.makedirs("data/impact")  # 创建文件夹
    userdata = {}
#此处不需要打开，删掉多余
# 读取群配置, 可能有人要问了, 为什么要搞两个json, 因为我自己的bot上个数据有多个用户数据, 我懒得合并了
if os.path.exists("data/impact/groupdata.json"):  # 读取用户数据
    with open("data/impact/groupdata.json", "r", encoding="utf-8") as f:
        groupdata = json.load(f)
else:   # 不存在则创建
    if not os.path.exists("data/impact"):
        os.makedirs("data/impact")  # 创建文件夹
    groupdata = {}

async def rule(event: GroupMessageEvent) -> bool:
    """rule检查, 是否有at"""
    msg = event.get_message()
    for msg_seg in msg:
        if msg_seg.type == "at":
            return True
    return False


async def get_at(event: GroupMessageEvent) -> str:
    """获取at的qq号, 不存在则返回寄, 类型为str"""
    msg = event.get_message()
    for msg_seg in msg:
        if msg_seg.type == "at":
            return str(msg_seg.data["qq"])
    return "寄"


async def CD_check(uid: str) -> bool:
    """冷却检查"""
    cd = time.time() - cdData[uid] if uid in cdData else djCDtime+1
    return True if cd > djCDtime else False


async def PK_CD_check(uid: str) -> bool:
    """pk冷却检查"""
    cd = time.time() - pkCDData[uid] if uid in pkCDData else pkCDTime+1
    return True if cd > pkCDTime else False


async def suo_CD_check(uid: str) -> bool:
    """嗦牛子冷却检查"""
    cd = time.time() - suoCDData[uid] if uid in suoCDData else suoCDTime+1
    return True if cd > suoCDTime else False

async def fuck_CD_check(uid:str)->bool:
    """透群友检查"""
    cd = time.time() - \
        ejaculation_CD[uid] if uid in ejaculation_CD else fuckCDTime+1
    return True if cd > fuckCDTime else False


async def check_group_allow(gid: str) -> bool:
    #检查群是否允许
    if gid not in groupdata:
        groupdata[gid] = {"allow": True}# 写入默认值为true
    return groupdata[gid]["allow"]


def write_data() -> None:
    """写入用户数据"""
    with open("data/impact/userdata.json", "w", encoding="utf-8") as f:
        json.dump(userdata, f, indent=4)


def get_random_num():
    """获取随机数"""
    rand_num = random.random()
    rand_num = random.uniform(0, 1) if rand_num > 0.1 else random.uniform(1, 2)
    return round(rand_num, 3)


def write_group_data() -> None:
    """写入群配置"""
    with open("data/impact/groupdata.json", "w", encoding="utf-8") as f:
        json.dump(groupdata, f, indent=4)


async def get_user_card(bot: Bot, group_id, qid):
    """返还用户nickname"""
    user_info: dict = await bot.get_group_member_info(group_id=group_id, user_id=qid)
    user_card = user_info["card"]
    if not user_card:
        user_card = user_info["nickname"]
    return user_card


notAllow = "群内还未开启淫趴游戏, 请管理员或群主发送\"开启淫趴\", \"关闭淫趴\"以开启/关闭该功能"
JJvariable = ["牛子", "牛牛", "丁丁", "JJ"]     # JJ变量
cdData = {}  # 冷却数据
pkCDData = {}   # pk冷却数据
suoCDData = {}  # 嗦牛子冷却数据
ejaculation_CD = {}  # 射精CD
config = nonebot.get_driver().config       # 获取配置
djCDtime:int = getattr(config, "djcdtime", 300)     # 打胶冷却时间
pkCDTime:int = getattr(config, "pkcdtime", 60)     # pk冷却时间
suoCDTime: int = getattr(config, "suocdtime", 300)     # 嗦牛子冷却时间
fuckCDTime: int = getattr(config, "fuckcdtime", 3600)     # 透群友冷却时间
