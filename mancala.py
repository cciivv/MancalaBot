class MancalaBoard(object):
    """
        Board layout is as such...
        [stash, pit * 6, stash, pit * 6]
        so stash for player one is at index 0, and stash for player two is at len(board)/2
    """
    def __init__(self, lane_length = 6, players = 2):
        self.lane_length = lane_length
        self.max_players = players
        print "=============================================================="
        self.board = [4 for x in range(players * (lane_length + 1))]

        for x in range(players):
            self.board[x * len(self.board)/players] = 0

    def grab_pit(self, loc):
        """ Assumes loc has been verified for the calling player"""
        if loc > len(self.board):
            return 0
        temp = self.board[loc]
        self.board[loc] = 0
        return temp
    
    def put(self, loc, num):
        """ Assumes valid move """
        if loc > len(self.board):
            return 0
        self.board[loc] += 1
        return self.board[loc]
    
    def get_move_options(self, p_num):
        b_len = len(self.board)
        shift = (p_num * b_len/2)
        look = range(shift + 1, shift + (b_len/2))
        out = look [:]
        for x in look:
            if self.board[x] == 0:
                out.remove(x)
        return out

    def get_stash_loc(self, player):
        return player * len(self.board) / self.max_players
    
    def get_stash_values(self):
        return [self.board[self.get_stash_loc(x)] for x in range(self.max_players)]

    def prev_loop(self, num, max_num):
        if (num - 1 < 0):
            next = max_num - 1
        else:
            next = (num - 1)
        return next

    def next_pit(self, player, loc):
        b_len = len(self.board)
        
        next = self.prev_loop(loc, b_len)

        p_test = self.prev_loop(player, self.max_players)
        if next == (p_test * b_len / 2):
            next = self.prev_loop(loc, b_len)

        return next
    
    def get_opposite(self, loc):
        b_len = len(self.board)/2
        if loc % b_len == 0:
            return -1
        diff = loc - b_len
        return b_len - diff 

    def is_game_over(self):
        game_over = False
        for p_num in range(self.max_players):
            if self.get_move_options(p_num) == []:
                game_over = True
        return game_over
    
    def print_board(self, player):
        print self.board
        return "You are blind, you cannot see the board. Choose one of these numbers " + str(self.get_move_options(player))

class MancalaGame(object):
    def __init__(self, *args):
        self.mat = MancalaBoard()
        self.turn = 0
        self.players = []
        for player in args:
            self.players.append(player)
            print player.name, "is player number", len(self.players)
            if len(self.players) >= self.mat.max_players:
                break
    
    def move_pieces(self, move, player):
        """ Assumes move is valid """
        beans = self.mat.grab_pit(move)
        loc = move
        last = -1
        while True:
            loc = self.mat.next_pit(player, loc)
            last = self.mat.put(loc, 1)
            beans -= 1
            if beans <= 0:
                break
        if last == 1 and loc in self.mat.get_move_options(player):
            opp = self.mat.get_opposite(loc)
            if self.mat.board[opp] != 0:
                jackpot = self.mat.grab_pit(opp) + self.mat.grab_pit(loc)
                print "Super Grab! %s gets %d points!" % (self.players[player], jackpot)
                self.mat.put(self.mat.get_stash_loc(player),jackpot)
        if loc == self.mat.get_stash_loc(player):
            return 1
        else:
            return 0      
        
    def play(self):
        while not (self.mat.is_game_over()):
            pid = self.turn % self.mat.max_players
            while True:
                print "====== %s'S TURN ======" % (self.players[0].name.upper())
                move = self.players[pid].make_move(self.mat, pid)
                if move in self.mat.get_move_options(pid):
                    extra = self.move_pieces(move, pid)
                    if  extra <= 0 or len(self.mat.get_move_options(pid)) == 0:
                        break
                    else:
                        print "%s gets to go again!" % self.players[pid]
                else:
                    print "Invalid Move"
            self.turn += 1
        print "============="
        print "  GAME OVER  "
        print "============="
        
        scores = self.mat.get_stash_values()

        winner = scores.index(max(scores))

        print "%s wins!" % (self.players[winner])

class Player(object):
    def __init__(self, name):
        self.name = name
    
    def make_move(self, board, num):
        pass
        
class HumanPlayer(Player):
    def __init__(self):
        player = raw_input("What is your name?")
        super(HumanPlayer, self).__init__(player)
        
    def make_move(self, board, num):
        print "This is the board", board.print_board(num)
        while True:
            try:
                move = int(raw_input("Make your move:"))
                break
            except ValueError:
                print "that isn't a number... try again dumbass."
        
        return move
        
    def __str__(self):
        return "A puny human named " + self.name

p1 = HumanPlayer()
p2 = HumanPlayer()
game = MancalaGame(p1, p2)
game.play()
