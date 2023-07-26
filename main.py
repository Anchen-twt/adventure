import sys
import random
import pickle
import os

from scene import Scene
from player import Player
from monster import Monster
from mechanism import Mechanism

class Game:
    def __init__(self):
        # 定义场景 name, desc, exits, monster, item, mechanism
        self.scenes = {
            'start': Scene(
                'start', 
                '你站在城堡门前', 
            	   {'进入': 'hall'}
            ),
            
            'hall': Scene(
            	    'hall', 
            	    '你进入到城堡大厅', 
            	    {'北': 'dungeon', '东': 'treasure', '西': 'garden'}
            ),
            
            'garden':Scene(
            	   'garden', 
                '你进入了花园', 
                {'东': 'hall'},
                None,
                '红宝石吊坠'
            ),
            	    
            'dungeon': Scene(
                 'dungeon', 
                 '你进入了地牢', 
                 {'南': 'hall'}, 
                 Monster('骷髅', 105, 17, ['钥匙'])
            ),
            
            'treasure': Scene(
                 'treasure', 
                 '你进入了藏宝室', 
                 {}, 
                 None, 
                 '宝藏', 
                 Mechanism('钥匙之门','一扇上锁的铁门', ['钥匙'])
            )
        }
 
        self.player = Player(100, 20, [])
 
    def play(self):
        """启动游戏并处理用户输入"""
        # 提示信息
        print('操作提示:进入 东 西 南 北 搜刮\n保存 加载 清空存档\n退出\n')
        # 显示初始场景信息
        current_scene = self.scenes[self.player.loc]
        print(current_scene.desc())
        while True:
            # 获取玩家输入的操作
            action = input(f'选择操作: ')
            # 根据操作执行事件
            if action == '保存':
                self.save_game('/storage/emulated/0/qpython/冒险文本游戏/data/savegame.dat')
                print('游戏已保存!')
            elif action == '加载':
                game = Game.load_game('/storage/emulated/0/qpython/冒险文本游戏/data/savegame.dat')
                # 存档存在
                if game:
                    game.play()
                    break 
            elif action == '清空存档':
                self.delete_save('/storage/emulated/0/qpython/冒险文本游戏/data/savegame.dat')
                                             
            # 移动逻辑            
            elif current_scene.validate_movement(action):
                # 获取下一场景
                next_scene_name = current_scene.exits[action]   
                next_scene = self.scenes[next_scene_name]
                can_pass = True
                
                # 检查下一场景的机关
                if next_scene.mechanism:
                    # 有机关时更新can_pass
                    can_pass = next_scene.mechanism.can_pass(self.player)
                    
                    if not can_pass:
                        print(next_scene.mechanism.desc)
                        print("你无法通过这个机关!")
                    else:
                        # 通过机关
                        next_scene.mechanism.pass_mechanism(self.player)
                
                # 移动
                if can_pass:
                    self.player.move(self.scenes, action)  
               
                    # 更新current_scene
                    current_scene = next_scene
                    print(current_scene.desc())
                
                # 如果有怪物
                if current_scene.monster:
                    # 战斗
                    self.fight_with_monster(self.player, current_scene.monster)
                    # 检查玩家是否被击败
                    if not self.check_player_death():  
                      continue
                    else:
                      self.print_final_state()
                      break
            
            # 捡取物品
            elif action == "搜刮":
                current_scene.pickup(self.player)   
            
            elif action == '退出':
                sys.exit()
            else:
                print('无效操作!')
                
            if self.check_game_win():
              self.print_final_state()
              break
    
    def check_player_death(self):
      """检查玩家是否死亡"""
      if self.player.hp <= 0:
        print("Wasted!")
        return True
      else:
        return False
    
    def check_game_win(self):
      """检查游戏是否胜利"""
      if '宝藏' in self.player.inventory:
        print("你找到了宝藏,游戏结束!") 
        return True
      elif self.player.hp <= 0:
        print("Wasted!")
        return True
      else:
        return False
    
    def print_final_state(self):
      """游戏结束时输出玩家最终状态"""
      print(f"你的最终生命值:{self.player.hp}")
      print(f"你的最终攻击力:{self.player.atk}")
      print(f"你的最终物品:{self.player.inventory}")
        
    def fight_with_monster(self, player, monster):
      """处理玩家和一只怪物之间的战斗"""
      while player.hp and monster.hp > 0:
        # 怪物先手
        # 怪物回合
        monster.attack(player)
        if player.hp <= 0:
            # 玩家被击败
            print(f' 你被{monster.name}击败了!')
            break
            
        # 玩家回合 
        player.attack(monster)
        if monster.hp <= 0:
            # 怪物被击败
            current_scene = self.scenes[self.player.loc]
            print(f' 你击败了{current_scene.monster.name}')
            current_scene.monster = None
        
            # 随机选择一个战利品
            loot = random.choice(monster.drops)
            print(f' 你获得了{loot}!')
            player.inventory.append(loot)
    
    def save_game(self, filename):
        """存档"""
        with open(filename, 'wb') as f:
            pickle.dump(self, f)
    
    @staticmethod
    def load_game(filename):
        """读档"""
        try:
            with open(filename, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            print('存档不存在!')
            return None   
            
    def delete_save(self, filename):
        """删档"""
        if os.path.exists(filename):
            os.remove(filename)
            print('存档已清空!')
        else:
            print('存档不存在!')
    
if __name__ == '__main__':
  game = Game()
  game.play()