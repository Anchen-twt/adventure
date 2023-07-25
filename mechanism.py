class Mechanism:
  def __init__(self, name, desc, required_items):
      self.name = name
      self.desc = desc
      self.required_items = required_items
     
  def can_pass(self, player):
      # 检查玩家是否有开启机关需要的道具
      for item in self.required_items:
          if item not in player.inventory:
            return False
      return True
     
  def pass_mechanism(self, player):
      # 玩家通过机关的逻辑
      print(f"你使用{self.required_items}打开了{self.name}")
      
key_door = Mechanism('钥匙之门', '一扇上锁的铁门', ['钥匙'])