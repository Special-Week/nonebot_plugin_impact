import os
import json
import time
import random
from nonebot.adapters.onebot.v11 import GroupMessageEvent


# 读取用户数据
if os.path.exists("data/impact/userdata.json"):  # 读取用户数据
    with open("data/impact/userdata.json", "r", encoding="utf-8") as f:
        userdata = json.load(f)
else:   # 不存在则创建
    if not os.path.exists("data/impact"):
        os.makedirs("data/impact")  # 创建文件夹
    userdata = {}
    with open("data/impact/userdata.json", "w", encoding="utf-8") as f:
        json.dump(userdata, f, indent=4)

# 读取群配置
if os.path.exists("data/impact/groupdata.json"):  # 读取用户数据
    with open("data/impact/groupdata.json", "r", encoding="utf-8") as f:
        groupdata = json.load(f)
else:   # 不存在则创建
    if not os.path.exists("data/impact"):
        os.makedirs("data/impact")  # 创建文件夹
    groupdata = {}
    with open("data/impact/groupdata.json", "w", encoding="utf-8") as f:
        json.dump(groupdata, f, indent=4)


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
    cd = time.time() - cdData[uid] if uid in cdData else CDtime+1
    return True if cd > CDtime else False


async def PK_CD_check(uid: str) -> bool:
    """pk冷却检查"""
    cd = time.time() - pkCDData[uid] if uid in pkCDData else pkCDTime+1
    return True if cd > pkCDTime else False


async def suo_CD_check(uid: str) -> bool:
    """嗦牛子冷却检查"""
    cd = time.time() - suoCDData[uid] if uid in suoCDData else suoCDTime+1
    return True if cd > suoCDTime else False


async def check_group_allow(gid: str) -> bool:
    """检查群是否允许"""
    if gid in groupdata:
        return groupdata[gid]["allow"]
    else:
        return False


def wirte_data() -> None:
    """写入用户数据"""
    with open("data/impact/userdata.json", "w", encoding="utf-8") as f:
        json.dump(userdata, f, indent=4)


def get_random_num():
    """获取随机数"""
    rand_num = random.random()
    rand_num = random.uniform(0, 1) if rand_num > 0.1 else random.uniform(1, 2)
    return round(rand_num, 3)


def wirte_group_data() -> None:
    """写入群配置"""
    with open("data/impact/groupdata.json", "w", encoding="utf-8") as f:
        json.dump(groupdata, f, indent=4)


notAllow = "群内还未开启淫趴游戏, 请管理员或群主发送\"开启淫趴\", \"禁止淫趴\"以开启/关闭该功能"
JJvariable = ["牛子", "牛牛", "丁丁", "JJ"]     # JJ变量
cdData = {}  # 冷却数据
CDtime = 300  # 冷却时间
pkCDData = {}   # pk冷却数据
pkCDTime = 60  # pk冷却时间
suoCDData = {}  # 嗦牛子冷却数据
suoCDTime = 300  # 嗦牛子冷却时间
