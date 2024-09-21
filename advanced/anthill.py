class node:

    def __init__(self,name,capacity):
        self.next = []
        self.isfull = False
        self.ants = []
        self.name = ""
        self.dist = float('inf')
        self.backproped = False
        self.name = name
        self.capacity = capacity
    def addant(self,ant) :
        self.ants.append(ant)
    def removeant(self,ant) :
        for i in range(len(self.ants)) :
            if self.ants[i].index == ant.index :
                print(len(self.ants))
                self.ants.pop(i)
                print(len(self.ants))
                break
    def backprop(self) :
        self.backproped = True
        if self.name=="" :
            self.dist=float('inf')
            return
        if self.name == "d" :
            self.dist = 0
        for n in self.next :
            if n.dist>self.dist+1 :
                n.dist = self.dist+1
        for n in self.next :
            if not n.backproped :
                n.backprop()
        print("exit "+self.name)
    def addnext(self,n) :
        print("addnext : "+self.name+" "+n.name)
        self.next.append(n)
        n.next.append(self)

class ant :

    def __init__(self,index,n) :
        self.path = []
        self.index=index
        self.n=n
        self.path.append(n.name)
        self.previous=n.name
        self.waitingturn=0
    def move(self) :
        if self.n.dist == 0 or self.n.name == "" :
            return 
        N =self.n
        weight = float('inf')
        blocked=[]
        for nod in self.n.next :
            if nod.capacity>len(nod.ants) :
                if nod.dist<=weight and not nod.name==self.previous :
                    N=nod
                    weight = nod.dist
            else :
                blocked.append(nod)
        non=float('inf')
        no=self.n
        a=0
        for ant in self.n.ants :
            if ant.index<self.index :
                a=a+1
        for nod in blocked :
            if (nod.ants[0].waitingturn+nod.dist)<non :
                non=nod.ants[0].waitingturn+nod.dist
                no=nod
        if self.n.name == N.name :
            print("bloqued ant :"+str(self.index)+" at "+self.n.name)
            if len(no.ants)>0 :
                self.waitingturn=self.waitingturn+no.ants[0].waitingturn+1
                self.previous=self.n
                self.path.append(self.n.name)
        else :
            if N.dist<=(non+1+a) :
                print("ant :"+str(self.index)+" nod "+N.name+" capacité "+str(N.capacity)+" fourmies "+str(len(N.ants ))+"dist :"+str(N.dist))
                self.n.removeant(self)
                N.addant(self)
                self.previous=self.n.name
                self.n=N
                self.path.append(self.n.name)
                self.waitingturn=0
            else :
                print("waiting ant :"+str(self.index)+" at "+self.n.name+"to go to "+no.name+" capacité "+str(no.capacity)+" fourmies "+str(len(no.ants ))+"dist :"+str(no.dist))
                self.waitingturn=self.waitingturn+no.ants[0].waitingturn
                self.path.append(self.n.name)
