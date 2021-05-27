#############################################################################
# Client - that connect to the multi-threading server
############################################################################
import socket
import threading
import tkinter as tk
import random
import time


class Client(object):
    def __init__(self, ip, port, color, name, password):
        self.ip = ip
        self.port = port
        self.money = 250
        self.color = color
        self.password = password
        self.name = name
        self.place = 0
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.player_assets = []
        self.root = tk.Tk()
        self.players = []
        self.question_count = 0
        self.board = (
            "start ----->", "TLV", "question", "Azrieli Towers", "income taxes", "Port of Haifa", "Hamelichim city",
            "surprise", "SuperLand",
            "The Biblical Zoo", "Eletrical company", "The Bima", "jail", "Haifa", "Eilat", "surprise", "Ramat Gan",
            "Petah Tiqwa", "Tveria", "Jerusalem", "question", "Bethlehem")
        self.assets = {"TLV": 250, "Azrieli Towers": 300, "income taxes": 300,
                       "Port of Haifa": 150, "Hamelichim city": 200, "SuperLand": 250, "The Biblical Zoo": 200,
                       "Eletrical company": 400, "The Bima": 250, "Haifa": 200, "Eilat": 150, "Ramat Gan": 300,
                       "Petah Tiqwa": 100, "Tveria": 150, "Jerusalem": 300, "Bethlehem": 230}

    def start(self):
        try:
            print('connecting to ip %s port %s' % (ip, port))
            # Create a TCP/IP socket
            self.sock.connect((ip, port))
            print('connected to server')
            # send receive example
            self.sock.sendall('Hello this is client 1, send me a job'.encode())
            # implement here your main logic
            self.handleServer()
            self.opening_screen()
        except socket.error as e:
            print(e)

    def handleServer(self):
        client_handler = threading.Thread(target=self.handle_client, args=())
        # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
        client_handler.start()

    def handle_client(self):
        while True:
            msg = self.sock.recv(1024).decode()
            print(msg)
            if 'player count' in msg:
                if '1' in msg:
                    screen_width = int(self.root.winfo_screenwidth())
                    screen_height = int(self.root.winfo_screenheight())
                    wait = tk.Label(self.root, text='Waiting for more players to join....', bg='white')
                    wait.place(x=int(screen_width/2-100), y=screen_height-350)
                if '2' in msg:
                    register = "playerInfo: " + str(self.name) + " color: " + str(self.color) + " place: 0 "
                    self.sock.send(str(register).encode())
                    screen_width = int(self.root.winfo_screenwidth())
                    screen_height = int(self.root.winfo_screenheight())
                    #self.root.withdraw()
                    delete = tk.Label(self.root, bg='white', width=screen_width, height=screen_height)
                    delete.place(x=0, y=0)
            if "playerInfo" in msg or "updated_info" in msg:
                self.enter_players(msg)
                if len(self.players) > 1:
                    self.draw_board()

    def quitwindow(self, event):
        self.sock.send("im leaving".encode())

    def opening_screen(self):
        open = self.root
        screen_width = int(open.winfo_screenwidth())
        screen_height = int(open.winfo_screenheight())
        size = str(screen_width) + 'x' + str(screen_height)
        open.geometry(size)
        open["background"] = "white"
        open.iconbitmap('monopolylogo.ico')
        open.title("Monopoly Cyber- Opening Screen")
        fn = tk.Label(open, text="First Name:", bg='white')
        fn.place(x=int(screen_width/4), y=screen_height-400)
        ps = tk.Label(open, text="Password:", bg='white')
        ps.place(x=int(screen_width/4+350), y=screen_height-400)
        e1 = tk.Entry(open)
        e2 = tk.Entry(open)
        e1.place(x=int(screen_width/4)+80, y=screen_height-400)
        e2.place(x=int(screen_width/4+430), y=screen_height-400)
        submit = tk.Button(open, text='Submit', command=lambda: self.get_info(open, e1.get(), e2.get()))
        submit.place(x=int(screen_width/2-80), y=screen_height-350)
        instructions = tk.Label(open, bg= 'white', text='instructions:\n In this game at least 2 player has to play, else the game wont start or be over.\n'
                                           'Every player in its turn will get to rotate the cube once and decide if they want to buy the land they stand on or not.\n '
                                           'If the land has been purchased by another player they will have to pay them a certain amount.\n'
                                           'If the player got to a surprise square, their amount of money will increase by 50 to a 1000.\n'
                                           'The game will last 30 minutes, the player with the most assets will win!')
        instructions.place(x=int(screen_width/4), y=screen_height/4+50)
        self.image(open, screen_width/4+100, 0)
        self.root.mainloop()

    def get_info(self, open, name, password):
        screen_width = int(open.winfo_screenwidth())
        screen_height = int(open.winfo_screenheight())
        self.name = name
        self.password = password
        colors = ["red4", "tomato", "coral", "orange", "gold", "lawn green", "cyan", "RoyalBlue1", "magenta3", "purple", "MediumPurple4"]
        msg = "name&password " + str(name) + " " + str(password)
        x = int(screen_width / 4+50)
        if self.name != '' and self.password != '':
            self.sock.send(str(msg).encode())
            lbl = tk.Label(open, text="Choose a color:")
            lbl.place(x=int(screen_width / 4), y=screen_height - 300)
            for color in colors:
                cb = tk.Button(open, bg=color, width=3, height=2, command=lambda: self.change_color(color, open))
                cb.place(x=x, y=screen_height - 270)
                x += 50
        else:
            temptk = tk.Tk()
            temptk.iconbitmap('monopolylogo.ico')
            temptk.title("Error")
            tk.Label(temptk, text='Submit your name and password before you continue').grid(row=0, column=0)

    def change_color(self, color, open):
        self.color = color
        screen_width = int(open.winfo_screenwidth())
        screen_height = int(open.winfo_screenheight())
        start = tk.Button(open, bg='yellow2', text="Click Here To Start", width=20, height=5, command=lambda: self.starting_screen(open))
        start.place(x=int(screen_width/2-100), y=int(screen_height-200))

    def starting_screen(self, open):
        screen_width = int(open.winfo_screenwidth())
        screen_height = int(open.winfo_screenheight())
        hide = tk.Label(open, width=90, height=13, bg="white")
        hide.place(x=int(screen_width/4), y=screen_height/2-30)
        self.sock.send("start".encode())
        #self.handleServer()

    def enter_players(self, info):
        sp = info.split()
        c = info.count("playerInfo") + 1
        player = sp[0]
        x = 1
        num = 1
        while c != num:
            if sp[x] != "playerInfo":
                player = player + str(sp[x]) + " "
                x += 1
            else:
                num += 1
                self.players.append(player)


    def decode_server_msg(self, info):
        sp = info.split()
        turn = False
        name = sp[1]
        color = sp[3]
        psum = sp[5]
        if len(sp) > 5 and [6] == 'TURN':
            turn = True
        self.handleServer()
        #print("name: " + name + " psum: " + str(psum) + " color: " + color)
        return name, color, psum, turn

    def draw_board(self):
        self.draw_board_squares(self.root)
        self.update_and_show_money(self.root)
        self.draw_players(self.root)
        #self.image(self.root, 500, 200)
        #self.root.mainloop()

    def image(self, window, x, y):
        img = tk.PhotoImage(file='monopolygif.gif')
        lbl = tk.Label(window, image=img, bg='white')
        lbl.place(x=int(x), y=int(y))
        window.mainloop()

    def finding_player_place(self, sum):
        sum = int(sum)
        bp = self.board[sum]
        boardplace = [0, 10, 20, 30, 40, 50, 60, 70, 80, 81, 82, 83, 73, 63, 53, 43, 33, 23, 13, 12, 11]
        # finiding x and y
        playerp = boardplace[sum]
        x = (playerp / 10) * 146
        y = (playerp % 10) * 156
        return x, y, bp

    def rand_number(self, window):
        rand = random.randrange(1, 7)
        cub = tk.Label(window, bg='black', text=rand, fg='white', width=2, height=2)
        cub.place(x=1030, y=375)
        self.place += rand
        if self.place >= 21:
            self.place = self.place % 10
        # sending the player's updated info
        players_info = "updated_info: " + self.name + " color: " + self.color + " place: " + str(self.place)
        self.sock.send(str(players_info).encode())

    def questions(self, window):
        question_list = ("What is the difference between list and tuples in Python?",
                         "What type of language is python? Programming or scripting?",
                         "What is namespace in Python?", "What are local variables and global variables in Python?")
        right_answers = ("Tuples are immutable", "Tuples are slower than list", )
        false_answers = ("Tuples made with []", )
        newWindow = tk.Toplevel(window)
        newWindow["background"] = "white"
        newWindow.iconbitmap('monopolylogo.ico')
        newWindow.title("Monopoly Cyber")
        newWindow.geometry("600x400")
        rand = random.randrange(2)
        x = 1
        tk.Label(newWindow, text=question_list[self.question_count]).grid(row=0, column=0)

        tk.Button(newWindow, text=right_answers[0], command=lambda: self.answers(newWindow, True)).grid(row=1, column=rand)
        if rand == x:
            x = 0
        tk.Button(newWindow, text=false_answers[0], command=lambda: self.answers(newWindow, False)).grid(row=1, column=x)
        newWindow.mainloop()

    def answers(self, window, right):
        window.destroy()
        w = tk.Tk()
        w.iconbitmap('monopolylogo.ico')
        w.title("Monopoly Cyber")
        if right:
            #self.gift_cards(window)
            answer = tk.Label(w, text="congrats! you are right!")
            answer.grid(row=0, column=0)
        if not right:
            answer = tk.Label(w, text="you are wrong, try next time")
            answer.grid(row=0, column=0)
        w.after(5000, w.destroy)

    def gift_cards(self, window):
        gift_lst = (500, 100, 50, 50, 100, 1000, 50, 1)
        ran = random.choice(gift_lst)
        self.money += int(ran)
        self.update_and_show_money(window)

    def update_and_show_money(self, window):
        msg = tk.Label(window, text="your current money value:", fg="black")
        msg.place(x=30, y=650)
        mny = tk.Label(window, text=self.money, fg="black")
        mny.place(x=180, y=650)

    def cube(self, window):
        cube = tk.Button(window, bg='black', width=10, height=5, command=lambda: self.rand_number(window))
        cube.place(x=1000, y=350)

    def draw_players(self, game_screen):
        #The next player on the array is the updated version of the first player.
        #In this if the player delets itself and then drawing again in the "for".
        for player in self.players:
            if len(self.players) > 2:
                self.delete_player(game_screen, self.players[0])
            name, color, psum, turn = self.decode_server_msg(player)
            x, y, bp = self.finding_player_place(psum)
            if turn and self.name == name:
                self.cube(game_screen)
            if not turn:
                x = x + 20
            draw_player = tk.Label(game_screen, text=str(name), bg=color, fg='white')
            draw_player.place(x=int(x), y=int(y))
            if 'start' not in bp and "question" not in bp and 'jail' not in bp and 'surprise' not in bp:
                self.asset_purchase_button(game_screen, player)
            if bp == "surprise":
                self.gift_cards(game_screen)
            if bp == "question":
                self.questions(game_screen)

    def delete_player(self, game_screen, player):
        name, color, psum, turn = self.decode_server_msg(player)
        x, y, bp = self.finding_player_place(psum)
        color = self.find_color(bp)
        player = tk.Label(game_screen, bg="black", text=str(name), fg="black")
        player.place(x=int(x), y=int(y))
        self.players.remove(self.players[0])
        print((self.players))

    def asset_purchase_button(self, window, player):
        name, color, psum, turn = self.decode_server_msg(player)
        x, y, bp = self.finding_player_place(psum)
        color = self.find_color(bp)
        price = self.assets[str(bp)]
        purchase = tk.Button(window, text='purchase: ' + str(price), bg=color, fg="black", command= lambda: self.buy(window, player))
        purchase.place(x=0, y=y + 100)

    def find_color(self, bp):
        colors = ['red', 'blue', 'yellow', 'orange', 'green']
        counter = 0
        for place in self.board:
            if place != bp:
                counter += 1
            else:
                if counter > len(colors):
                    x = int(counter / len(colors))
                else:
                    return colors[counter]
                return colors[int(x)]

    def buy(self, window, buyer_player):
        for player in self.players:
            if buyer_player == player:
                name, color, psum, turn = self.decode_server_msg(player)
                x, y, bp = self.finding_player_place(psum)
                price = self.assets[str(bp)]
                if self.money > price:
                    self.player_assets.append(bp)
                    self.money -= price
                    self.update_and_show_money(window)
                    purchase = tk.Label(window, text=name + "s'  property    ", bg='gray')
                    purchase.place(x=0, y=y + 100)
                else:
                    screen_width = int(window.winfo_screenwidth()/2)
                    screen_height = int(window.winfo_screenheight()/2)
                    msg_window = tk.Toplevel(window)
                    size = str(screen_width) + 'x' + str(screen_height)
                    msg_window.geometry(size)
                    cant = tk.Label(msg_window, text="You don't have enough money to buy this asset", bg='white')
                    cant.place(x=0, y=0)
                    msg_window.mainloop()

    def countdown(self, t):
        while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(timer, end="\r")
            time.sleep(1)
            t -= 1
        return 'done'

    def draw_board_squares(self, window):
        boardlen = len(self.board)
        third = int(boardlen / 3) + 2
        colors = ['red', 'blue', 'yellow', 'orange', 'green']
        pname = 0
        x, y, count = 0, 0, 0
        for path in range(third):
            if count > 4:
                count = 0
            asset = self.board[pname]
            square = tk.Label(window, width=20, height=10, bg=colors[count])
            square.place(x=x, y=y)
            name = tk.Label(window, text=asset, bg=colors[count])
            name.place(x=x + 40, y=y + 60)
            if 'start' not in self.board[pname] and "question" not in self.board[pname] and 'jail' not in self.board[
                pname] and 'surprise' not in self.board[pname]:
                price = self.assets[str(asset)]
                purchase = tk.Label(window, text='purchase: ' + str(price), bg=colors[count], fg="black")
                purchase.place(x=x, y=y + 100)
            x += 146
            pname += 1
            count += 1

        x = 146
        y = 156
        for path in range(int(boardlen / 7)):
            if count > 4:
                count = 0
            square = tk.Label(window, width=20, height=10, bg=colors[count])
            square.place(x=x, y=y)
            name = tk.Label(window, text=self.board[pname], bg=colors[count])
            name.place(x=x + 40, y=y + 60)
            if 'start' not in self.board[pname] and "question" not in self.board[pname] and 'jail' not in self.board[
                pname] and 'surprise' not in self.board[pname]:
                asset = self.board[pname]
                price = self.assets[str(asset)]
                purchase = tk.Label(window, text='purchase: ' + str(price), bg=colors[count], fg="black")
                purchase.place(x=x, y=y + 100)
            count += 1
            y += 156
            pname += 1

        y = y - 156
        x = 146
        for path in range(third - 2):
            if count > 4:
                count = 0
            square = tk.Label(window, width=20, height=10, bg=colors[count])
            square.place(x=x, y=y)
            name = tk.Label(window, text=self.board[pname], bg=colors[count])
            name.place(x=x + 40, y=y + 60)
            if 'start' not in self.board[pname] and "question" not in self.board[pname] and 'jail' not in self.board[
                pname] and 'surprise' not in self.board[pname]:
                asset = self.board[pname]
                price = self.assets[str(asset)]
                purchase = tk.Label(window, text='purchase: ' + str(price), bg=colors[count], fg="black")
                purchase.place(x=x, y=y + 100)
            x += 146
            count += 1
            pname += 1

        for path in range(int(boardlen / 7)):
            if count > 4:
                count = 0
            square = tk.Label(window, width=20, height=10, bg=colors[count])
            square.place(x=x, y=y)
            name = tk.Label(window, text=self.board[pname], bg=colors[count])
            name.place(x=x + 40, y=y + 60)
            if 'start' not in self.board[pname] and "question" not in self.board[pname] and 'jail' not in self.board[
                pname] and 'surprise' not in self.board[pname]:
                asset = self.board[pname]
                price = self.assets[str(asset)]
                purchase = tk.Label(window, text='purchase: ' + str(price), bg=colors[count], fg="black")
                purchase.place(x=x, y=y + 100)
            count += 1
            y -= 156
            pname += 1
        exitb = tk.Button(window, text='Exit', command=exit)
        exitb.place(x=0, y=300)
        # self.picture(window)


if __name__ == '__main__':
    ip = '127.0.0.2'
    port = 1730
    color = "black"
    name = "-"
    password = "-"
    c = Client(ip, port, color, name, password)
    c.start()
