import pygame
import random
from vectors import Vector 

pygame.font.init()

SCREEN_HEIGHT = 800
SCREEN_WIDTH = 1200
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

BG = pygame.image.load('background/background.jpg')
BG = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))

card_back = pygame.image.load('cards/card_back.png')

WHITE = (255,255,255)

SUITS = ['S', 'H', 'C', 'D']

class Card :
    def __init__(self, pos, num, suit, img) :
        self.x = pos[0]
        self.y = pos[1]
        
        self.num = num
        self.suit = suit
        self.img = img

        if self.num == 1 :
            self.val = 14
        else :
            self.val = self.num
        
        self.w = 120
        self.h = self.w * 3 // 2
        self.cut = self.w // 20

        self.front = False

    def set_vector(self, x1, y1) :
        self.pos = Vector(self.x, self.y)
        self.vel = Vector(0, 0)
        self.acc = Vector(0, 0)
        self.target = Vector(x1, y1)

        self.max_speed = 15
        self.max_force = 8

    def update(self) :
        self.pos.add(self.vel)
        self.vel.add(self.acc)
        self.acc.mult(0)

        self.x = int(self.pos.x)
        self.y = int(self.pos.y)

    def move(self) :
         
        diff_vec = self.pos.subtract(self.target)
        if diff_vec.mag < 2 :
            return False
        
        arrive = self.arrive()
        # arrive.mult(1)
        self.applyForce(arrive)

        return True

    def arrive(self) :

        desired = self.target.subtract(self.pos)

        d = desired.mag
        #speed = self.max_speed
        #if d < 100 :
        speed = self.max_speed * d / 100

        desired.setMag(speed)

        steer = desired.subtract(self.vel)
        if steer.mag > self.max_force :
            steer.setMag(self.max_force)

        return steer

    def applyForce(self, force) :
        self.acc.add(force)

    def show(self) :

        if self.front :
            pygame.draw.rect(win, WHITE, (self.x, self.y + self.cut, self.w, self.h - 2*self.cut))
            pygame.draw.rect(win, WHITE, (self.x + self.cut, self.y, self.w - 2*self.cut, self.h))
            pygame.draw.circle(win, WHITE, (self.x + self.cut, self.y + self.cut), self.cut)
            pygame.draw.circle(win, WHITE, (self.x + self.w - self.cut, self.y + self.cut), self.cut)
            pygame.draw.circle(win, WHITE, (self.x + self.cut, self.y + self.h - self.cut), self.cut)
            pygame.draw.circle(win, WHITE, (self.x + self.w - self.cut, self.y + self.h - self.cut), self.cut)
            
            img = pygame.transform.scale(self.img, (self.w, self.h))
            win.blit(img, (self.x, self.y))

        else :
            img = pygame.transform.scale(card_back, (self.w, self.h))
            win.blit(img, (self.x, self.y))

class Chip :
    def __init__(self, pos, value, img) :
        self.x = pos[0]
        self.y = pos[1]
        
        self.value = value
        self.img = img

        self.w = 60

    def inside(self, x, y) :
        if (self.x - x) ** 2 + (self.y - y) ** 2 < self.w ** 2 :
            return True
        
        return False

    def set_vector(self, x1, y1) :
        self.pos = Vector(self.x, self.y)
        self.vel = Vector(0, 0)
        self.acc = Vector(0, 0)
        self.target = Vector(x1, y1)

        self.max_speed = 25
        self.max_force = 15

    def update(self) :
        self.pos.add(self.vel)
        self.vel.add(self.acc)
        self.acc.mult(0)

        self.x = int(self.pos.x)
        self.y = int(self.pos.y)

    def move(self) :
         
        diff_vec = self.pos.subtract(self.target)
        if diff_vec.mag < 2 :
            return False
        
        arrive = self.arrive()
        # arrive.mult(1)
        self.applyForce(arrive)

        return True

    def arrive(self) :

        desired = self.target.subtract(self.pos)

        d = desired.mag
        #speed = self.max_speed
        #if d < 100 :
        speed = self.max_speed * d / 100

        desired.setMag(speed)

        steer = desired.subtract(self.vel)
        if steer.mag > self.max_force :
            steer.setMag(self.max_force)

        return steer

    def applyForce(self, force) :
        self.acc.add(force)

    def show(self) :
        img = pygame.transform.scale(self.img, (self.w, self.w))
        win.blit(img, (self.x, self.y))

class Player :
    def __init__(self, pos = (0, 0), cards = []) :
        self.x = pos[0]
        self.y = pos[1]
        self.cards = cards

        self.score = 0

    def Sort(self) :
        for i in range(2) :
            best = i
            
            for j in range(i + 1, 3) :

                if self.cards[j].val > self.cards[best].val :
                    best = j

            self.cards[i].x, self.cards[best].x = self.cards[best].x, self.cards[i].x
            self.cards[i].y, self.cards[best].y = self.cards[best].y, self.cards[i].y
            self.cards[i], self.cards[best] = self.cards[best], self.cards[i]

    def show(self) :

        for card in self.cards :
            card.show()

    def cal_score(self) :

        score = 0
        for i in range(3) :
            score += self.cards[i].val
            score *= 100

        score *= 10e-9

        trail = True
        for i in range(3) :
            if self.cards[i].num != self.cards[0].num :
                trail = False
                break

        # Trail or set
        if trail :
            return 5 + score

        sequence = True
        for i in range(2) :
            if self.cards[i].val == self.cards[i + 1].val + 1 or (self.cards[i].num == 1 and self.cards[i + 1].num == 2) :
                continue
            else :
                sequence = False
                break

        same_suit = True 
        for i in range(2) :
            if self.cards[i].suit != self.cards[i + 1].suit :
                same_suit = False

        # Pure Sequence
        if sequence and same_suit :
            return 4 + score

        # Sequence
        if sequence :
            return 3 + score
        
        # Color
        if same_suit :
            return 2 + score

        # Pair
        for i in range(2) :
            for j in range(i + 1, 3) :
                if self.cards[i].num == self.cards[j].num :
                    return 1 + 0.01 * self.cards[i].num

        # High card
        return score

def set_deck() :
    deck = []

    for suit in SUITS :
        for num in range(1, 14) :
            img = pygame.image.load('cards/' + str(suit) + str(num) + '.png')
            c = Card(DEALER_POS, num, suit, img)
            deck.append(c)

    return deck

def set_chips() :
    values = [1, 2, 5, 10, 25, 50, 100, 250, 500, 1000, 2000, 5000]
    chips = []

    for i in range(len(values)) :
        val = values[i]
        img = pygame.image.load('chips/' + str(val) + '.png')

        if i < len(values) // 2 :
            c = Chip((SCREEN_WIDTH - 200, i * 75 + 350), val, img)
        else :
            c = Chip((SCREEN_WIDTH - 100, (i - len(values) // 2) * 75 + 350), val, img)

        chips.append(c)

    return chips

def deal(players, deck) :

    d = deck.copy()

    for i in range(NUM_PLAYERS) :
        players[i].cards = []

    for i in range(3) :
        for j in range(NUM_PLAYERS) :
            card = random.choice(d)

            if NUM_PLAYERS == 3 :
                card.set_vector(players[j].x + i * card.w * 8 // 7, players[j].y)
            else :
                card.set_vector(players[j].x + i * card.w * 13 // 12, players[j].y)

            check =  True
            while check :
                win.blit(BG, (0, 0))

                for chip in chips :
                    chip.show()

                img = pygame.transform.scale(card_back, (100, 150))
                win.blit(img, DEALER_POS)

                for k in range(len(players)) :
                    players[k].show()

                    font = pygame.font.SysFont('Consolas', 30)
                    text = font.render('Player ' + str(k + 1), True, WHITE)

                    if k == 0 :
                        win.blit(text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 40))
                    elif k == 1 :
                        win.blit(text, (300, 15))
                    else :
                        win.blit(text, (800, 15))
                
                check = card.move() 
                card.update()
                card.show()
                pygame.display.update()

            players[j].cards.append(card)

            d.remove(card)

    for i in range(NUM_PLAYERS) :
        players[i].Sort()

NUM_PLAYERS = 3
players = []

# DEALER_POS = (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 100)
DEALER_POS = (50, 350)

deck = set_deck()
chips = set_chips()

for i in range(NUM_PLAYERS) :
    if i == 0 :
        players.append(Player((SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 230)))
    else :
        if NUM_PLAYERS == 3 :
            players.append(Player((200 + (i - 1) * 500 , 50)))
        else :
            players.append(Player((40 + (i - 1) * 400, 50)))

boot_placed = False
bets_placed = False

run = True
play = False
while run :

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            run = False

    keys = pygame.key.get_pressed() 
    if keys[pygame.K_ESCAPE] :
        quit()
    elif keys[pygame.K_SPACE] :
        pygame.time.delay(100)

        if not boot_placed :
            deal(players, deck)
            boot_placed = True

    elif keys[pygame.K_b] :
        pygame.time.delay(100)

        if not bets_placed :
            bets_placed = True
            boot_placed = False

    win.blit(BG, (0, 0))

    for chip in chips :
        chip.show()

    img = pygame.transform.scale(card_back, (100, 150))
    win.blit(img, DEALER_POS)

    for i in range(len(players)) :
        players[i].show()

        font = pygame.font.SysFont('Consolas', 30)
        text = font.render('Player ' + str(i + 1), True, WHITE)

        if i == 0 :
            win.blit(text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 40))
        elif i == 1 :
            win.blit(text, (300, 15))
        else :
            win.blit(text, (800, 15))

    if boot_placed :
        if pygame.mouse.get_pressed() != (0, 0, 0) :
            mouse_x, mouse_y = pygame.mouse.get_pos()

            for chip in chips :
                if chip.inside(mouse_x, mouse_y) :
                    pygame.time.delay(50)
                    if NUM_PLAYERS == 3 :
                        new_chip = Chip((chip.x, chip.y), chip.value, chip.img)
                        chips.append(new_chip)
                        new_chip.set_vector(SCREEN_WIDTH // 2 + random.randint(0, 100) - 50, SCREEN_HEIGHT // 2 + random.randint(0, 100) - 50)

                    check =  True
                    while check :
                        win.blit(BG, (0, 0))

                        for chip in chips :
                            chip.show()

                        img = pygame.transform.scale(card_back, (100, 150))
                        win.blit(img, DEALER_POS)

                        for k in range(len(players)) :
                            players[k].show()

                            font = pygame.font.SysFont('Consolas', 30)
                            text = font.render('Player ' + str(k + 1), True, WHITE)

                            if k == 0 :
                                win.blit(text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 40))
                            elif k == 1 :
                                win.blit(text, (300, 15))
                            else :
                                win.blit(text, (800, 15))
                        
                        check = new_chip.move() 
                        new_chip.update()
                        new_chip.show()
                        pygame.display.update()

    if bets_placed :
        done = False 

        if not done :
            for i in range(NUM_PLAYERS) :
                p = players[i]
                for j in range(3) :
                    card = p.cards[j]
                    card.front = True

            all_show = True
            for i in range(NUM_PLAYERS) :
                if not players[i].cards[0].front :
                    all_show = False
                    break

            if all_show :
                max_p = 0
                for i in range(NUM_PLAYERS) :
                    players[i].score = players[i].cal_score()

                    if players[i].score > players[max_p].score :
                        max_p = i

                for i in range(len(chips) - 1, 11, -1) :
                    chip = chips[i]

                    if NUM_PLAYERS == 3 :
                        if max_p == 0 :
                            chip.set_vector(SCREEN_WIDTH // 2 + random.randint(0, 100) - 50, SCREEN_HEIGHT - 100 + random.randint(0, 100) - 50)
                        elif max_p == 1 :
                            chip.set_vector(300 + random.randint(0, 100) - 50, 100 + random.randint(0, 100) - 50)
                        else :
                            chip.set_vector(800 + random.randint(0, 100) - 50, 100 + random.randint(0, 100) - 50)

                    check =  True
                    while check :
                        win.blit(BG, (0, 0))

                        for chip in chips :
                            chip.show()

                        img = pygame.transform.scale(card_back, (100, 150))
                        win.blit(img, DEALER_POS)

                        for k in range(len(players)) :
                            players[k].show()

                            font = pygame.font.SysFont('Consolas', 30)
                            text = font.render('Player ' + str(k + 1), True, WHITE)

                            if k == 0 :
                                win.blit(text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 40))
                            elif k == 1 :
                                win.blit(text, (300, 15))
                            else :
                                win.blit(text, (800, 15))
                        
                        check = chip.move() 
                        chip.update()
                        chip.show()
                        pygame.display.update()

                    chips.pop()

            font = pygame.font.SysFont('Consolas', 50)
            text = font.render('Player ' + str(max_p + 1) + ' wins!', True, WHITE)
            win.blit(text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 20))

    pygame.display.update()

pygame.quit()