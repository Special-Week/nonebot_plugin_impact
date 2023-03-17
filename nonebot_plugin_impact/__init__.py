import asyncio
from re import I
from random import choice
from nonebot.typing import T_State
from nonebot.params import CommandArg
from nonebot import on_command, on_regex
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.adapters.onebot.v11.permission import GROUP_OWNER, GROUP_ADMIN

from .utils import *
from .txt2img import txt_to_img

import pygal
from pygal.style import Style

suo = on_command("嗦牛子", priority=20, block=True)
dajiao = on_regex("^(打胶|开导)$", priority=20, block=True)
pk = on_command("pk", aliases={"对决"}, rule=rule, priority=20, block=False)
queryJJ = on_command("查询", priority=20, block=False)
JJrank = on_command(
    "jj排行榜", aliases={"jj排名", "jj榜单", "jjrank"}, priority=20, block=True)
rbqrank = on_command(
    "雌堕排行榜", aliases={"雌堕排名", "雌堕榜单", "rbqrank"}, priority=20, block=True)
openmodule = on_regex(r"^(开启银趴|禁止银趴)", permission=SUPERUSER |
                      GROUP_ADMIN | GROUP_OWNER, flags=I, priority=20, block=True)
yinPa = on_regex(r"^(日群友|透群友|日群主|透群主|日管理|透管理)",
                 flags=I, priority=20, block=True)
grass = on_regex(r"^/(被群友日|被群友透|被群主日|被群主透|被管理日|被管理透)", flags=I, priority=20, block=True)
queryinjection = on_command(
    "注入查询", aliases={"摄入查询", "射入查询"}, priority=20, block=True)
yinpaIntroduce = on_command("银趴介绍", priority=20, block=True)


@pk.handle()
async def _(event: GroupMessageEvent):
    if not (await check_group_allow(str(event.group_id))):
        await pk.finish(notAllow, at_sender=True)
    uid = event.get_user_id()  # 获取用户id, 类型为str
    allow = await PK_CD_check(uid)     # CD是否允许pk
    if not allow:       # 如果不允许pk, 则返回
        await pk.finish(f"你已经pk不动了喵，请等待{round(pkCDTime-(time.time() - pkCDData[uid]),3)}秒后再pk喵", at_sender=True)
    pkCDData.update({uid: time.time()})    # 更新CD时间
    at = await get_at(event)            # 获取at的id, 类型为str
    if at == uid:   # 如果at的id和uid相同, 则返回
        await pk.finish("你不能pk自己喵", at_sender=True)
    # rule规定了必须有at, 所以不用判断at是否为寄
    if uid in userdata and at in userdata:  # 如果两个都在userdata里面
        random_num = random.random()    # 生成一个随机数
        # 如果random_num大于0.5, 则胜利, 否则失败
        if random_num > 0.5:
            random_num = get_random_num()  # 重新生成一个随机数
            userdata.update(
                {uid: round(userdata[uid] + (random_num/2), 3)})  # 更新userdata
            # 更新userdata
            userdata.update({at: round(userdata[at] - random_num, 3)})
            write_user_data()    # 写入文件
            await pk.finish(f"对决胜利喵，你的{choice(JJvariable)}增加了{round(random_num/2,3)}cm喵，对面则在你的阴影笼罩下减小了{random_num}cm喵", at_sender=True)
        else:
            random_num = get_random_num()    # 重新生成一个随机数
            userdata.update(
                {uid: round(userdata[uid] - random_num, 3)})  # 更新userdata
            # 更新userdata
            userdata.update({at: round(userdata[at] + random_num/2, 3)})
            write_user_data()    # 写入文件
            await pk.finish(f"对决失败喵，在对面牛子的阴影笼罩下你的{choice(JJvariable)}减小了{random_num}cm喵，对面增加了{round(random_num/2,3)}cm喵", at_sender=True)
    else:
        # 谁不在userdata里面, 就创建谁
        if uid not in userdata:
            userdata.update({uid: 10})   # 创建用户
        if at not in userdata:
            userdata.update({at: 10})    # 创建用户
        write_user_data()     # 写入文件
        del pkCDData[uid]   # 删除CD时间
        await pk.finish(f"你或对面还没有创建{choice(JJvariable)}喵，咱全帮你创建了喵，你们的{choice(JJvariable)}长度都是10cm喵", at_sender=True)


@dajiao.handle()
async def _(event: GroupMessageEvent):
    if not (await check_group_allow(str(event.group_id))):
        await dajiao.finish(notAllow, at_sender=True)
    uid = event.get_user_id()   # 获取用户id, 类型为str
    allow = await CD_check(uid)    # CD是否允许打胶
    if not allow:   # 如果不允许打胶, 则返回
        await dajiao.finish(f"你已经打不动了喵，请等待{round(djCDtime-(time.time() - cdData[uid]),3)}秒后再打喵", at_sender=True)
    cdData.update({uid: time.time()})    # 更新CD时间
    if uid in userdata:    # 如果在userdata里面
        random_num = get_random_num()    # 生成一个随机数
        userdata.update(
            {uid: round(userdata[uid] + random_num, 3)})  # 更新userdata
        write_user_data()    # 写入文件
        await dajiao.finish(f"打胶结束喵，你的{choice(JJvariable)}很满意喵，长了{random_num}cm喵，目前长度为{userdata[uid]}cm喵", at_sender=True)
    else:
        userdata.update({uid: 10})   # 创建用户
        write_user_data()    # 写入文件
        del cdData[uid]     # 删除CD时间
        await dajiao.finish(f"你还没有创建{choice(JJvariable)}，咱帮你创建了喵，目前长度是10cm喵", at_sender=True)


@suo.handle()
async def _(event: GroupMessageEvent):
    if not (await check_group_allow(str(event.group_id))):
        await suo.finish(notAllow, at_sender=True)
    uid = event.get_user_id()   # 获取用户id, 类型为str
    allow = await suo_CD_check(uid)   # CD是否允许嗦
    if not allow:   # 如果不允许嗦, 则返回
        await suo.finish(f"你已经嗦不动了喵，请等待{round(suoCDTime-(time.time() - suoCDData[uid]),3)}秒后再嗦喵", at_sender=True)
    suoCDData.update({uid: time.time()})    # 更新CD时间
    at = await get_at(event)    # 获取at的用户id, 类型为str
    if at == "寄":  # 如果没有at
        if uid in userdata:   # 如果在userdata里面
            random_num = get_random_num()    # 生成一个随机数
            userdata.update(
                {uid: round(userdata[uid] + random_num, 3)})  # 更新userdata
            write_user_data()    # 写入文件
            await suo.finish(f"你的{choice(JJvariable)}很满意喵，嗦长了{random_num}cm喵，目前长度为{userdata[uid]}cm喵", at_sender=True)
        else:   # 如果不在userdata里面
            userdata.update({uid: 10})   # 创建用户
            write_user_data()    # 写入文件
            del suoCDData[uid]     # 删除CD时间
            await suo.finish(f"你还没有创建{choice(JJvariable)}喵，咱帮你创建了喵，目前长度是10cm喵", at_sender=True)
    else:
        if at in userdata:  # 如果在userdata里面
            random_num = get_random_num()    # 生成一个随机数
            # 更新userdata
            userdata.update({at: round(userdata[at] + random_num, 3)})
            write_user_data()    # 写入文件
            await suo.finish(f"对方的{choice(JJvariable)}很满意喵，嗦长了{random_num}cm喵，目前长度为{userdata[at]}cm喵", at_sender=True)
        else:
            userdata.update({at: 10})    # 创建用户
            write_user_data()    # 写入文件
            del suoCDData[uid]     # 删除CD时间
            await suo.finish(f"他还没有创建{choice(JJvariable)}喵，咱帮他创建了喵，目前长度是10cm喵", at_sender=True)


@queryJJ.handle()
async def _(event: GroupMessageEvent):
    if not (await check_group_allow(str(event.group_id))):
        await queryJJ.finish(notAllow, at_sender=True)
    uid = event.get_user_id()   # 获取用户id, 类型为str
    at = await get_at(event)    # 获取at的用户id, 类型为str
    if at == "寄":  # 如果没有at
        if uid in userdata:  # 如果在userdata里面
            await queryJJ.finish(f"你的{choice(JJvariable)}目前长度为{userdata[uid]}cm喵", at_sender=True)
        else:
            userdata.update({uid: 10})   # 创建用户
            write_user_data()    # 写入文件
            await queryJJ.finish(f"你还没有创建{choice(JJvariable)}喵，咱帮你创建了喵，目前长度是10cm喵", at_sender=True)
    else:   # 如果有at
        if at in userdata:  # 如果在userdata里面
            await queryJJ.finish(f"他的{choice(JJvariable)}目前长度为{userdata[at]}cm喵", at_sender=True)
        else:
            userdata.update({at: 10})    # 创建用户
            write_user_data()    # 写入文件
            await queryJJ.finish(f"他还没有创建{choice(JJvariable)}喵，咱帮他创建了喵，目前长度是10cm喵", at_sender=True)


@JJrank.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    if not (await check_group_allow(str(event.group_id))):
        await JJrank.finish(notAllow, at_sender=True)
    uid = event.get_user_id()   # 获取用户id, 类型为str
    rankdata = sorted(userdata.items(),
                      key=lambda x: x[1], reverse=True)   # 排序
    if len(rankdata) < 10:
        await JJrank.finish("目前记录的数据量小于10，无法显示rank喵")
    top = rankdata[:10]    # 取前10
    index = [i for i, x in enumerate(rankdata) if x[0] == uid]  # 获取用户排名
    if index == []:   # 如果用户没有创建JJ
        userdata.update({uid: 10})   # 创建用户
        write_user_data()    # 写入文件
        await JJrank.finish(f"你还没有创建{choice(JJvariable)}看不到rank喵，咱帮你创建了喵，目前长度是10cm喵", at_sender=True)
    # top的信息，然后获取其网名
    topinfo = [await bot.get_stranger_info(user_id=int(name[0])) for name in top]
    topnames = [name["nickname"] for name in topinfo]
    # 构造消息，手搓
    out: str = 'JJ排名：\n'
    view = pygal.Bar(style=Style(font_family='SimHei'))
    for i in range(10):
        index_str = convert_num_to_chinese(i+1)
        str_example = '第{index}名{chatdatanum}cm：{nickname}\n'.format(index=index_str,nickname=topnames[i],chatdatanum="{:.1f}".format(top[i][1]))
        out = out + str_example
        view.add(topnames[i], top[i][1])
    try:
        png: bytes = view.render_to_png()  # type: ignore
        reply2 = f"你的排名为{index[0] + 1}喵"
        await JJrank.finish(out + MessageSegment.image(png) + reply2, at_sender=True)
    except OSError:
        await JJrank.finish('GTK+(GIMP Toolkit) is not installed, the svg can not be transformed to png')

# 定义一个字典，存储数字和中文字符的对应关系
num_to_chinese = {1: "一", 2: "二", 3: "三", 4: "四", 5: "五", 6: "六", 7: "七", 8: "八", 9: "九", 10: "十"}

# 定义一个函数，把数字转换成中文字符
def convert_num_to_chinese(num):
    # 如果数字在字典中，直接返回对应的中文字符
    if num in num_to_chinese:
        return num_to_chinese[num]
    # 否则，返回空字符串
    else:
        return ""


@rbqrank.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    if not (await check_group_allow(str(event.group_id))):
        await JJrank.finish(notAllow, at_sender=True)
    uid = event.get_user_id()   # 获取用户id, 类型为str
    rankdata = sorted(ejaculation_data.items(), key=lambda x: x[1]['total'], reverse=True) # 排序
    if len(rankdata) < 10:
        await rbqrank.finish("目前记录的数据量小于10，无法显示rank喵")
    top = rankdata[:10]    # 取前10
    index = [i for i, x in enumerate(rankdata) if x[0] == uid]  # 获取用户排名
    # top的信息，然后获取其网名
    topinfo = [await bot.get_stranger_info(user_id=int(name[0])) for name in top]
    topnames = [name["nickname"] for name in topinfo]
    # 构造消息，手搓
    out: str = 'RBQ排名：\n'
    view = pygal.Pie(style=Style(font_family='SimHei'))
    for i in range(10):
        key, value = top[i]
        index_str = convert_num_to_chinese(i+1)
        str_example = '第{index}名{chatdatanum}ml：{nickname}\n'.format(index=index_str,nickname=topnames[i],chatdatanum="{:.1f}".format(value['total']))
        out = out + str_example
        view.add(topnames[i], value['total'])
    try:
        png: bytes = view.render_to_png()  # type: ignore
        reply2 = f"你还没有被注入喵" if index == [] else f"你的排名为{index[0] + 1}喵"
        await rbqrank.finish(out + MessageSegment.image(png) + reply2, at_sender=True)
    except OSError:
        await rbqrank.finish('GTK+(GIMP Toolkit) is not installed, the svg can not be transformed to png')


@yinPa.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    gid = event.group_id  # 群号
    uid = event.user_id   # 获取用户id, 类型为int
    if not (await check_group_allow(str(gid))):
        await JJrank.finish(notAllow, at_sender=True)
    allow = await fuck_CD_check(event)  # CD检查是否允许
    if not allow:
        await yinPa.finish(f"你已经榨不出来任何东西了，请先休息{round(fuckCDTime-(time.time() - ejaculation_CD[str(uid)]),3)}秒", at_sender=True)
    ejaculation_CD.update({str(uid): time.time()})  # 记录时间
    # 请求者的昵称
    req_user_card = await get_user_card(bot, group_id=int(gid), qid=int(uid))
    # 获取用户输入的参数
    args = list(state["_matched_groups"])
    command = args[0]
    # 获取群成员列表
    prep_list = await bot.get_group_member_list(group_id=gid)
    if "群友" in command:  # 如果发送的命令里面含有群友， 说明在透群友
        prep_list = [prep.get("user_id", 114514) for prep in prep_list]  # 群友列表
        target = await get_at(event)    # 获取消息有没有at
        if target == "寄":              # 没有的话
            # 随机抽取幸运成员
            prep_list.remove(uid)
            lucky_user = choice(prep_list)
            await yinPa.send(f"现在咱将随机抽取一位幸运裙友\n送给{req_user_card}色色！")
        else:                           # 有的话lucky user就是at的冷
            lucky_user = target
    elif "群主" in command:  # 如果发送的命令里面含有群主， 说明在透群主
        for prep in prep_list:  # 循环遍历群成员找到role是owner的角色，
            if prep['role'] == 'owner':
                lucky_user = prep['user_id']
                break
        if int(lucky_user) == uid:      # 如果群主是自己
            del ejaculation_CD[str(uid)]
            await yinPa.finish("你透你自己？")
        await yinPa.send(f"现在咱将把群主\n送给{req_user_card}色色！")
    elif "管理" in command:      # 如果发送的命令里面含有管理， 说明在透管理
        admin_id = []               # 空列表， 放管理的
        for prep in prep_list:  # 遍历， 找到管理就append
            if prep['role'] == 'admin':
                group_admin_id = prep['user_id']
                admin_id.append(group_admin_id)
        if uid in admin_id:         # 如果自己是管理的话， 移除自己
            admin_id.remove(uid)
        if admin_id == []:          # 如果没有管理的话, del cd信息， 然后finish
            del ejaculation_CD[str(uid)]
            await yinPa.finish("喵喵喵？找不到群管理！")
        lucky_user = choice(admin_id)   # random抽取一个管理
        await yinPa.send(f"现在咱将随机抽取一位幸运管理\n送给{req_user_card}色色！")
    # 获取群名片或者网名
    lucky_user_card = await get_user_card(bot, gid, int(lucky_user))
    # 1--100的随机数， 保留三位
    ejaculation = round(random.uniform(1, 100), 3)
    await update_ejaculation(ejaculation, str(lucky_user))
    await asyncio.sleep(2)  # 休眠2秒, 更有效果
    # 准备调用api, 用来获取头像椭偏
    url = f"http://q1.qlogo.cn/g?b=qq&nk={lucky_user}&s=640"
    repo_1 = f"好欸！{req_user_card} 用时{random.randint(1, 20)}秒给 {lucky_user_card} 注入了{ejaculation}毫升的脱氧核糖核酸，当日总注入量为：{get_today_ejaculation(str(lucky_user))}"
    await yinPa.send(repo_1 + MessageSegment.image(url))  # 结束

@grass.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    gid = event.group_id  # 群号
    uid = event.user_id   # 获取用户id, 类型为int
    if not (await check_group_allow(str(gid))):
        await JJrank.finish(notAllow, at_sender=True)
    allow = await fuck_CD_check(event)  # CD检查是否允许
    if not allow:
        await grass.finish(f"你已经进入贤者模式了，请先休息{round(fuckCDTime-(time.time() - ejaculation_CD[str(uid)]),3)}秒", at_sender=True)
    ejaculation_CD.update({str(uid): time.time()})  # 记录时间
    # 请求者的昵称
    req_user_card = await get_user_card(bot, group_id=int(gid), qid=int(uid))
    # 获取用户输入的参数
    args = list(state["_matched_groups"])
    command = args[0]
    # 获取群成员列表
    prep_list = await bot.get_group_member_list(group_id=gid)
    if "群友" in command:  # 如果发送的命令里面含有群友， 说明在透群友
        prep_list = [prep.get("user_id", 114514) for prep in prep_list]  # 群友列表
        target = await get_at(event)    # 获取消息有没有at
        if target == "寄":              # 没有的话
            # 随机抽取幸运成员
            prep_list.remove(uid)
            lucky_user = choice(prep_list)
            await grass.send(f"现在咱将随机抽取一位幸运裙友\n送给{req_user_card}色色！")
        else:                           # 有的话lucky user就是at的冷
            lucky_user = target
    elif "群主" in command:  # 如果发送的命令里面含有群主， 说明在透群主
        for prep in prep_list:  # 循环遍历群成员找到role是owner的角色，
            if prep['role'] == 'owner':
                lucky_user = prep['user_id']
                break
        if int(lucky_user) == uid:      # 如果群主是自己
            del ejaculation_CD[str(uid)]
            await grass.finish("你透你自己？")
        await grass.send(f"现在咱将把群主\n送给{req_user_card}色色！")
    elif "管理" in command:      # 如果发送的命令里面含有管理， 说明在透管理
        admin_id = []               # 空列表， 放管理的
        for prep in prep_list:  # 遍历， 找到管理就append
            if prep['role'] == 'admin':
                group_admin_id = prep['user_id']
                admin_id.append(group_admin_id)
        if uid in admin_id:         # 如果自己是管理的话， 移除自己
            admin_id.remove(uid)
        if admin_id == []:          # 如果没有管理的话, del cd信息， 然后finish
            del ejaculation_CD[str(uid)]
            await grass.finish("喵喵喵？找不到群管理！")
        lucky_user = choice(admin_id)   # random抽取一个管理
        await grass.send(f"现在咱将随机抽取一位幸运管理\n送给{req_user_card}色色！")
    # 获取群名片或者网名
    lucky_user_card = await get_user_card(bot, gid, int(lucky_user))
    # 1--100的随机数， 保留三位
    ejaculation = round(random.uniform(1, 100), 3)
    await update_ejaculation(ejaculation, str(uid))
    await asyncio.sleep(2)  # 休眠2秒, 更有效果
    # 准备调用api, 用来获取头像椭偏
    url = f"http://q1.qlogo.cn/g?b=qq&nk={lucky_user}&s=640"
    repo_1 = f"好欸！{req_user_card} 用时{random.randint(1, 20)}秒被 {lucky_user_card} 注入了{ejaculation}毫升的脱氧核糖核酸，当日总注入量为：{get_today_ejaculation(str(uid))}"
    await grass.send(repo_1 + MessageSegment.image(url))  # 结束


@queryinjection.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    if not (await check_group_allow(str(event.group_id))):
        await JJrank.finish(notAllow, at_sender=True)
    target = args.extract_plain_text()  # 获取命令参数
    user_id = event.get_user_id()   # 获取对象qq号， 类型string
    # 判断带不带at
    [object_id, replay1] = [await get_at(event), "该用户"] if await get_at(event) != "寄" else [user_id, "您"]
    if "历史" in target or "全部" in target:
        try:
            date = ejaculation_data[object_id]  # 对象不存在直接输出0
        except:
            await queryinjection.finish(f"{replay1}历史总被注射量为0ml")
        pic_string: str = ""            # 文字， 准备弄成图片
        for key in date:                # 遍历所有的日期
            if key != 'total':
                temp = date[key]["ejaculation"]
                pic_string += f"{key}\t\t{temp}\n"
        await queryinjection.finish(f"{replay1}历史总被注射量为{ejaculation_data[object_id]['total']}ml"+MessageSegment.image(txt_to_img(pic_string)))
    # 参数没有历史和全部的情况下， 只输出当天
    else:
        ejaculation = get_today_ejaculation(object_id)  # 获取对象当天的注入量
        await queryinjection.finish(f"{replay1}当日总被注射量为{ejaculation}ml")


@openmodule.handle()
async def _(event: GroupMessageEvent, state: T_State):
    gid = str(event.group_id)  # 群号
    # 获取用户输入的参数
    args = list(state["_matched_groups"])
    command = args[0]
    if "开启银趴" in command:
        if gid in groupdata:
            groupdata[gid]["allow"] = True
            write_group_data()
            await openmodule.finish("功能已开启喵")
        else:
            groupdata.update({gid: {"allow": True}})
            write_group_data()
            await openmodule.finish("功能已开启喵")
    elif "禁止银趴" in command:
        if gid in groupdata:
            groupdata[gid]["allow"] = False
            write_group_data()
            await openmodule.finish("功能已禁用喵")
        else:
            groupdata.update({gid: {"allow": False}})
            write_group_data()
            await openmodule.finish("功能已禁用喵")


@yinpaIntroduce.handle()
async def _(event:GroupMessageEvent):
    await yinpaIntroduce.send(MessageSegment.image(await plugin_usage()))
