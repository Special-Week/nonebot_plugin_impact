import contextlib
from re import I

from nonebot import on_command, on_regex
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.permission import SUPERUSER

from .handle import impart
from .utils import utils

on_command(
    "pk",
    aliases={"对决"},
    rule=utils.rule,
    priority=20,
    block=False,
    handlers=[impart.pk],
)

on_regex(
    "^(打胶|开导)$", 
    priority=20, 
    block=True, 
    handlers=[impart.dajiao]
)

on_command(
    "嗦牛子", 
    priority=20, 
    block=True, 
    handlers=[impart.suo]
)

on_command(
    "查询", 
    priority=20, 
    block=False, 
    handlers=[impart.queryjj]
)

on_command(
    "jj排行榜",
    aliases={"jj排名", "jj榜单", "jjrank"},
    priority=20,
    block=True,
    handlers=[impart.jjrank],
)
on_regex(
    r"^(日群友|透群友|日群主|透群主|日管理|透管理)",
    flags=I,
    priority=20,
    block=True,
    handlers=[impart.yinpa],
)

on_regex(
    r"^(开始银趴|关闭银趴|开启淫趴|禁止淫趴|开启银趴|禁止银趴)",
    permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER,
    flags=I,
    priority=20,
    block=True,
    handlers=[impart.open_module],
)

on_command(
    "注入查询",
    aliases={"摄入查询", "射入查询"},
    priority=20,
    block=True,
    handlers=[impart.query_injection],
)

on_command(
    "淫趴介绍", 
    priority=20, 
    block=True,
    handlers=[impart.yinpa_introduce]
)

with contextlib.suppress(Exception):
    from nonebot.plugin import PluginMetadata

    __plugin_meta__ = PluginMetadata(
        name="impact",
        description="让群友们眼前一黑的nonebot2淫趴插件",
        usage=utils.usage,
        type="application",
        homepage="https://github.com/Special-Week/nonebot_plugin_impact",
        supported_adapters={"~onebot.v11"},
        extra={
            "author": "Special-Week",
            "version": "0.03.114514",
            "priority": 20,
        },
    )
