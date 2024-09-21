import anthill
import random
import networkx as nx
import collections
import matplotlib.pyplot as plt
import copy
import os
import cv2

def toload(load) :
    file = open(load,'r')
    lines = []
    line = file.readline()
    lines.append(line)
    while not line == "" :
        line = file.readline()
        if not line == "" :
            lines.append(line)
    startnode=anthill.node("v",float("inf"))
    nodes={}
    nodes["v"] = startnode
    ants=[]
    for line in lines :
        if line[0] == "f" :
            i=1
            while not line[i].isnumeric() :
                i=i+1
            f=int(line[i:len(line)])
            for j in range(f) :
                at=anthill.ant(j,startnode)
                ants.append(at)
                startnode.addant(at)
        if line[0] == "S" :
            n=""
            i=1
            name=""
            if not line[i] == "v" or line[i] == "d" :
                while line[i].isnumeric() :
                    name=name+line[i]
                    i=i+1
            else :
                name=line[i]
                i=i+1
            if name in nodes :
                n=nodes[name]
            else :
                n=anthill.node(name,1)
                print(name)
                nodes[name] = n
            while line[i] == " " :
                i=i+1
            if line[i] == "{" :
                i=i+1
                while line[i] == " " :
                    i=i+1
                num = ""
                while line[i].isnumeric() :
                    num=num+line[i]
                    i=i+1
                n.capacity=int(num)
            elif line[i] == "-" :
                i=i+1
                while line[i] == " " or line[i] == "S" :
                    i=i+1
                num = ""
                if line[i] == "d" :
                    num="d"
                else :
                    while line[i].isnumeric() :
                        num=num+line[i]
                        i=i+1
                        if not i<len(line) :
                            break
                if num in nodes :
                    n.addnext(nodes[num])
                else :
                    print("pas")
                    print(n.name)
                    print(num)
                    print(line)
                    nodes[num]=anthill.node(num,1)
                    n.addnext(nodes[num])
                if num == "d" :
                    endnode=nodes[num]
                    nodes[num].capacity = float('inf')
    if "" in nodes :
        n=nodes[""]
        del nodes[""]
        del n
    file.close()
    return ants,endnode,startnode

def generate(dir,antnum,room,maxcap,iteraco) :
    start = anthill.node("v",float('inf'))
    end = anthill.node('d',float("inf"))
    nodes=[]
    nodes.append(start)
    nodes.append(end)
    for i in range(room) :
        nodes.append(anthill.node(str(i),random.randint(1,maxcap)))
    j=2
    start.addnext(nodes[2])
    while j<(len(nodes)-1) :
        nodes[j].addnext(nodes[j+1])
        j=j+1
    nodes[len(nodes)-1].addnext(nodes[1])
    for i in range(iteraco) :
        node1=nodes[random.randint(0,len(nodes)-1)]
        node2=nodes[random.randint(0,len(nodes)-1)]
        node1.addnext(node2)
    file = open(dir,'x')
    file.write("f="+str(antnum)+'\n')
    for n in nodes :
        if n.name=="d" or n.name=="v" :
            file.write('S'+n.name+'\n')
        else :
            file.write('S'+n.name+" "+"{ "+str(n.capacity)+" }"+'\n')
        for m in n.next :
            file.write('S'+n.name+" "+"-"+" "+'S'+m.name+'\n')
    file.close()

def showgraph(nod) :
    G = nx.Graph()
    nodes={}
    nodes[nod.name]=nod
    explored=[]
    while len(nodes)>0 :
        nod=nodes[list(nodes.keys())[0]]
        explored.append(nod.name)
        G.add_node(nod.name)
        for n in nod.next :
            if not n.name in explored :
                G.add_node(n.name)
                G.add_edge(nod.name,n.name)
                nodes[n.name]=n
        del nodes[nod.name]
    return G
run = ""
while not run=="stop" :
    run = input("que souaité vous faire (stop,run,generate) : ")
    if run == "run" :
        load = input("entré la directory du fichier ")
        ants,endnode,startnode = toload(load)
        endnode.backprop()
        allend = False
        while not allend :
            allend = True
            for ant in ants :
                allend = allend and ant.n.name == "d"
                if ant.n.name == "" :
                    ant.n.removeant(ant)
                    ant.n=startnode
                    ant.previous="v"
            for ant in ants :
                ant.move()
        allpath={}
        file = open(load+"_ants.txt",'w')
        for ant in ants :
            print("trajet fourmis numéro : "+str(ant.index))
            print(str(ant.path))
            print(str(collections.Counter(ant.path)))
            file.write("trajet fourmis numéro : "+str(ant.index)+'\n')
            file.write(str(ant.path)+'\n')
            file.write(str(collections.Counter(ant.path))+'\n')
            file.write("longueur du chemin : "+str(len(ant.path))+'\n')
            allpath[ant.index]=ant.path
        file.close()
        G=showgraph(startnode)
        I=1
        pos=nx.spring_layout(G)
        refpos=pos
        size=[]
        index=0
        while len(allpath)>0 :
            labels={}
            listedge=[]
            for p in allpath :
                if not I<(len(allpath[p])-1) :
                    allpath[p]=[]
                else :
                    if allpath[p][I] == allpath[p][I+1] :
                        if allpath[p][I] in labels.keys() :
                            labels[allpath[p][I]]=labels[allpath[p][I]]+1
                        else :
                            labels[allpath[p][I]]=1
                    else :
                        listedge.append([(allpath[p][I],allpath[p][I+1])])
            colors = ['r','b','y','c']*len(listedge)
            for a in labels.keys() :
                labels[a]=a+"-fourmis "+str(labels[a])
            for n in G.nodes :
                b=''
                for c in n :
                    if c=='-' :
                        break
                    b=b+c
                print((b,n))
                if n not in labels.keys() :
                    if b in labels.keys() :
                        labels[n]=n
                    else :
                        labels[n]=b
            newlabels={}
            for n in G.nodes :
                b=''
                for c in n :
                    if c=='-' :
                        break
                    b=b+c
                for a in labels.keys() :
                    d=''
                    for c in a :
                        if c=='-' :
                            break
                        d=d+c
                    if b==d :
                        newlabels[n]=labels[a]
                        break
            newedge={}
            ne=[]
            n=0
            count=0
            for edge in listedge :
                isin=False
                for i in ne :
                    if i[0][0]==edge[0][0] and i[0][1]==edge[0][1] :
                        isin=True
                        break
                if isin :
                    newedge[ne.index(edge)]=newedge[ne.index(edge)]+1
                elif not isin :
                    ne.append(edge)
                    newedge[n]=1
                    n=n+1
            nx.relabel_nodes(G,newlabels,False)
            newpos={}
            for a in newlabels.keys() :
                newpos[newlabels[a]]=refpos[a]
                for i in range(len(ne)) :
                    ne[i]=[[ne[i][0][0],ne[i][0][1]]]
                    b=''
                    for c in newlabels[a] :
                        if not c=='-' :
                            b=b+c
                        else :
                            break
                    edge=ne[i]
                    if edge[0][0]==b :
                        edge[0][0]=newlabels[a]
                    if edge[0][1]==b :
                        edge[0][1]=newlabels[a]
            for a in pos.keys() :
                if not a in newlabels.keys() :
                    newpos[a]=pos[a]
            renamer={}
            for edge in newedge.keys() :
                b=''
                for c in ne[edge][0][0] :
                    if c=='-' :
                        break
                    b=b+c
                d=''
                for c in ne[edge][0][1] :
                    if c=='-' :
                        break
                    d=d+c
                renamer[(ne[edge][0][0],ne[edge][0][1])]="fourmis : "+str(newedge[edge])+" de : "+b+" vers : "+d
            for edge in newedge.keys() :
                val=(newedge[edge]*15)/len(ants)
                if val>0.4 :
                    newedge[edge]=(newedge[edge]*20)/len(ne)
                else :
                    newedge[edge]=0.4
            refpos=copy.deepcopy(newpos)
            print("edges")
            print(ne)
            nx.draw(G,newpos ,with_labels=True)
            nx.draw_networkx_edge_labels(G,newpos,renamer,0.5,10,rotate=False)
            for ed in range(len(ne)) :
                nx.draw_networkx_edges(G,newpos,edgelist=ne[ed],edge_color=colors[ed],width=newedge[ed],alpha=0.5,arrows=True)
            plt.savefig("temp/"+str(index)+".png")
            plt.close()
            keys=list(allpath.keys())
            for i in keys :
                if len(allpath[i])==0 :
                    del allpath[i]
            index=index+1
            I=I+1
        pic=os.listdir("temp")
        newpic=[]
        for i in range(len(pic)) :
            newpic.append(0)
        for i in range(len(pic)) :
            B=""
            for C in pic[i] :
                if C=='.' :
                    break
                B=B+C
            newpic[int(B)]=pic[i]
        pic=newpic
        frame = cv2.imread(os.path.join("temp", pic[0]))
        height, width, layers = frame.shape
        pa=input("quel doit être le nom de la vidéo ?")
        video = cv2.VideoWriter(pa+".avi", 0, 1, (width,height))
        for image in pic :
            video.write(cv2.imread(os.path.join("temp", image)))
        cv2.destroyAllWindows()
        video.release()
        for image in pic :
            os.remove(os.path.join("temp",image))
    if run=="generate" :
        dir=input("quel doit être la directory du fichier :")
        antnum=int(input("combient voulait vous de fourmis : "))
        room=int(input("quel doit être le nombre de sale : "))
        maxcap=int(input("quel doit être la capacité maximal : "))
        iteraco=int(input("combient de chance de génération de connection doit-il y avoir : "))
        generate(dir,antnum,room,maxcap,iteraco)
