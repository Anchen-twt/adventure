import sys
import random

from scene import Scene
from player import Player
from monster import Monster
from mechanism import Mechanism
from mechanism import key_door

class Game:
    def __init__(self):
        self.scenes = {
            'start': Scene('start', '你站在城堡门前', {'进入': 'hall'}),
            'hall': Scene('hall', '你进入到城堡大厅', {'北': 'dungeon', '东': 'treasure'}),
            'dungeon': Scene('dungeon', '你进入了地牢', {'南': 'hall'}, Monster('骷髅', 20, 3, ['钥匙'])),
            'treasure': Scene('treasure', '你进入了藏宝室', {}, None, '宝藏', key_door)
        }
 
        self.player = Player(100, 20, [])
 
    def play(self):
        # 提示信息
        print('操作提示:进入 东 西 南 北 搜刮 退出')
        # 显示初始场景信息
        current_scene = self.scenes[self.player.loc]
        print(current_scene.desc())
        while True:
            # 获取玩家输入的操作
            action = input(f'选择操作: ')
            # 根据操作执行事件                              
            # 移动            
            if current_scene.validate_movement(action):
                self.player.move(self.scenes, action)  
               
                # 更新current_scene
                current_scene = self.scenes[self.player.loc]
                print(current_scene.desc())
                
                # 如果有怪物
                if current_scene.monster:
                    # 战斗
                    self.fight_with_monster(self.player, current_scene.monster)     
                    continue
            
            # 捡取物品
            elif action == "搜刮":
                current_scene.pickup(self.player)   
            
            elif action == '退出':
                sys.exit()
            else:
                print('无效操作!')
                
            if self.check_game_over():
              print(f"你的最终生命值:{self.player.hp}")
              print(f"你的最终攻击力:{self.player.atk}")
              print(f"你的最终物品:{self.player.inventory}")
              break
    
    # 检查游戏是否结束
    def check_game_over(self):
      if '宝藏' in self.player.inventory:
        print("你找到了宝藏,游戏结束!") 
        return True
      elif self.player.hp <= 0:
        print("Wasted!")
      else:
        return False
        
    # 进行战斗
    def fight_with_monster(self, player, monster):
      while player.hp and monster.hp > 0:
        # 循环回合制
        monster.attack(player)
        player.attack(monster)
      
      # 如果击败怪物，设置当前场景没有怪物了
      if monster.hp <= 0:
        current_scene = self.scenes[self.player.loc]
        print(f'你击败了{current_scene.monster.name}')
        current_scene.monster = None
        
        # 随机选择一个战利品
        loot = random.choice(monster.drops)
        print(f'你获得了{loot}!')
        player.inventory.append(loot)


 
game = Game()
game.play()