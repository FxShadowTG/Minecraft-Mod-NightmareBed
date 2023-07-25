# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi
import random
ServerSystem = serverApi.GetServerSystemCls()
Factory = serverApi.GetEngineCompFactory()


class BadBedModServerSystem(ServerSystem):
    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        self.ListenEvent()
        self.levelId = "0"
        #创建在线玩家列表和字典
        self.playerIdList = []
        self.playerIdDict = {}
        #创建是否在睡觉字典
        self.playerSleepingDict = {}

        print("加载监听ok")

    def ListenEvent(self):
        #获取levelId
        self.levelId = serverApi.GetLevelId()
        #监听玩家是否睡觉成功事件
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), 'PlayerSleepServerEvent', self, self.OnPlayerSleepServerEvent)
        #监听玩家点击床方块事件
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), 'ServerBlockUseEvent', self, self.OnServerBlockUseEvent)
        #增加原版监听方块
        self.compByCreateBlockUseEventWhiteList = Factory.CreateBlockUseEventWhiteList(self.levelId)
        self.compByCreateBlockUseEventWhiteList.AddBlockItemListenForUseEvent("minecraft:bed:*")

        #监听玩家停止睡觉事件
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), 'PlayerStopSleepServerEvent', self, self.OnPlayerStopSleepServerEvent)
        #监听玩家加入事件
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), 'AddServerPlayerEvent', self, self.OnAddServerPlayerEvent)
        print("ListenEvent完毕")

    def OnAddServerPlayerEvent(self, args):
        playerId = args["id"]
        #把新玩家加进去
        #self.playerIdList.append(playerId)
        self.playerIdDict[playerId] = "null"
        self.playerSleepingDict[playerId] = 0

        #获取在线玩家的id列表
        #self.playerIdList = serverApi.GetPlayerList()

        # #查看玩家是否在字典中，如果没有就加进去
        # for player in self.playerIdList:
        #     if (player in self.playerIdDict.keys()) == False:
        #         self.playerIdDict.update({player: "null"})
        #         self.playerSleepingDict.update({player: "null"})
        print("新玩家追加后的玩家字典：",self.playerIdDict)
        print("新玩家追加后的玩家睡觉字典：",self.playerSleepingDict)

    #todo     #生成物品到背包而不是give
    def PlayerSleepServerLuckyEvent(self, playerId):
            #随机数1-100
            number = random.randint(1,100)
            print(number)
            compByFactory = Factory.CreateMsg(playerId)
            compByEffectFactory = Factory.CreateEffect(playerId)
            compByCreateCommand = Factory.CreateCommand(self.levelId)

            #校验玩家是否是手持梦魇石
            compByCreateItem = Factory.CreateItem(playerId)
            itemDict = compByCreateItem.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0)

            #如果有就将随机数直接设置为100
            if itemDict != None:
                if itemDict["newItemName"] == "ciomg:nightmare_stone":
                    compByFactory.NotifyOneMessage(playerId, "你感受到了梦魇石的力量...", "§d")
                    number = 100

            #给睡觉的人发送消息并执行对应操作
            if number >= 1 and number <= 30: #30%几率无事发生
                compByFactory.NotifyOneMessage(playerId, "昨晚睡得很香", "§b")

            elif number >= 31 and number <= 35: #5%几率生命恢复
                compByFactory.NotifyOneMessage(playerId, "心跳开始加速了", "§c")
                compByEffectFactory.AddEffectToEntity("regeneration", 600, 1, False)

            elif number >= 36 and number <= 40: #5%几率力量
                compByFactory.NotifyOneMessage(playerId, "浑身充满力量的一天", "§b")
                compByEffectFactory.AddEffectToEntity("strength", 600, 1, False)

            elif number >= 41 and number <= 50: #10%几率下暴雨
                compByFactory.NotifyOneMessage(playerId, "天空下起了暴雨...", "§c")
                compByCreateCommand.SetCommand("weather thunder")

            elif number >= 51 and number <= 60: #10%几率获得梦魇碎片
                compByFactory.NotifyOneMessage(playerId, "你在睡梦中收获了2个梦魇碎片", "§a")
                #定义物品词典
                nightmareFragmentDict = {
                    'itemName': 'ciomg:nightmare_fragment',
                    'count': 2,
                    'auxValue': 0,
                }
                compByCreateItem = Factory.CreateItem(playerId)
                compByCreateItem.SpawnItemToPlayerInv(nightmareFragmentDict, playerId)

            elif number >= 61 and number <= 65: #5%几率爆梦魇剑
                compByFactory.NotifyOneMessage(playerId, "你在睡梦中收获了1把梦魇剑", "§d")
                #定义物品词典
                nightmareSwordDict = {
                    'itemName': 'ciomg:nightmare_sword',
                    'count': 1,
                    'auxValue': 0,
                }
                compByCreateItem = Factory.CreateItem(playerId)
                compByCreateItem.SpawnItemToPlayerInv(nightmareSwordDict, playerId)

            elif number >= 66 and number <= 70: #5%几率爆梦魇镐
                compByFactory.NotifyOneMessage(playerId, "你在睡梦中收获了1把梦魇镐", "§d")
                #定义物品词典
                nightmarePickaxeDict = {
                    'itemName': 'ciomg:nightmare_pickaxe',
                    'count': 1,
                    'auxValue': 0,
                }
                compByCreateItem = Factory.CreateItem(playerId)
                compByCreateItem.SpawnItemToPlayerInv(nightmarePickaxeDict, playerId)

            elif number >= 71 and number <= 75: #5%几率爆梦魇斧
                compByFactory.NotifyOneMessage(playerId, "你在睡梦中收获了1把梦魇斧", "§d")
                #定义物品词典
                nightmareAxeDict = {
                    'itemName': 'ciomg:nightmare_axe',
                    'count': 1,
                    'auxValue': 0,
                }
                compByCreateItem = Factory.CreateItem(playerId)
                compByCreateItem.SpawnItemToPlayerInv(nightmareAxeDict, playerId)

            elif number >= 76 and number <= 80: #5%几率爆梦魇礼盒
                compByFactory.NotifyOneMessage(playerId, "你梦见了梦魇宝箱怪", "§c")
                compByCreateCommand.SetCommand("summon ciomg:nightmare_gift")

            elif number >= 81 and number <= 82: #2%几率爆钻石头盔
                compByFactory.NotifyOneMessage(playerId, "你在睡梦中收获了1个钻石头盔", "§d")
                #定义物品词典
                diamondHelmetDict = {
                    'itemName': 'minecraft:diamond_helmet',
                    'count': 1,
                    'auxValue': 0,
                }
                compByCreateItem = Factory.CreateItem(playerId)
                compByCreateItem.SpawnItemToPlayerInv(diamondHelmetDict, playerId)

            elif number >= 83 and number <= 84: #2%几率爆钻石胸甲
                compByFactory.NotifyOneMessage(playerId, "你在睡梦中收获了1个钻石胸甲", "§d")
                #定义物品词典
                diamondChestplateDict = {
                    'itemName': 'minecraft:diamond_chestplate',
                    'count': 1,
                    'auxValue': 0,
                }
                compByCreateItem = Factory.CreateItem(playerId)
                compByCreateItem.SpawnItemToPlayerInv(diamondChestplateDict, playerId)

            elif number >= 85 and number <= 86: #2%几率爆钻石护腿
                compByFactory.NotifyOneMessage(playerId, "你在睡梦中收获了1个钻石护腿", "§d")
                #定义物品词典
                diamondLeggingsDict = {
                    'itemName': 'minecraft:diamond_leggings',
                    'count': 1,
                    'auxValue': 0,
                }
                compByCreateItem = Factory.CreateItem(playerId)
                compByCreateItem.SpawnItemToPlayerInv(diamondLeggingsDict, playerId)

            elif number >= 87 and number <= 88: #2%几率爆钻石靴子
                compByFactory.NotifyOneMessage(playerId, "你在睡梦中收获了1个钻石靴子", "§d")
                #定义物品词典
                diamondBootsDict = {
                    'itemName': 'minecraft:diamond_boots',
                    'count': 1,
                    'auxValue': 0,
                }
                compByCreateItem = Factory.CreateItem(playerId)
                compByCreateItem.SpawnItemToPlayerInv(diamondBootsDict, playerId)

            elif number >= 89 and number <= 90: #2%几率爆图腾
                compByFactory.NotifyOneMessage(playerId, "你在睡梦中收获了1个图腾", "§d")
                #定义物品词典
                TotemDict = {
                    'itemName': 'minecraft:totem',
                    'count': 1,
                    'auxValue': 0,
                }
                compByCreateItem = Factory.CreateItem(playerId)
                compByCreateItem.SpawnItemToPlayerInv(TotemDict, playerId)

            elif number >= 91 and number <= 95: #5%几率爆钻石
                compByFactory.NotifyOneMessage(playerId, "你在睡梦中收获了2颗钻石", "§d")
                #定义物品词典
                diamondDict = {
                    'itemName': 'minecraft:diamond',
                    'count': 2,
                    'auxValue': 0,
                }
                compByCreateItem = Factory.CreateItem(playerId)
                compByCreateItem.SpawnItemToPlayerInv(diamondDict, playerId)

            elif number >= 96 and number <= 99: #4%几率速掘
                compByFactory.NotifyOneMessage(playerId, "糟糕！麒麟臂发作了", "§e")
                compByEffectFactory.AddEffectToEntity("haste", 600, 1, False)

            elif number == 100: #1%几率进入末地
                compByFactory.NotifyOneMessage(playerId, "你昏睡了过去", "§d")
                
                #给玩家加上抵抗效果防止摔死
                compByEffectFactory.AddEffectToEntity("resistance", 12, 255, False)

                #把玩家传送到末地
                compByCreateDimension = Factory.CreateDimension(playerId)
                compByCreateDimension.ChangePlayerDimension(2,(0,100,0))
            
        #监听玩家是否停止了睡觉
    def OnPlayerStopSleepServerEvent(self, args):
        playerId = args["playerId"]
        #停止了睡觉就改回状态
        self.playerSleepingDict[playerId] = 0
        #校验是否是白天，如果不是白天说明没睡醒就离开床
        compByCreateTime = Factory.CreateTime(self.levelId)
        # 从游戏开始经过的总帧数
        passedTime = compByCreateTime.GetTime()
        # 当前游戏天内的帧数
        timeOfDay = passedTime % 24000  #睡醒一般是0

        if timeOfDay <= 100:
            return

        #拿到起床玩家的最后一次睡的床的坐标
        playerLastPos = self.playerIdDict[playerId]
        #检查该坐标是否为黑色的床
        compByCreateBlockInfo = Factory.CreateBlockInfo(playerId)
        color = compByCreateBlockInfo.GetBedColor(playerLastPos)

        if color == 0:
        #if玩家停止睡觉:清除床方块and中毒反胃失明and爆炸
            print("用户离开了黑床")
            compByCreateCommand = Factory.CreateCommand(self.levelId)

            compByFactory = Factory.CreateMsg(playerId)
            compByFactory.NotifyOneMessage(playerId, "你惹到了梦魇，受到了惩罚", "§c")

            #清除床方块
            PosX = str(playerLastPos[0])
            PosY = str(playerLastPos[1])
            PosZ = str(playerLastPos[2])
            cmd = "setblock" + " " + PosX + " " + PosY + " " + PosZ + " " + "air"
            compByCreateCommand.SetCommand(cmd)

            #中毒反胃失明
            compByCreateCommand.SetCommand("effect @s fatal_poison 15 1 true")
            compByCreateCommand.SetCommand("effect @s nausea 15 255 true")
            compByCreateCommand.SetCommand("effect @s blindness 15 255 true")
            
            #发生爆炸
            compByCreateCommand.SetCommand("execute @s ~~~ summon tnt")


    #监听玩家是否在睡觉
    def OnPlayerSleepServerEvent(self, args):
        #如果在睡觉则在字典里打上1
        playerId = args["playerId"]
        self.playerSleepingDict[playerId] = 1


    #监听玩家点击的方块
    def OnServerBlockUseEvent(self, args):
        playerId = args["playerId"]

        #假设把玩家是否在睡觉设置为0
        self.playerSleepingDict[playerId] = 0

        #增加原版监听方块
        compByCreateBlockUseEventWhiteList = Factory.CreateBlockUseEventWhiteList(self.levelId)
        compByCreateBlockUseEventWhiteList.AddBlockItemListenForUseEvent("minecraft:bed:*")

        #校验玩家是否在睡觉并执行相关操作
        def checkPlayerSleepingAndOperation(self, playerId):
            print("checkPlayerSleeping...")
            #正在睡觉
            if self.playerSleepingDict[playerId] == 1:
                #获取玩家点击床的坐标
                playerPos = [args["x"],args["y"],args["z"]]
                print(playerPos)

                 #检查该坐标是否为黑色的床
                compByCreateBlockInfo = Factory.CreateBlockInfo(playerId)
                color = compByCreateBlockInfo.GetBedColor(playerPos)

                #校验玩家是否在改该坐标r=2内
                compByCreateName = Factory.CreateName(playerId)
                playerName = compByCreateName.GetName()
                compByCreateCommand = Factory.CreateCommand(self.levelId)
                result = compByCreateCommand.SetCommand("testfor" + " @a[" + "name=" + playerName + ",x=" + str(args["x"]) + ",y=" + str(args["y"]) + ",z=" + str(args["z"]) + ",r=4]")
                
                
                if result == False:
                    return

                if color == 0:
                    print("colorTrue")
                    #更新最后一次睡觉的床的坐标
                    self.playerIdDict[playerId] = playerPos
                    #调用随机事件
                    self.PlayerSleepServerLuckyEvent(playerId)
            else:
                return

        #延时调用相关操作
        compByCreateGame = Factory.CreateGame(self.levelId)
        compByCreateGame.AddTimer(0.2, checkPlayerSleepingAndOperation, self, playerId)

        blockName = args["blockName"]
        aux = str(args["aux"])
        print("触发点击" + blockName + aux)

    def UnListenEvent(self):
        self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), 'PlayerSleepServerEvent', self, self.OnPlayerSleepServerEvent)
        self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), 'ServerBlockUseEvent', self, self.OnServerBlockUseEvent)
        self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), 'PlayerStopSleepServerEvent', self, self.OnPlayerStopSleepServerEvent)
        self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), 'AddServerPlayerEvent', self, self.OnAddServerPlayerEvent)
        self.compByCreateBlockUseEventWhiteList.RemoveBlockItemListenForUseEvent("minecraft:bed:*")

    def Destroy(self):
        self.UnListenEvent()
        pass