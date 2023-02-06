import os
import json
import time
import random
import nonebot
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot


def write_group_data() -> None:
    """写入群配置"""
    with open("data/impact/groupdata.json", "w", encoding="utf-8") as f:
        json.dump(groupdata, f, indent=4)


def write_user_data() -> None:
    """写入用户数据"""
    with open("data/impact/userdata.json", "w", encoding="utf-8") as f:
        json.dump(userdata, f, indent=4)


def write_ejaculation_data() -> None:
    """写入注入数据"""
    with open("data/impact/ejaculation_data.json", "w", encoding="utf-8") as f:
        json.dump(ejaculation_data, f, indent=4)


# 读取用户数据
if os.path.exists("data/impact/userdata.json"):  # 读取用户数据
    with open("data/impact/userdata.json", "r", encoding="utf-8") as f:
        userdata = json.load(f)
else:   # 不存在则创建
    if not os.path.exists("data/impact"):
        os.makedirs("data/impact")  # 创建文件夹
    userdata = {}
    write_user_data()
# json结构
# {
#     "user_id":int
# }



# 读取群配置, 可能有人要问了, 为什么要搞这么多个json, 因为我自己的bot上个数据有多个用户数据, 我懒得合并了
if os.path.exists("data/impact/groupdata.json"):  # 读取用户数据
    with open("data/impact/groupdata.json", "r", encoding="utf-8") as f:
        groupdata = json.load(f)
else:   # 不存在则创建
    if not os.path.exists("data/impact"):
        os.makedirs("data/impact")  # 创建文件夹
    groupdata = {}
    write_group_data()
# json结构
# {
#     "group_id": {
#         "allow": true|false
#     }
# }


# 读取用户被精液注入的量, 重构上面的json好麻烦, 新建一个json
if os.path.exists("data/impact/ejaculation_data.json"):  # 读取数据
    with open("data/impact/ejaculation_data.json", "r", encoding="utf-8")as f:
        ejaculation_data = json.load(f)
else:  # 不存在就创建
    if not os.path.exists("data/impact"):
        os.makedirs("data/impact")  # 创建文件夹
    ejaculation_data = {}
    write_ejaculation_data()
# 这种结构, 不想重构也不想新建json了， 所以放宽了这么多
# {
#     "user_id": {
#         "date": {
#             "ejaculation": 123
#         }
#     }
# }


async def rule(event: GroupMessageEvent) -> bool:
    """rule检查, 是否有at"""
    msg = event.get_message()
    for msg_seg in msg:
        if msg_seg.type == "at":
            if msg_seg.data["qq"] == "all":
                return False
            return True
    return False


async def get_at(event: GroupMessageEvent) -> str:
    """获取at的qq号, 不存在则返回寄, 类型为str"""
    msg = event.get_message()
    for msg_seg in msg:
        if msg_seg.type == "at":
            if msg_seg.data["qq"] == "all":
                return "寄"
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


async def fuck_CD_check(event: GroupMessageEvent) -> bool:
    """透群友检查"""
    uid = event.get_user_id()
    cd = time.time() - \
        ejaculation_CD[uid] if uid in ejaculation_CD else fuckCDTime+1
    return True if (cd > fuckCDTime or event.get_user_id() in nonebot.get_driver().config.superusers) else False


async def check_group_allow(gid: str) -> bool:
    """检查群是否允许"""
    if gid in groupdata:
        return groupdata[gid]["allow"]
    else:
        return False


def get_today() -> str:
    """获取当前年月日  2023-02-04  """
    today = time.strftime("%Y-%m-%d", time.localtime())
    return today


async def update_ejaculation(ejaculation: float, lucky_user: str) -> None:
    """更新ejaculation_data数据并且写入json"""
    if lucky_user in ejaculation_data:
        target_dict = ejaculation_data[lucky_user]
        target_dict.update({
            get_today(): {
                "ejaculation": ejaculation
            }
        })
        ejaculation_data.update({str(lucky_user):target_dict})
    else:
        target_dict = {str(lucky_user): {
            get_today(): {
                "ejaculation": ejaculation
            }}
        }
        ejaculation_data.update(target_dict)
    write_ejaculation_data()


def get_today_ejaculation(user_id: str) -> float:
    """获取当日注入的量"""
    try:
        return ejaculation_data[str(user_id)][get_today()]["ejaculation"]  # 尝试获取, json没有的话就返回0
    except:
        return 0


def get_random_num() -> float:
    """获取随机数 0.1的概率是1-2随机获取, 剩下0.9是0-1"""
    rand_num = random.random()
    rand_num = random.uniform(0, 1) if rand_num > 0.1 else random.uniform(1, 2)
    return round(rand_num, 3)


async def get_user_card(bot: Bot, group_id, qid) -> str:
    """返还用户nickname"""
    user_info: dict = await bot.get_group_member_info(group_id=group_id, user_id=qid)
    user_card = user_info["card"]
    if not user_card:
        user_card = user_info["nickname"]
    return user_card


notAllow = "群内还未开启淫趴游戏, 请管理员或群主发送\"开启淫趴\", \"禁止淫趴\"以开启/关闭该功能"  # 未开启该功能的send信息
JJvariable = ["牛子", "牛牛", "丁丁", "JJ"]     # JJ变量
cdData = {}  # 冷却数据
pkCDData = {}   # pk冷却数据
suoCDData = {}  # 嗦牛子冷却数据
ejaculation_CD = {}  # 射精CD
config = nonebot.get_driver().config       # 获取配置
djCDtime: int = getattr(config, "djcdtime", 300)     # 打胶冷却时间
pkCDTime: int = getattr(config, "pkcdtime", 60)     # pk冷却时间
suoCDTime: int = getattr(config, "suocdtime", 300)     # 嗦牛子冷却时间
fuckCDTime: int = getattr(config, "fuckcdtime", 3600)     # 透群友冷却时间
