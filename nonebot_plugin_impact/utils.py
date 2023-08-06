"""放一点工具函数"""
import random
import time
from typing import Union

import nonebot
from nonebot.adapters.onebot.v11 import GroupMessageEvent

from .txt2img import txt_to_img


class Utils:
    def __init__(self) -> None:
        """读取配置"""
        self.usage = """指令1: 嗦牛子 (给目标牛牛增加长度, 自己或者他人, 通过艾特选择对象, 没有at时目标是自己)
指令2: 打胶 | 开导 (给自己牛牛增加长度)
指令3: pk | 对决 (普通的pk,单纯的random实现输赢, 胜利方获取败方随机数/2的牛牛长度)
指令4: 查询 (目标牛牛长度, 自己或者他人, 通过艾特选择对象, 没有at时目标是自己)
指令5: jj排行榜 | jj排名 | jj榜单 | jjrank (字面意思, 输出倒数五位和前五位, 以及自己的排名)
指令6: 开始银趴 | 关闭银趴 | 开启淫趴 | 禁止淫趴 | 开启银趴 | 禁止银趴 (由管理员 | 群主 | SUPERUSERS开启或者关闭淫趴)
指令7: 日群友 | 透群友 | 日群主 | 透群主 | 日管理 | 透管理  (字面意思, 当使用透群友的时候如果at了人那么直接指定)
指令8: 注入查询 | 摄入查询 | 射入查询 (查询目标被透注入的量，后接(历史|全部), 可查看总被摄入的量, 无艾特的时候是自己, 有at的时候是目标)
指令9: 淫趴介绍  (输出淫趴插件的命令列表)"""
        self.not_allow = '群内还未开启淫趴游戏, 请管理员或群主发送"开启淫趴", "禁止淫趴"以开启/关闭该功能'  # 未开启该功能的send信息
        self.jj_variable = ["牛子", "牛牛", "丁丁", "JJ"]  # JJ变量
        self.cd_data = {}  # 冷却数据
        self.pk_cd_data = {}  # pk冷却数据
        self.suo_cd_data = {}  # 嗦牛子冷却数据
        self.ejaculation_cd = {}  # 射精CD
        config = nonebot.get_driver().config  # 获取配置
        self.dj_cd_time: int = getattr(config, "djcdtime", 300)  # 打胶冷却时间
        self.pk_cd_time: int = getattr(config, "pkcdtime", 60)  # pk冷却时间
        self.suo_cd_time: int = getattr(config, "suocdtime", 300)  # 嗦牛子冷却时间
        self.fuck_cd_time: int = getattr(config, "fuckcdtime", 3600)  # 透群友冷却时间

    @staticmethod
    async def rule(event: GroupMessageEvent) -> bool:
        """rule检查, 是否有at"""
        msg = event.get_message()
        return next(
            (msg_seg.data["qq"] != "all" for msg_seg in msg if msg_seg.type == "at"),
            False,
        )

    @staticmethod
    async def get_at(event: GroupMessageEvent) -> str:
        """获取at的qq号, 不存在则返回寄, 类型为str"""
        msg = event.get_message()
        return next(
            (
                "寄" if msg_seg.data["qq"] == "all" else str(msg_seg.data["qq"])
                for msg_seg in msg
                if msg_seg.type == "at"
            ),
            "寄",
        )

    async def cd_check(self, uid: str) -> bool:
        """打胶的冷却检查"""
        cd = (
            time.time() - self.cd_data[uid]
            if uid in self.cd_data
            else self.dj_cd_time + 1
        )
        return cd > self.dj_cd_time

    async def pkcd_check(self, uid: str) -> bool:
        """pk冷却检查"""
        cd = (
            time.time() - self.pk_cd_data[uid]
            if uid in self.pk_cd_data
            else self.pk_cd_time + 1
        )
        return cd > self.pk_cd_time

    async def suo_cd_check(self, uid: str) -> bool:
        """嗦牛子冷却检查"""
        cd = (
            time.time() - self.suo_cd_data[uid]
            if uid in self.suo_cd_data
            else self.suo_cd_time + 1
        )
        return cd > self.suo_cd_time

    async def fuck_cd_check(self, event: GroupMessageEvent) -> bool:
        """透群友检查"""
        uid = event.get_user_id()
        cd = (
            time.time() - self.ejaculation_cd[uid]
            if uid in self.ejaculation_cd
            else self.fuck_cd_time + 1
        )
        return (
            cd > self.fuck_cd_time
            or event.get_user_id() in nonebot.get_driver().config.superusers
        )

    @staticmethod
    def get_random_num() -> float:
        """获取随机数 0.1的概率是1-2随机获取, 剩下0.9是0-1"""
        rand_num = random.random()
        rand_num = random.uniform(0, 1) if rand_num > 0.1 else random.uniform(1, 2)
        return round(rand_num, 3)

    @staticmethod
    async def get_user_card(event: GroupMessageEvent) -> Union[None, str]:
        """返还用户nickname"""
        sender = event.sender
        return sender.card or sender.nickname

    async def plugin_usage(self) -> bytes:
        return await txt_to_img.txt_to_img(self.usage)


utils = Utils()
