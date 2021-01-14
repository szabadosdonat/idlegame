import pygame

# global variables
button_pressed = False
screen_width = 360
screen_heigth = 640


# ToDo: inherit Button and Text from Thing/Object class
class Text:
    def __init__(self, value, size, x=None, y=None, bold=False):
        # x == None --> centered vertically
        # y == None --> centered horizontally
        self.value = value
        self.x = x
        self.y = y
        self.size = size
        self.bold = bold

    def draw_text(self):
        # note: bold switch does seemingly nothing
        if self.bold:
            font = pygame.font.Font('freesansbold.ttf', self.size)
        else:
            font = pygame.font.SysFont('calibrilight.ttf', self.size)
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
        self.active = False     # True if button is on screen, needed for overlapping frames with buttons

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
        screen.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + (self.heigth/3)))
        return action


class Frame:
    def __init__(self, name, *things, background_color=(255, 255, 255)):
        self.name = name
        self.color = background_color
        self.things = things

    def draw_frame(self):
        screen.fill(self.color)
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


if __name__ == '__main__':

    pygame.init()

    screen = pygame.display.set_mode((screen_width, screen_heigth))
    pygame.display.set_caption("Donát féle Idle Game")

    # buttons
    # ToDo: make button coordinates relative to screen dimensions
    b11 = Button('Játék', x=80, y=250)
    b12 = Button('Beállítások', x=80, y=360)
    b13 = Button('Kilépés', x=80, y=470)
    b21 = Button('Fejlesztések', x=20, y=20, width=100, heigth=40, text_size=15)
    b22 = Button('Főmenü', x=240, y=20, width=100, heigth=40, text_size=15)
    b31 = Button('Vissza', x=240, y=20, width=100, heigth=40, text_size=15)
    b41 = Button('Vissza', x=240, y=20, width=100, heigth=40, text_size=15)

    # text objects
    t11 = Text('Idle Játék', 60, x=None, y=50, bold=True)
    t12 = Text('készítette: Szabados Donát', 25, x=None, y=150)

    # frames
    f1 = Frame('Main Menu', b11, b12, b13, t11, t12)
    f2 = Frame('Home Screen', b21, b22)
    f3 = Frame('Upgrades', b31)
    f4 = Frame('Beállítások', b41)

    current_frame = f1

    # game loop
    running = True
    clock = pygame.time.Clock()

    while running:

        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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

        current_frame.draw_frame()

        pygame.display.update()
