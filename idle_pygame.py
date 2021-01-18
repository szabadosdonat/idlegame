import pygame
import random

"""
update 0.4
"""

# global variables
button_pressed = False
screen_width = 360
screen_heigth = 640
money = 0               # starting money
level = 1               # starting level
factories = 0           # factories auto-generate money
product_value = 1       # value of one product
sold_products = 0       # number of sold products
productivity = 1000     # rate of production (denominator)
infobox = False         # on/off switch for infoboxes
isr = 0                 # investment succes rate

boxes = (
    pygame.image.load("box_images\\box1.png"),
    pygame.image.load("box_images\\box2.png"),
    pygame.image.load("box_images\\box3.png"),
    pygame.image.load("box_images\\box4.png"),
    pygame.image.load("box_images\\box5.png"),
    pygame.image.load("box_images\\box6.png")
)


# ToDo: inherit Button and Text from Thing/Object class
class Text:
    def __init__(self, value, size, x=None, y=None):
        # x == None --> centered vertically
        # y == None --> centered horizontally
        self.value = value
        self.x = x
        self.y = y
        self.size = size

    def set_value(self, value):
        self.value = value
        self.x = (screen_width / 2) - (pygame.font.Font('freesansbold.ttf', self.size).render(self.value, True, (0, 0, 0)).get_width() / 2)

    def draw_text(self):
        font = pygame.font.Font('freesansbold.ttf', self.size)
        rendered = font.render(self.value, True, (0, 0, 0))
        if self.x is None:
            self.x = (screen_width / 2) - (rendered.get_width() / 2)
        if self.y is None:
            self.y = (screen_heigth / 2) - (rendered.get_height() / 2)
        screen.blit(rendered, (self.x, self.y))


class Button:
    def __init__(self, text, x, y, width=200, heigth=75, text_size=30, associated_upgrade=None):
        self.x = x
        self.y = y
        self.text = text
        self.width = width
        self.heigth = heigth
        self.text_size = text_size
        self.active = False     # True if button is on screen, needed for overlapping frames with buttons
        self.associated_upgrade = associated_upgrade  # if it's an upgrade button, that upgrade is associated with the button object through this variable

    @property
    def get_width(self):
        return self.width

    @property
    def get_heigth(self):
        return self.heigth

    @property
    def get_upgrade(self):
        return self.associated_upgrade

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def cursor_collide(self):
        button_rect = pygame.Rect(self.x, self.y, self.width, self.heigth)
        return button_rect.collidepoint(pygame.mouse.get_pos()) and self.active

    def render_text(self, price=None):  # if it's an upgrade button, "price" sets a price to be displayed
        font = pygame.font.Font('freesansbold.ttf', self.text_size)
        text_img = font.render(self.text, True, (255, 255, 255))
        text_len = text_img.get_width()
        if price is not None:
            price_text_img = pygame.font.Font('freesansbold.ttf', self.text_size+5).render(price, True, (255, 255, 255))
            price_text_len = price_text_img.get_width()
            screen.blit(price_text_img, (self.x + int(self.width / 2) - int(price_text_len / 2), self.y + (3*self.heigth/5-5)))
        screen.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + (self.heigth / (3 if price is None else 5))))

    def draw_button(self):
        global button_pressed
        action = False
        cursor_position = pygame.mouse.get_pos()
        button_rect = pygame.Rect(self.x, self.y, self.width, self.heigth)
        colors = ((180, 77, 77), (146, 60, 60), (100, 60, 60))

        # cursor detection
        if button_rect.collidepoint(cursor_position) and self.active:
            if pygame.mouse.get_pressed(3)[0]:
                button_pressed = True
                pygame.draw.rect(screen, colors[2], button_rect)
            elif not pygame.mouse.get_pressed(3)[0] and button_pressed:
                button_pressed = False
                action = True
            else:
                pygame.draw.rect(screen, colors[1], button_rect)
        else:
            pygame.draw.rect(screen, colors[0], button_rect)

        return action


class Frame:
    def __init__(self, name, *things, background_color=(255, 255, 255)):
        self.name = name
        self.color = background_color
        self.things = things

    def draw_frame(self):
        screen.fill(self.color)
        if self.name == 'Home Screen':
            screen.blit(boxes[level - 1], (screen_width // 2 - 64, 325))
        for thing in self.things:
            if isinstance(thing, Button):
                thing.activate()
                thing.draw_button()
            elif isinstance(thing, Text):
                thing.draw_text()

    def hide_frame(self):
        for thing in self.things:
            if isinstance(thing, Button):
                thing.deactivate()


# just to organise the upgrade prices, levels etc.
class Upgrade:
    def __init__(self, name, prices):
        self.name = name
        self.prices = prices
        self.level = 1

    @property
    def get_name(self):
        return self.name

    @property
    def get_prices(self):
        return self.prices

    @property
    def get_level(self):
        return self.level

    def current_price(self):
        if self.level <= len(self.prices):
            return f'${self.prices[self.level - 1]}'
        else:
            return '(max level)'

    def current_price_numeric(self):
        if self.level <= len(self.prices):
            return self.prices[self.level - 1]


if __name__ == '__main__':

    pygame.init()

    screen = pygame.display.set_mode((screen_width, screen_heigth))
    pygame.display.set_caption("Idle Game")

    # text objects
    t11 = Text('Idle Játék', 60, x=None, y=50)
    t12 = Text('készítette: Szabados Donát', 20, x=None, y=150)
    t21 = Text(f'${money}', 80, x=None, y=80)
    t22 = Text(f'level {level}', 25, x=None, y=30)
    t23 = Text(f'termék értéke: {product_value}', 25, x=None, y=185)
    t24 = Text(f'gyárak száma: {factories}', 25, x=None, y=225)
    t25 = Text(f'eladott termékek: {sold_products}', 25, x=None, y=265)
    t31 = Text(f'${money}', 35, x=None, y=25)

    # upgrades
    u1 = Upgrade('gyár építése', (50, 500, 5000, 50000, 500000, 5000000))
    u2 = Upgrade('termék fejlesztése', (10, 20, 30))
    u3 = Upgrade('béremelés', (10000, 100000, 1000000))
    u4 = Upgrade('befektetésérzék', (500, 2500, 10000, 30000, 70000, 150000, 250000, 500000, 800000, 1000000))
    u5 = Upgrade('upgrade 5', tuple())
    u6 = Upgrade('upgrade 6', tuple())
    u7 = Upgrade('upgrade 7', tuple())
    u8 = Upgrade('upgrade 8', tuple())
    u9 = Upgrade('upgrade 9', tuple())
    u10 = Upgrade('szintlépés', (1000, 30000, 140000, 600000, 1500000))

    # buttons
    b11 = Button('Játék', x=80, y=250)
    b12 = Button('Beállítások', x=80, y=360)
    b13 = Button('Kilépés', x=80, y=470)
    b21 = Button('Fejlesztések', x=20, y=20, width=100, heigth=40, text_size=15)
    b22 = Button('Főmenü', x=240, y=20, width=100, heigth=40, text_size=15)
    b23 = Button('Kézi gyártás', x=55, y=485, width=250, heigth=100, text_size=35)
    b31 = Button('Vissza', x=240, y=20, width=100, heigth=40, text_size=15)
    b32 = Button('gyár építése', x=20, y=120, width=150, heigth=75, text_size=15, associated_upgrade=u1)
    b33 = Button('termék fejlesztése', x=20, y=215, width=150, heigth=75, text_size=15, associated_upgrade=u2)
    b34 = Button('béremelés', x=20, y=310, width=150, heigth=75, text_size=15, associated_upgrade=u3)
    b35 = Button('befektetésérzék', x=20, y=405, width=150, heigth=75, text_size=15, associated_upgrade=u4)
    b36 = Button('Upgrade 5', x=20, y=500, width=150, heigth=75, text_size=15)
    b37 = Button('Upgrade 6', x=190, y=120, width=150, heigth=75, text_size=15)
    b38 = Button('Upgrade 7', x=190, y=215, width=150, heigth=75, text_size=15)
    b39 = Button('Upgrade 8', x=190, y=310, width=150, heigth=75, text_size=15)
    b310 = Button('Upgrade 9', x=190, y=405, width=150, heigth=75, text_size=15)
    b311 = Button('szintlépés', x=190, y=500, width=150, heigth=75, text_size=15, associated_upgrade=u10)
    b312 = Button('i', x=25, y=25, width=30, heigth=30, text_size=15)
    b41 = Button('Vissza', x=240, y=20, width=100, heigth=40, text_size=15)
    b42 = Button('option 1', x=80, y=140)
    b43 = Button('option 2', x=80, y=250)
    b44 = Button('option 3', x=80, y=360)
    b45 = Button('option 4', x=80, y=470)

    # frames
    f1 = Frame('Main Menu', b11, b12, b13, t11, t12)
    f2 = Frame('Home Screen', b21, b22, b23, t21, t22, t23, t24, t25)
    f3 = Frame('Upgrades', b31, b32, b33, b34, b35, b36, b37, b38, b39, b310, b311, b312, t31)
    f4 = Frame('Beállítások', b41, b42, b43, b44, b45)

    # lists of things
    button_list = [b11, b12, b13, b21, b22, b23, b31, b32, b33, b34, b35, b36, b37, b38, b39, b310, b311, b312, b41, b42, b43, b44, b45]
    texts = [t11, t12, t21, t22, t23, t24, t25, t31]

    # the frame set here shows up on game start, for now it's the main menu
    current_frame = f1

    # events
    EVENT_FACTORY = pygame.USEREVENT + 1

    # game loop
    running = True
    clock = pygame.time.Clock()

    # limiting game to 60fps
    while running:
        clock.tick(60)

        # refreshes display of all statistics and money
        def refresh_numbers():
            t22.set_value(f'level {level}')
            t23.set_value(f'gyárak száma: {factories}')
            t24.set_value(f'termék értéke: {product_value}')
            t25.set_value(f'eladott termékek: {sold_products}')
            t21.set_value(f'${money}')
            t31.set_value(f'${money}')

        # adds an amount to the global "money" variable
        def make_money(amount):
            global money
            money += amount * level ** 3
            refresh_numbers()

        # shows an infobox when hovering over upgrade buttons (a gray rectangle for now)
        def show_infobox():
            x = 15
            y = 420 if pygame.mouse.get_pos()[1] < 400 else 110
            pygame.draw.rect(screen, (230, 230, 230), pygame.Rect(x, y, 330, 200))

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == EVENT_FACTORY:
                sold_products += 1
                make_money(product_value)
                refresh_numbers()

        # navigation buttons
        if b11.draw_button():
            current_frame.hide_frame()
            current_frame = f2
        elif b12.draw_button():
            current_frame.hide_frame()
            current_frame = f4
        elif b13.draw_button():
            running = False
        elif b21.draw_button():
            current_frame.hide_frame()
            current_frame = f3
        elif b22.draw_button():
            current_frame.hide_frame()
            current_frame = f1
        elif b31.draw_button():
            current_frame.hide_frame()
            current_frame = f2
        elif b41.draw_button():
            current_frame.hide_frame()
            current_frame = f1

        # hand-manufacturing button
        if b23.draw_button():
            sold_products += 1
            # investment upgrade
            if isr > 0 and random.randint(isr, 25) == 25:
                make_money(level+4 ** 3)
            make_money(product_value)
            refresh_numbers()

        # price and level handling for upgrade buttons
        def upgrade(u, fun):
            global factories, money
            if u.level <= len(u.prices):
                if u.current_price_numeric() <= money:
                    money -= u.current_price_numeric()
                    u.level += 1
                    fun()
                else:
                    print(f'Not enough money for "{u.name}" upgrade\nprice: {u.current_price()}')
            else:
                print(f'Max level for "{u.name}" upgrade reached')

        # upgrade functions (what the upgrades actually do)
        def ufun1():    # gyár építése
            global factories
            factories += 1
            pygame.time.set_timer(EVENT_FACTORY, productivity // factories)
            refresh_numbers()

        def ufun2():    # termék fejlesztése
            global product_value
            product_value += 1
            if factories > 0:
                pygame.time.set_timer(EVENT_FACTORY, productivity // factories)
            refresh_numbers()

        def ufun3():    # béremelés
            global productivity
            productivity -= 50
            if factories > 0:
                pygame.time.set_timer(EVENT_FACTORY, productivity // factories)

        def ufun4():    # befektetésérzék
            global isr
            if isr <= 25:
                isr += 1

        def ufun5():
            pass

        def ufun6():
            pass

        def ufun7():
            pass

        def ufun8():
            pass

        def ufun9():
            pass

        def ufun10():    # levelup/prestige
            global level, current_frame, money, factories, productivity, product_value, sold_products, isr
            if level < 6:
                level += 1
                money = 0
                factories = 0
                product_value = 1
                sold_products = 0
                productivity = 1000
                isr = 0
                for u in (u1, u2, u3, u4):
                    u.level = 1
                pygame.time.set_timer(EVENT_FACTORY, 0)
                current_frame.hide_frame()
                current_frame = f2
                refresh_numbers()

        # upgrade buttons
        button_list = [b32, b33, b34, b35, b36, b37, b38, b39, b310, b311]
        upgrade_list = [u1, u2, u3, u4, u5, u6, u7, u8, u9, u10]
        ufun_list = [ufun1, ufun2, ufun3, ufun4, ufun5, ufun6, ufun7, ufun8, ufun9, ufun10]
        for i in range(len(button_list)):
            if button_list[i].draw_button():
                upgrade(upgrade_list[i], ufun_list[i])

        # infoboxes on/off switch
        if b312.draw_button():
            infobox = not infobox

        # show the current frame
        current_frame.draw_frame()

        # render text on buttons
        for button in [b11, b12, b13, b21, b22, b23, b31, b32, b33, b34, b35, b36, b37, b38, b39, b310, b311, b312, b41, b42, b43, b44, b45]:
            if button.active:
                if button.associated_upgrade is not None:
                    button.render_text(button.associated_upgrade.current_price())
                else:
                    button.render_text()

        # show infoboxes about upgrades
        if infobox:
            for button in (b32, b33, b34, b35, b36, b37, b38, b39, b310, b311):
                if button.cursor_collide():
                    show_infobox()

        # refresh screen
        pygame.display.update()
