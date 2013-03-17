class Player(object):
    def __init__(self, name):
        self.name = name
        
class HumanPlayer(Player):
    def __init__(self):
        player = raw_input("What is your name?")
        print player
        super(HumanPlayer, self).__init__(player)

p1 = HumanPlayer()
