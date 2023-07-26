class Player:
    def __init__(self, hp, atk, inventory):
        self.hp = hp
        self.atk = atk 
        self.inventory = inventory
        self.loc = 'start'
    
    # 在场景间移动
    def move(self, scenes, exit_name):
        self.loc = scenes[self.loc].exits[exit_name]
    
    # 进行一次攻击
    def attack(self, monster):
      monster.hp -= self.atk
      print(f' 你攻击了{monster.name}！造成了{self.atk}点伤害')    