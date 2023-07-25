# -*- coding: utf-8 -*-

from common.mod import Mod


@Mod.Binding(name="Script_NeteaseModz6RrjjwO", version="0.0.1")
class Script_NeteaseModz6RrjjwO(object):

    def __init__(self):
        pass

    @Mod.InitServer()
    def Script_NeteaseModz6RrjjwOServerInit(self):
        pass

    @Mod.DestroyServer()
    def Script_NeteaseModz6RrjjwOServerDestroy(self):
        pass

    @Mod.InitClient()
    def Script_NeteaseModz6RrjjwOClientInit(self):
        pass

    @Mod.DestroyClient()
    def Script_NeteaseModz6RrjjwOClientDestroy(self):
        pass
