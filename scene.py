class Scene:
     def __init__(self, name, desc, exits, monster = None):
         self.name = name
         self.base_desc = desc
         self.exits = exits
         self.monster = monster
     
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