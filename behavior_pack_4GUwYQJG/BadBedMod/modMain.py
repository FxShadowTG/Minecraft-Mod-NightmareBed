# -*- coding: utf-8 -*-

from mod.common.mod import Mod
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi

@Mod.Binding(name="BadBedMod", version="0.0.1")
class BadBedMod(object):

    def __init__(self):
        pass

    @Mod.InitServer()
    def BadBedModServerInit(self):
        print("server注册中")
        serverApi.RegisterSystem("BadBedMod","BadBedModServerSystem","BadBedMod.BadBedModServerSystem.BadBedModServerSystem")
        print("===服务端注册完毕===")

    @Mod.DestroyServer()
    def BadBedModServerDestroy(self):
         print("===服务端销毁完毕===")

    @Mod.InitClient()
    def BadBedModClientInit(self):
        clientApi.RegisterSystem("BadBedMod","BadBedModClientSystem","BadBedMod.BadBedModClientSystem.BadBedModClientSystem")
        print("===客户端注册完毕===")

    @Mod.DestroyClient()
    def BadBedModClientDestroy(self):
        print("===客户端销毁完毕===")
