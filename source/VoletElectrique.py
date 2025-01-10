# -*- coding: utf-8 -*-


"======================================================================="
"========================= VoletElectrique =============================="
"======================================================================="

class VoletElectrique:
    "Simule un volet electrique"
    def __init__(self):
        self.isOpen = False
    def Open(self):
        if self.isOpen == False:
            self.isOpen = True
    def Close(self):
        if self.isOpen == True:
            self.isOpen = False
    def GetOpen(self):
        return self.isOpen

