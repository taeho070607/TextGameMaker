from typing import List
import winsound
winsound.Beep(100,250)

with open("gamedata\\map\\huntingground.txt","r",encoding="UTF8") as f:
        x = f.read()
content = x.split("\n")
map = x.split("\n")
del map[10::]
npc_s=0
npc_e=0

for i,x in zip(content,range(0,len(content))):
        if i == "NPC":
                npc_s=x
        if i == "NPC_end":
                npc_e=x
npc_list = []
for i in content[npc_s+1:npc_e]:
        i = i.split(" ")
        npc_list.append([str(i[0]),[int(i[1]),int(i[2])]])
npc_m_list = []
for i in npc_list:
        npc_m_list.append([i[0]])
for i,x in zip(content,range(0,len(content))):
        for z,c in zip(npc_m_list,range(0,len(npc_m_list))):
                if i == "ment_" + z[0]:
                        npc_m_list[c].append(x)
                if i == "ment_" + z[0] + "_end":
                        npc_m_list[c].append(x)
for i,x in zip(content,range(0,len(content))):
        for z,c in zip(npc_m_list,range(0,len(npc_m_list))):
                if i == "question_" + z[0]:
                        npc_m_list[c].append(x)
                if i == "question_" + z[0] + "_end":
                        npc_m_list[c].append(x)

enemy_s=0
enemy_e=0

for i,x in zip(content,range(0,len(content))):
        if i == "ENEMY":
                enemy_s=x
        if i == "ENEMY_end":
                enemy_e=x
enemy_list = []
for i in content[enemy_s+1:enemy_e]:
        i = i.split(" ")
        enemy_list.append([str(i[0]),[int(i[1]),int(i[2])]])
enemy_adress_list = []
for i in enemy_list:
        enemy_adress_list.append([i[0]])
for i,x in zip(content,range(0,len(content))):
        for z,c in zip(enemy_adress_list,range(0,len(enemy_adress_list))):
                if i == "ENEMY_" + z[0] + "_status":
                        enemy_adress_list[c].append(x)
                if i == "ENEMY_" + z[0] + "_status_end":
                        enemy_adress_list[c].append(x)
enemy_status_list = []
for i in range(0,len(enemy_list)):
        k = [enemy_adress_list[i][0]]
        for c in content[enemy_adress_list[i][1]+1:enemy_adress_list[i][2]]:
                k.append(c.split(" ")[1])
        enemy_status_list.append(k)
enemy_status_list_dic :dict
for i in enemy_status_list:
        enemy_status_list_dic ={
                "??????" : i[0],
                "??????" : i[1],
                "?????????" : i[2],
                "?????????" : i[3],
                "???" : i[4],
                "?????????" : i[5]
        }
item_box_s = 0
item_box_e = 0
item_box_list = []
for i,x in zip(content,range(0,len(content))):
        if i == "ITEM":
                item_box_s = x
        if i == "ITEM_end":
                item_box_e = x
for i in content[item_box_s+1:item_box_e]:
        i = i.split(" ")
        item_box_list.append([str(i[0]),[int(i[1]),int(i[2])],eval(i[3])])
print(item_box_list)
print(enemy_status_list_dic)
print(enemy_status_list)