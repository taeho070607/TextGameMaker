import os
from time import sleep
from random import randrange
import winsound
class road:
    map = [] # 10x10의 맵
    player = [0, 0]  # player = (x,y)
    door_list = None
    event = False
    content = None
    npc_list = None
    npc_m_list = None
    meeter = None
    meeter_x = None
    meeter_y = None
    enemy_status_list_dic = None
    sub_enemy_status_list_dic = None
    item_box_list = None
    damage = 0
    damaged = 0
    item_box_adress = None
    target = None
    player_status_dic = None
    enemy_list = None
    item = None
    skill = None
    armor_list = None
    weapon_list = None
    item_list = None
    effect = 0
    def load(self,map_name):
        with open(f"gamedata\\map\\{map_name}.txt","r",encoding="UTF8") as f:
            data = f.read()
            self.content = data.split("\n")
            self.map = self.content[:10]
            for i,x in zip(self.map,range(0,len(self.map))):
                self.map[x] = i.split(" ")
            npc_s = 0
            npc_e = 0
            for i, x in zip(self.content, range(0, len(self.content))):
                if i == "NPC":
                    npc_s = x
                if i == "NPC_end":
                    npc_e = x
            npc_list = []
            for i in self.content[npc_s + 1:npc_e]:
                i = i.split(" ")
                npc_list.append([str(i[0]), [int(i[1]), int(i[2])]])
            door_s = 0
            door_e = 0
            for i, x in zip(self.content, range(0, len(self.content))):
                if i == "door":
                    door_s = x
                if i == "door_end":
                    door_e = x
            door_list = []
            for i in self.content[door_s + 1:door_e]:
                i = i.split(" ")
                door_list.append([str(i[0]), [int(i[1]), int(i[2])],str(i[3])])
            self.door_list = door_list
            npc_m_list = []
            for i in npc_list:
                npc_m_list.append([i[0]])
            for i, x in zip(self.content, range(0, len(self.content))):
                for z, c in zip(npc_m_list, range(0, len(npc_m_list))):
                    if i == "ment_" + z[0]:
                        npc_m_list[c].append(x)
                    if i == "ment_" + z[0] + "_end":
                        npc_m_list[c].append(x)
            for i, x in zip(self.content, range(0, len(self.content))):
                for z, c in zip(npc_m_list, range(0, len(npc_m_list))):
                    if i == "question_" + z[0]:
                        npc_m_list[c].append(x)
                    if i == "question_" + z[0] + "_end":
                        npc_m_list[c].append(x)
            self.npc_list = npc_list
            self.npc_m_list = npc_m_list
            enemy_s = 0
            enemy_e = 0

            for i, x in zip(self.content, range(0, len(self.content))):
                if i == "ENEMY":
                    enemy_s = x
                if i == "ENEMY_end":
                    enemy_e = x
            enemy_list = []
            for i in self.content[enemy_s + 1:enemy_e]:
                i = i.split(" ")
                enemy_list.append([str(i[0]), [int(i[1]), int(i[2])]])
            enemy_adress_list = []
            for i in enemy_list:
                enemy_adress_list.append([i[0]])
            for i, x in zip(self.content, range(0, len(self.content))):
                for z, c in zip(enemy_adress_list, range(0, len(enemy_adress_list))):
                    if i == "ENEMY_" + z[0] + "_status":
                        enemy_adress_list[c].append(x)
                    if i == "ENEMY_" + z[0] + "_status_end":
                        enemy_adress_list[c].append(x)
            enemy_status_list = []
            for i in range(0, len(enemy_list)):
                k = [enemy_adress_list[i][0]]
                for c in self.content[enemy_adress_list[i][1] + 1:enemy_adress_list[i][2]]:
                    k.append(c.split(" ")[1])
                enemy_status_list.append(k)
            enemy_status_list_dic = []
            for i in enemy_status_list:
                enemy_status_list_dic.append({
                    "이름": i[0],
                    "체력": int(i[1]),
                    "공격력": int(i[2]),
                    "경험치": int(i[3]),
                    "돈": int(i[4]),
                    "방어력": int(i[5])
                })
        sub_enemy_status_list_dic = []
        for i in enemy_status_list:
            sub_enemy_status_list_dic.append({
                "이름": i[0],
                "체력": int(i[1]),
                "공격력": int(i[2]),
                "경험치": int(i[3]),
                "돈": int(i[4]),
                "방어력": int(i[5])
            })
        item_box_s = 0
        item_box_e = 0
        item_box_list = []
        for i, x in zip(self.content, range(0, len(self.content))):
            if i == "ITEM":
                item_box_s = x
            if i == "ITEM_end":
                item_box_e = x
        for i in self.content[item_box_s + 1:item_box_e]:
            i = i.split(" ")
            item_box_list.append([str(i[0]), [int(i[1]), int(i[2])], eval(i[3])])
        self.item_box_adress = [item_box_s,item_box_e]
        self.enemy_list = enemy_list
        self.enemy_status_list_dic = enemy_status_list_dic
        self.sub_enemy_status_list_dic = sub_enemy_status_list_dic
        self.item_box_list = item_box_list
    def load_armor(self):
        with open("gamedata\\armor\\armor_list.txt","r",encoding="UTF8") as f:
            self.armor_list = eval(f.read())
        with open("gamedata\\armor\\weapon_list.txt","r",encoding="UTF8") as f:
            self.weapon_list = eval(f.read())
    def load_status(self):
        with open("gamedata\\player.txt","r",encoding="UTF8") as f:
            self.player_status_dic = eval(f.read())
    def print_map(self):
        for i,k in zip(self.map[::-1],range(0,len(self.map))):
            s = ""
            for x in i:
                s = s + str(x) + "  "
            if k == 0:
                print(s + f"이번턴 총 공격량 : {self.damage}")
            elif k == 1:
                print(s + f"이번턴 총 피해량 : {self.damaged}")
            elif k == 9:
                print(s + f"플레이어 위치 : ({self.player[0]+1},{self.player[1]+1})")
            else:
                print(s)
    def load_item(self):
        with open("gamedata\\item.txt","r",encoding="UTF8") as f:
            self.item = eval(f.read())
        with open("gamedata\\item\\item__list.txt","r",encoding="UTF8") as f:
            self.item_list = eval(f.read())
    def draw_player(self, x, y):
        self.map[self.player[1]][self.player[0]] = "□"
        self.player = [self.player[0] + x, self.player[1] + y]
        self.map[self.player[1]][self.player[0]] = "P"
    def draw_entty(self,x,y,A):
        self.map[x][y] = A
    def chat(self,ment,target):
        print("대화상대 : " + target)
        print("대화 |")
        for i in ment:
            print(i)
        print("Y or N")
    def search(self,npc_name) -> int:
        for i,x in zip(self.npc_m_list,range(0,len(self.npc_m_list))):
            if i[0] == npc_name:
                return x
    def search_enemy(self,enemy_name) -> list:
        for i in self.enemy_list:
            if enemy_name == i[0]:
                return i[1]
    def search_enemy_var(self, enemy_name) -> int:
        for i,x in zip(self.enemy_status_list_dic,range(0,len(self.enemy_status_list_dic))):
            if i['이름'] == enemy_name:
                return x
    def status_tab(self):
        print(f"체력 : {self.player_status_dic['체력_max']}/{self.player_status_dic['체력']}")
        print(f"공격력 : {self.player_status_dic['공격력'] + self.player_status_dic['무기'][1]}(+{self.player_status_dic['무기'][1]})")
        print(f"방어력 : {self.player_status_dic['방어력'] + self.player_status_dic['방어구'][1]}(+{self.player_status_dic['방어구'][1]})")
        print(f"경험치 : {self.player_status_dic['경험치_max']}/{self.player_status_dic['경험치']}")
        print(f"돈 : {self.player_status_dic['돈']}")
        print(f"위치 : {self.player_status_dic['위치']}")
        print(f"방어구 : {self.player_status_dic['방어구'][0]}")
        print(f"무기 : {self.player_status_dic['무기'][0]}")
    def enemy_tab(self):
        for i in self.enemy_status_list_dic:
            if self.target == i['이름']:
                print(f"[{i['이름']}]<--selected")
            if self.target != i['이름']:
                print(f"[{i['이름']}]")
            print(f"체력 : {i['체력']}")
    def level_up(self):
        with open(f"gamedata\\levels\\level{self.player_status_dic['레벨'] + 1}.txt","r",encoding="UTF8") as f:
            level = eval(f.read())
        print("경험치가 올랐다!")
        print(f"레벨 : {self.player_status_dic['레벨']} -> {level['레벨']}")
        self.player_status_dic['레벨'] = level['레벨']
        print(f"최대체력 : {self.player_status_dic['체력_max']} -> {level['체력_max']}")
        self.player_status_dic['체력_max'] = level['체력_max']
        print(f"공격력 : {self.player_status_dic['공격력']} -> {level['공격력']}")
        self.player_status_dic['공격력'] = level['공격력']
        print(f"방어력 : {self.player_status_dic['방어력']} -> {level['방어력']}")
        self.player_status_dic['방어력'] = level['방어력']
        print(f"다음 레벨업 경험치 : {level['경험치_max']}")
        self.player_status_dic['경험치_max'] = level['경험치_max']
    def save(self):
        with open("gamedata\\player.txt","w",encoding="UTF8") as f:
            f.write(str(self.player_status_dic))
        with open("gamedata\\item.txt","w",encoding="UTF8") as f:
            f.write(str(self.item))
        with open("gamedata\\skill.txt","w",encoding="UTF8") as f:
            f.write(str(self.skill))
    def init_game(self):
        self.load(map_name="startmap")
        with open("gamedata\\init\\init_player.txt","r",encoding="UTF8") as f:
            self.player_status_dic = eval(f.read())
        with open("gamedata\\init\\init_item.txt","r",encoding="UTF8") as f:
            self.item = eval(f.read())
        with open("gamedata\\init\\init_skill.txt","r",encoding="UTF8") as f:
            self.skill = eval(f.read())
        self.save()
    def skill_turn(self):
        for i,x in zip(self.skill,range(0,len(self.skill))):
            if i['활성여부'] == True:
                if i['스킬이름'] == "TheWorld":
                    if not i['턴'] > 0:
                        for k in range(0,len(self.enemy_status_list_dic)):
                            self.enemy_status_list_dic[k]['공격력'] = 0
                            self.skill[x]['턴'] += 1
                    self.skill[x]['턴'] += 1
                    if i['턴'] >= i['최대턴']:
                        for f,g in zip(self.enemy_status_list_dic,range(0,len(self.enemy_status_list_dic))):
                            for e in self.sub_enemy_status_list_dic:
                                if f['이름'] == e['이름']:
                                    self.enemy_status_list_dic[g]['공격력'] = e['공격력']
                                    self.skill[x]['턴'] = 0
                                    self.skill[x]['활성여부'] = False
                if i['스킬이름'] == "보호막":
                    if not i['턴'] > 0:
                        self.player_status_dic['방어력'] += 5
                    self.skill[x]['턴'] += 1
                    if i['턴'] >= i['최대턴']:
                        self.player_status_dic['방어력'] = self.player_status_dic['방어력'] - 5
                        self.skill[x]['턴'] = 0
                        self.skill[x]['활성여부'] = False
                if i['스킬이름'] == "최후의일격":
                    if not i['턴'] > 0:
                        for k,l in zip(self.enemy_list,range(0,len(self.enemy_list))):
                            damage = 10
                            count = 0
                            if [self.player[1],self.player[0]+1] == k[1]:
                                count += 1
                                self.enemy_status_list_dic[self.search_enemy_var(k[0])]['체력'] -= damage
                            if [self.player[1]+1,self.player[0]] == k[1]:
                                count += 1
                                self.enemy_status_list_dic[self.search_enemy_var(k[0])]['체력'] -= damage
                            if [self.player[1],self.player[0]-1] == k[1]:
                                count += 1
                                self.enemy_status_list_dic[self.search_enemy_var(k[0])]['체력'] -= damage
                            if [self.player[1]-1,self.player[0]] == k[1]:
                                count += 1
                                self.enemy_status_list_dic[self.search_enemy_var(k[0])]['체력'] -= damage
                            if [self.player[1],self.player[0]] == k[1]:
                                count += 1
                                self.enemy_status_list_dic[self.search_enemy_var(k[0])]['체력'] -= damage
                            if count > 0:
                                self.damage += damage * count
                    self.skill[x]['턴'] += 1
                    if i['턴'] >= i['최대턴']:
                        self.skill[x]['턴'] = 0
                        self.skill[x]['활성여부'] = False
    def load_skill(self):
        with open("gamedata\\skill.txt","r",encoding="UTF8") as f:
            self.skill = eval(f.read())
    def load_all(self):
        self.map = []
        self.player = [0, 0]  # player = (x,y)
        self.door_list = None
        self.event = False
        self.content = None
        self.npc_list = None
        self.npc_m_list = None
        self.meeter = None
        self.meeter_x = None
        self.meeter_y = None
        self.enemy_status_list_dic = None
        self.sub_enemy_status_list_dic = None
        self.target = None
        self.player_status_dic = None
        self.enemy_list = None
        self.item = None
        self.skill = None
        self.armor_list = None
        self.load_armor() #gamedata\\armor\\armor_list.txt(방어구 목록)을 로드후 armor_list에저장
        self.load_skill() #gamedata\\skill.txt(보유중인 스킬목록을 로드)을 로드후 skill에 저장
        self.load_item() #gamedata\\item.txt(보유중인 아이템목을 로드)을 로드후 item에 저장
        self.load_status() #gamedata\\player.txt(플레이어의 스탯을 로드)을 로드후 player_status_dic에 저장
        self.load(self.player_status_dic['위치']) #gamedata\\map\\self.player_status_dic['위치'].txt(세이브된 플레이어의 맵 데이터)을 로드후 map,sub_enemy_status_list_dic,npc_list,npc_m_list,enemy_list,enemy_status_list_dic,content,door_list에 저장
    def map_save(self):
        with open(f"gamedata\\map\\{self.player_status_dic['위치']}.txt","w",encoding="UTF8") as f:
            for i in self.content:
                f.write(i + "\n")
new_road = road()
new_road.load_all()
new_road.draw_player(x=0, y=0)
while True:
    for i,x in zip(new_road.skill,range(0,len(new_road.skill))):
        if i['쿨여부'] and not i['활성여부']:
            if i['쿨턴'] <= i['쿨타임']:
                new_road.skill[x]['쿨턴'] += 1
            else:
                new_road.skill[x]['쿨턴'] =0
                new_road.skill[x]['쿨여부'] = False
    for i in new_road.skill:
        if i['활성여부']:
            if i['스킬이름'] == "최후의일격":
                if not new_road.player[1] == 9:
                    new_road.draw_entty(x=new_road.player[1]+1, y=new_road.player[0], A="■")
                if not new_road.player[0] == 9:
                    new_road.draw_entty(x=new_road.player[1], y=new_road.player[0]+1, A="■")
                if not new_road.player[1] == 0:
                    new_road.draw_entty(x=new_road.player[1]-1, y=new_road.player[0], A="■")
                if not new_road.player[0] == 0:
                    new_road.draw_entty(x=new_road.player[1], y=new_road.player[0]-1, A="■")
                new_road.effect += 1
    new_road.skill_turn()
    for i in new_road.enemy_list:
        new_road.draw_entty(x=i[1][0], y=i[1][1], A="□")
    for i in range(0,len(new_road.enemy_list)):
        change_random_x = randrange(-1, 2)
        change_random_y = randrange(-1, 2)
        if new_road.enemy_list[i][1][0] == 9:
            change_random_x = randrange(-1,1)
        if new_road.enemy_list[i][1][1] == 9:
            change_random_y = randrange(-1,1)
        if new_road.enemy_list[i][1][0] == 0:
            change_random_x = randrange(0,2)
        if new_road.enemy_list[i][1][1] == 0:
            change_random_y = randrange(0,2)
        new_road.enemy_list[i][1][0] += change_random_x
        new_road.enemy_list[i][1][1] += change_random_y
    if new_road.player_status_dic['체력'] >= new_road.player_status_dic['체력_max']:
        new_road.player_status_dic['체력'] = new_road.player_status_dic['체력_max']
    for i in new_road.enemy_list:
        A="E"
        if new_road.target == i[0]:
            A="T"
        new_road.draw_entty(x=i[1][0], y=i[1][1], A=A)
    for i in new_road.npc_list:
        new_road.draw_entty(x=i[1][1],y=i[1][0],A="N")
    for i in new_road.item_box_list:
        new_road.draw_entty(x=i[1][1],y=i[1][0],A="I")
    if new_road.enemy_status_list_dic == []:
        for i in new_road.npc_list:
            if i[1] == new_road.player:
                new_road.event = True
                new_road.meeter = i[0]
                new_road.meeter_x = i[1][1]
                new_road.meeter_y = i[1][0]
    for i in new_road.door_list:
        if i[1] == new_road.player:
            for x in range(0,len(new_road.skill)):
                new_road.skill[x]['활성여부'] = False
                new_road.skill[x]['쿨여부'] = False
                new_road.skill[x]['턴'] = 0
                new_road.skill[x]['쿨턴'] = 0
            new_road.load(i[2])
            new_road.player_status_dic['위치'] = i[2]
            new_road.draw_player(x=0, y=0)
    if new_road.enemy_status_list_dic != []:
        for i in new_road.enemy_status_list_dic:
            new_road.player_status_dic["체력"] = new_road.player_status_dic["체력"] - (i["공격력"] * (1 - (new_road.player_status_dic["방어력"] + new_road.player_status_dic["방어구"][1])/100))
            new_road.damaged += (i["공격력"] * (1 - (new_road.player_status_dic["방어력"] + new_road.player_status_dic["방어구"][1])/100))
        if new_road.target is not None:
            for i,x in zip(new_road.enemy_status_list_dic,range(0,len(new_road.enemy_status_list_dic))):
                if i["이름"] == new_road.target:
                    new_road.enemy_status_list_dic[x]["체력"] = new_road.enemy_status_list_dic[x]["체력"] - ((new_road.player_status_dic["공격력"] + new_road.player_status_dic["무기"][1]) * (1 - new_road.enemy_status_list_dic[x]["방어력"]/100))
                    new_road.damage += ((new_road.player_status_dic["공격력"] + new_road.player_status_dic["무기"][1]) * (1 - new_road.enemy_status_list_dic[x]["방어력"]/100))
        for i,x in zip(new_road.enemy_status_list_dic,range(0,len(new_road.enemy_status_list_dic))):
            if i["체력"] <= 0:
                new_road.player_status_dic["경험치"] += new_road.enemy_status_list_dic[x]["경험치"]
                new_road.player_status_dic["돈"] += new_road.enemy_status_list_dic[x]["돈"]
                new_road.draw_entty(x=new_road.search_enemy(i['이름'])[0],y=new_road.search_enemy(i['이름'])[1],A="□")
                new_road.enemy_status_list_dic.remove(i)
                for k,l in zip(new_road.enemy_list,range(0,len(new_road.enemy_list))):
                    if i["이름"] == k[0]:
                        del new_road.enemy_list[l]
                if new_road.target == i["이름"]:
                    new_road.target = None
    if new_road.player_status_dic['체력'] <= 0:
        print("============================")
        print("=          GameOver        =")
        print("============================")
        sleep(1)
        break
    os.system('cls')
    print()
    new_road.print_map()
    if new_road.effect == 1:
        if not new_road.player[1] == 9:
            new_road.draw_entty(x=new_road.player[1] + 1, y=new_road.player[0], A="□")
        if not new_road.player[0] == 9:
            new_road.draw_entty(x=new_road.player[1], y=new_road.player[0] + 1, A="□")
        if not new_road.player[1] == 0:
            new_road.draw_entty(x=new_road.player[1] - 1, y=new_road.player[0], A="□")
        if not new_road.player[0] == 0:
            new_road.draw_entty(x=new_road.player[1] , y=new_road.player[0]-1, A="□")
        new_road.effect = 0
    change = [0, 0]
    print("============================")
    if new_road.event:
        new_road.chat(ment=new_road.content[new_road.npc_m_list[new_road.search(new_road.meeter)][1]+1:new_road.npc_m_list[new_road.search(new_road.meeter)][2]],target=new_road.meeter)
        print("============================")
    new_road.status_tab()
    print("============================")
    if new_road.enemy_status_list_dic != []:
        new_road.enemy_tab()
        print("============================")
    if new_road.player_status_dic["경험치"] >= new_road.player_status_dic["경험치_max"]:
        new_road.level_up()
        print("============================")
    for i,k in zip(new_road.item_box_list,range(0,len(new_road.item_box_list))):
        if i[1] == new_road.player:
            if i[2] != []:
                for x in i[2]:
                    new_road.item.append(x)
                    print(f"{x}를 얻었다!!")
                new_road.item_box_list[k][2] = []
                item_save = []
                for x in new_road.item_box_list:
                    item_save.append(f"{x[0]} {x[1][0]} {x[1][1]} {str(x[2])}")
                for x in range(new_road.item_box_adress[0]+1,new_road.item_box_adress[1]):
                    new_road.content[x] = item_save[x - (new_road.item_box_adress[0] + 1)]
                new_road.map_save()
            else:
                print("상자는 비어있다.")
            print("============================")
    game_input = input(">")
    if not new_road.event:
        if game_input == "u" and new_road.player[1] is not 9:
            change[1] += 1
        elif game_input == "d" and new_road.player[1] is not 0:
            change[1] -= 1
        elif game_input == "r" and new_road.player[0] is not 9:
            change[0] += 1
        elif game_input == "l" and new_road.player[0] is not 0:
            change[0] -= 1
        elif game_input == "item":
            while True:
                os.system('cls')
                print("============================")
                for i in new_road.item:
                    for x in new_road.armor_list:
                        if i == x[0]:
                            print(x[0])
                            print("-" + x[3])
                    for x in new_road.weapon_list:
                        if i == x[0]:
                            print(x[0])
                            print("-" + x[3])
                    for x in new_road.item_list:
                        if i == x[0]:
                            print(x[0])
                            print("-" + x[3])
                print("============================")
                local_input = input(">")
                if "use" in local_input:
                    for i,x in zip(new_road.item,range(0,len(new_road.item))):
                        if local_input.split(" ")[1] == i:
                            for k in new_road.item_list:
                                if local_input.split(" ")[1] == k[0]:
                                    if local_input.split(" ")[1] == "붕대":
                                        print(f"{new_road.player_status_dic['체력']} -> {new_road.player_status_dic['체력'] + 20}")
                                        new_road.player_status_dic['체력'] += 20
                                        del new_road.item[x]
                                        break
                            for k in new_road.armor_list:
                                if local_input.split(" ")[1] == k[0]:
                                    if new_road.player_status_dic['방어구'][2] != None:
                                        new_road.skill.remove(new_road.player_status_dic['방어구'][2])
                                    if k[2] != None:
                                        new_road.skill.append(k[2])
                                    del new_road.item[x]
                                    new_road.item.append(new_road.player_status_dic['방어구'][0])
                                    new_road.player_status_dic['방어구'] = k
                                    break
                            for k in new_road.weapon_list:
                                if local_input.split(" ")[1] == k[0]:
                                    if new_road.player_status_dic['무기'][2] != None:
                                        new_road.skill.remove(new_road.player_status_dic['무기'][2])
                                    if k[2] != None:
                                        new_road.skill.append(k[2])
                                    del new_road.item[x]
                                    new_road.item.append(new_road.player_status_dic['무기'][0])
                                    new_road.player_status_dic['무기'] = k
                                    break
                if local_input == "exit":
                    break
        elif game_input == "skill":
            while True:
                os.system('cls')
                print("============================")
                for i in new_road.skill:
                    if i['쿨여부']:
                        print(i['스킬이름']+f" ({i['쿨타임']}/{i['쿨턴']})")
                    if not i['쿨여부']:
                        print(i['스킬이름'] + " (사용가능)")
                    print("-" + i['설명'])
                print("============================")
                local_input = input(">")
                if "use" in local_input:
                    for i,x in zip(new_road.skill,range(0,len(new_road.skill))):
                        if local_input.split(" ")[1] == i["스킬이름"]:
                            if local_input.split(" ")[1] == "TheWorld":
                                if not i["쿨여부"]:
                                    print("The World!! (스킬시전)")
                                    new_road.skill[x]['쿨여부'] = True
                                    new_road.skill[x]['활성여부'] = True
                            if local_input.split(" ")[1] == "보호막":
                                if not i["쿨여부"]:
                                    print("쉴드!! (스킬시전)")
                                    new_road.skill[x]['쿨여부'] = True
                                    new_road.skill[x]['활성여부'] =True
                            if local_input.split(" ")[1] == "최후의일격":
                                if not i["쿨여부"]:
                                    print("최후의 일격!! (스킬시전)")
                                    new_road.skill[x]['쿨여부'] = True
                                    new_road.skill[x]['활성여부'] =True
                        else:
                            print("존재하지않는 스킬입니다.")
                if local_input == "exit":
                    break
        elif game_input == "init_game":
            new_road.init_game()
        if game_input == "save":
            new_road.save()
            print("저장되었습니다!")
            sleep(1)
        if new_road.enemy_status_list_dic != []:
            if "target" in game_input:
                for i in new_road.enemy_status_list_dic:
                    if game_input.split(" ")[1] == i["이름"]:
                        new_road.target = i["이름"]
        else:
            pass
    while new_road.event:
        if game_input == "Y":
            print(new_road.content[new_road.npc_m_list[new_road.search(new_road.meeter)][3]+1:new_road.npc_m_list[new_road.search(new_road.meeter)][4]][0])
            change[0] -= 1
            sleep(1)
            break
        if game_input == "N":
            print(new_road.content[new_road.npc_m_list[new_road.search(new_road.meeter)][3] + 1:new_road.npc_m_list[new_road.search(new_road.meeter)][4]][1])
            change[0] -= 1
            sleep(1)
            break
        else:
            break
    new_road.draw_player(x=change[0], y=change[1])
    if new_road.event:
        new_road.draw_entty(x=new_road.meeter_x,y=new_road.meeter_y,A="N")
        new_road.event = False
        new_road.meeter = None
        new_road.meeter_x = None
        new_road.meeter_y = None
    #init
    new_road.damage = 0
    new_road.damaged = 0
    #sound
    winsound.Beep(150,250)