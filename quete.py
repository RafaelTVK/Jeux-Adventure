import json 
from AppConfig import *


# class qui va gérer les quetes

class QueteManager:
    def __init__(self) -> None:
        self.quetes = self.loadQuetes()
        pass
    
    def save(self):
        with open(QUETE,"w") as f:
            json.dump(self.quetes,f,indent=2)

    def loadQuetes(self):
        with open(QUETE,"r") as f:
            quetes:dict = json.load(f)
        return quetes
    
    def getQuetesNpc(self,npc):
        return self.quetes[npc] # {'queteNUM': [STATUT, 'BUT']}

    def getStateQuete(self,npc,quetename):
        return self.quetes[npc][quetename][0]
    
    def getText(self, npc):
        texts = []
        try:
            for i in self.quetes[npc]:
                texts.append(self.quetes[npc][i][1])
        except:
            pass
        return texts

    def getFinalText(self, npc, quetename):
        return self.quetes[npc][quetename][3]

    def getPoint(self,npc,quetename)->str:
        return self.quetes[npc][quetename][2]
    
    def changeStateQuete(self,npc,quetename):
        if not self.quetes[npc][quetename][0]:
            self.quetes[npc][quetename][0] = 1


if __name__=="__main__":

    q = QueteManager()
    q.getText("robin","")
    
    