import sys

from scene import Scene
from player import Player
from monster import Monster

class Game:
    def __init__(self):
        self.scenes = {
            'start': Scene('start', '你站在城堡门前', {'enter': 'hall'}),
            'hall': Scene('hall', '你进入到城堡大厅', {'north': 'dungeon', 'east': 'treasure'}),
            'dungeon': Scene('dungeon', '你进入了地牢', {'south': 'hall'}, Monster('Skeleton', 10, 2)),
            'treasure': Scene('treasure', '你获得了宝藏!', {})
        }
 
        self.player = Player(100, 20, [])
 
    def play(self):
        # 显示初始场景信息
        current_scene = self.scenes[self.player.loc]
        print(current_scene.desc())
        while True:
            # 获取玩家输入的操作
            action = input(f'选择操作: ')
            # 根据操作执行事件
            if current_scene.validate_action(action):
                self.player.move(self.scenes, action)
                current_scene = self.scenes[self.player.loc]
                print(current_scene.desc())
                # 如果有怪物
                if current_scene.monster:
                  # 战斗
                  self.fight_with_monster(self.player, current_scene.monster)     
                  continue
                  
            elif action == 'quit':
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
      if self.player.loc == 'treasure':
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


 
game = Game()
game.play()