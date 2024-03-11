import pygame

from grave.scene import Scene
from grave.static_window_widget import StaticWindowWidget

from os.path import join, abspath, dirname

class StaticWidgetTestScene(Scene):
    def __init__(self, screen, global_things):
        super().__init__(screen, global_things, "MenuScene")

        _this_dir_ = dirname(abspath(__file__))

        img = pygame.image.load(join(_this_dir_, "window.png")).convert_alpha()
        img_2 = pygame.image.load(join(_this_dir_, "ship.png")).convert_alpha()
        pos = ((1920 // 2) - (512 // 2), (1080 // 2) - (512 // 2))

        self.mask = pygame.mask.from_surface(img)
        self.mask_2 = pygame.mask.from_surface(img_2)
        self._overlap_mask = None

        self._show_masks = False

        self.a = StaticWindowWidget(surface=screen, image=img_2)
        self.b = StaticWindowWidget(surface=screen, image=img, position=pos)

    def draw(self):
        self._screen.fill((255, 0, 0))
        if not self._show_masks:
            self.b.draw()
            self.a.draw()
        else:
            self._screen.blit(self.mask.to_surface(), self.b.position)
            self._screen.blit(self.mask_2.to_surface(), self.a.position)
            if self._overlap_mask is not None:
                self._screen.blit(self._overlap_mask.to_surface(unsetcolor=(0,0,0,0), setcolor=(0,0,255,255)), self.a.position)

    def update_scene(self):
        m_x, m_y = pygame.mouse.get_pos()
        self.a.position = (m_x - (256 // 2), m_y - (256 // 2))

        o_x = self.b.x - self.a.x
        o_y = self.b.y - self.a.y
        self._overlap_mask = self.mask_2.overlap_mask(self.mask, (o_x, o_y))

        self.a.set_overlap_mask(self._overlap_mask)

    def process_event(self, event):
        super().process_event(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            self._show_masks = not self._show_masks

        if event.type == pygame.MOUSEBUTTONUP:
            m_x, m_y = event.pos
            self.b.position = (m_x - (512 // 2), m_y - (512 // 2))
