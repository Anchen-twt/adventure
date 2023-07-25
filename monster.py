class Monster:
  def __init__(self, name, hp, atk, drops=[]):
    self.name = name
    self.hp = hp
    self.atk = atk
    self.drops = drops
    
  # 进行一次攻击
  def attack(self, player):
    player.hp -= self.atk
    print(f'{self.name}攻击了你！造成了{self.atk}点伤害')