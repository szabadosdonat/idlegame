import pygame

"""
update 0.3
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
infobox = False          # on/off switch for infoboxes

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
    def __init__(self, text, x, y, width=200, heigth=75, text_size=30):
        self.x = x
        self.y = y
        self.text = text
        self.width = width
        self.heigth = heigth
        self.text_size = text_size
        self.active = False  # True if button is on screen, needed for overlapping frames with buttons

    @property
    def get_width(self):
        return self.width

    @property
    def get_heigth(self):
        return self.heigth

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def cursor_collide(self):
        button_rect = pygame.Rect(self.x, self.y, self.width, self.heigth)
        return button_rect.collidepoint(pygame.mouse.get_pos()) and self.active

    def draw_button(self):
        global button_pressed
        action = False
        cursor_position = pygame.mouse.get_pos()
        button_rect = pygame.Rect(self.x, self.y, self.width, self.heigth)
        colors = ((180, 77, 77), (146, 60, 60), (100, 60, 60), (255, 255, 255))

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

        # button text
        font = pygame.font.Font('freesansbold.ttf', self.text_size)
        text_img = font.render(self.text, True, colors[3])
        text_len = text_img.get_width()
        screen.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + (self.heigth / 3)))
        return action


class Frame:
    def __init__(self, name, *things, background_color=(255, 255, 255)):
        self.name = name
        self.color = background_color
        self.things = things

    def draw_frame(self):
        screen.fill(self.color)
        if self.name == 'Home Screen':
            screen.blit(boxes[level - 1], (screen_width // 2 - 64, 330))
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


# ToDo: finish Upgrade class
class Upgrade:
    def __init__(self, name, pricing, upgrade):
        self.name = name
        self.pricing = pricing
        self.upgrade = upgrade
        self.level = 0

    def deploy(self):
        global money
        if self.level < len(self.pricing):
            money -= self.pricing[self.level]
            self.level += 1
        self.upgrade()


if __name__ == '__main__':

    pygame.init()

    screen = pygame.display.set_mode((screen_width, screen_heigth))
    pygame.display.set_caption("Donát féle Idle Game")

    # buttons
    # ToDo: make button coordinates relative to screen dimensions
    # ToDo: name things properly
    b11 = Button('Játék', x=80, y=250)
    b12 = Button('Beállítások', x=80, y=360)
    b13 = Button('Kilépés', x=80, y=470)
    b21 = Button('Fejlesztések', x=20, y=20, width=100, heigth=40, text_size=15)
    b22 = Button('Főmenü', x=240, y=20, width=100, heigth=40, text_size=15)
    b23 = Button('Kézi gyártás', x=55, y=485, width=250, heigth=100, text_size=35)
    b31 = Button('Vissza', x=240, y=20, width=100, heigth=40, text_size=15)
    b32 = Button('gyár építése', x=20, y=120, width=150, heigth=75, text_size=15)
    b33 = Button('termék fejlesztése', x=20, y=215, width=150, heigth=75, text_size=15)
    b34 = Button('béremelés', x=20, y=310, width=150, heigth=75, text_size=15)
    b35 = Button('Upgrade 4', x=20, y=405, width=150, heigth=75, text_size=15)
    b36 = Button('Upgrade 5', x=20, y=500, width=150, heigth=75, text_size=15)
    b37 = Button('Upgrade 6', x=190, y=120, width=150, heigth=75, text_size=15)
    b38 = Button('Upgrade 7', x=190, y=215, width=150, heigth=75, text_size=15)
    b39 = Button('Upgrade 8', x=190, y=310, width=150, heigth=75, text_size=15)
    b310 = Button('Upgrade 9', x=190, y=405, width=150, heigth=75, text_size=15)
    b311 = Button('szintlépés', x=190, y=500, width=150, heigth=75, text_size=15)
    b312 = Button('i', x=25, y=25, width=30, heigth=30, text_size=15)
    b41 = Button('Vissza', x=240, y=20, width=100, heigth=40, text_size=15)
    b42 = Button('option 1', x=80, y=140)
    b43 = Button('option 2', x=80, y=250)
    b44 = Button('option 3', x=80, y=360)
    b45 = Button('option 4', x=80, y=470)

    # text objects
    t11 = Text('Idle Játék', 60, x=None, y=50)
    t12 = Text('készítette: Szabados Donát', 20, x=None, y=150)
    t21 = Text(f'${money}', 80, x=None, y=90)
    t22 = Text(f'level {level}', 25, x=None, y=30)
    t23 = Text(f'termék értéke: {product_value}', 25, x=None, y=200)
    t24 = Text(f'gyárak száma: {factories}', 25, x=None, y=240)
    t25 = Text(f'eladott termékek: {sold_products}', 25, x=None, y=280)
    t31 = Text(f'${money}', 35, x=None, y=25)

    # frames
    f1 = Frame('Main Menu', b11, b12, b13, t11, t12)
    f2 = Frame('Home Screen', b21, b22, b23, t21, t22, t23, t24, t25)
    f3 = Frame('Upgrades', b31, b32, b33, b34, b35, b36, b37, b38, b39, b310, b311, b312, t31)
    f4 = Frame('Beállítások', b41, b42, b43, b44, b45)

    # the frame set here shows up on game start, for now it's the main menu
    current_frame = f1

    # event for factory money generating
    EVENT_FACTORY = pygame.USEREVENT + 1

    # game loop
    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(60)

        def make_money(value):
            global money
            money += value * level**3
            refresh_numbers()

        def refresh_numbers():
            t22.set_value(f'level {level}')
            t23.set_value(f'gyárak száma: {factories}')
            t24.set_value(f'termék értéke: {product_value}')
            t25.set_value(f'eladott termékek: {sold_products}')
            t21.set_value(f'${money}')
            t31.set_value(f'${money}')

        def show_upgrade_details():
            x = 15
            y = pygame.mouse.get_pos()[1] + 60 if pygame.mouse.get_pos()[1] < 400 else pygame.mouse.get_pos()[1] - 240
            pygame.draw.rect(screen, (230, 230, 230), pygame.Rect(x, y, 330, 200))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == EVENT_FACTORY:
                sold_products += 1
                make_money(product_value)
                refresh_numbers()

        # navigation buttons
        # ToDo: organize these somehow
        if b11.draw_button():
            current_frame.hide_frame()
            current_frame = f2

        if b12.draw_button():
            current_frame.hide_frame()
            current_frame = f4

        if b13.draw_button():
            running = False

        if b21.draw_button():
            current_frame.hide_frame()
            current_frame = f3

        if b22.draw_button():
            current_frame.hide_frame()
            current_frame = f1

        if b31.draw_button():
            current_frame.hide_frame()
            current_frame = f2

        if b41.draw_button():
            current_frame.hide_frame()
            current_frame = f1

        # kézi gyártás gomb
        if b23.draw_button():
            sold_products += 1
            make_money(product_value)
            refresh_numbers()

        # upgrade buttons (b32-b311)
        if b32.draw_button():   # gyár építése
            factories += 1
            pygame.time.set_timer(EVENT_FACTORY, productivity // factories)
            refresh_numbers()

        if b33.draw_button():   # termék fejlesztése
            product_value += 1
            refresh_numbers()
            if factories > 0:
                pygame.time.set_timer(EVENT_FACTORY, productivity // factories)

        if b34.draw_button():   # béremelés
            productivity -= 50
            if factories > 0:
                pygame.time.set_timer(EVENT_FACTORY, productivity // factories)

        if b311.draw_button():
            if level < 6:
                print(level)
                level += 1
                money = 0
                factories = 0
                product_value = 1
                sold_products = 0
                productivity = 1000
                pygame.time.set_timer(EVENT_FACTORY, 0)
                current_frame.hide_frame()
                current_frame = f2
                refresh_numbers()

        if b312.draw_button():
            infobox = not infobox

        current_frame.draw_frame()

        if infobox:
            for button in (b32, b33, b34, b35, b36, b37, b38, b39, b310, b311):
                if button.cursor_collide():
                    show_upgrade_details()

        pygame.display.update()
