class Monster:
  def __init__(self, hp, atk):
    self.hp = hp
    self.atk = atk
    
  # 进行一次攻击
  def attack(self, player):
    player.hp -= self.atk
    print(f'怪物攻击了你！造成了{self.atk}点伤害')