class Scene:
     def __init__(self, name, desc, exits, monster=None, item=None):
         self.name = name
         self.base_desc = desc
         self.exits = exits
         self.monster = monster
         self.item = item
     
     # 根据有无怪物输出不同desc
     def desc(self):
         if self.monster:
           return f'{self.base_desc} \n 这里有怪物! \n 你遇到了{self.monster.name}'
         else:
           return self.base_desc
      
     # 检查移动命令是否合法   
     def validate_action(self, action):
         if action in self.exits:
           return True
         else:
           return False
           
     # 捡起物品
     def pickup(self, player):
         if self.item:
           player.inventory.append(self.item)
           print(f"你捡起了{self.item}")
           # 清空场景
           self.item = None
         else:
           print("这里没有可以拾取的物品")