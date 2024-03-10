import pygame

from grave.scene import Scene
from grave.static_window_widget import StaticWindowWidget

from os.path import join, abspath, dirname

class MenuScene(Scene):
    def __init__(self, screen, global_things):
        super().__init__(screen, global_things, "MenuScene")

        img = pygame.image.load(join(dirname(abspath(__file__)), "rat.jpg")).convert()
        pos = ((1920 // 2) - (512 // 2), (1080 // 2) - (512 // 2))

        self.b = StaticWindowWidget(surface=screen, image=img, position=pos)

    def draw(self):
        self._screen.fill((0, 0, 0))
        self.b.draw()

    def process_event(self, event):
        super().process_event(event)

        if event.type == pygame.MOUSEBUTTONUP:
            m_x, m_y = event.pos
            self.b.position = (m_x - (512 // 2), m_y - (512 // 2))
