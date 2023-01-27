# nonebot_plugin_impact

让群友们眼前一黑的nonebot2淫趴插件 (牛牛比拼)



群友在群里开淫趴



响应器如下

```python
suo = on_command("嗦牛子", priority=5)
dajiao = on_regex("^(打胶|开导)$", priority=5)
pk = on_command("pk", aliases={"对决"}, rule=rule, priority=5)
queryJJ = on_command("查询", priority=5)
JJrank = on_command("jj排行榜", aliases={"jj排名", "jj榜单", "jjrank"}, priority=5)
```

指令1: 嗦牛子 (给目标牛牛增加长度, 自己或者他人, 通过艾特选择对象, 没有at时目标是自己)

指令2: 打胶 | 开导 (给自己牛牛增加长度)

指令3: pk | 对决 (普通的pk,单纯的random实现输赢吗胜利方获取败方随机数/2的牛牛长度)

指令4: 查询 (目标牛牛长度, 自己或者他人, 通过艾特选择对象, 没有at时目标是自己)

指令5: jj排行榜 | jj排名 | jj榜单 | jjrank (字面意思, 输出倒数五位和前五位, 以及自己的排名)