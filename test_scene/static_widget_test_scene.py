import pygame

from grave.scene import Scene
from grave.static_window_widget import StaticWindowWidget
from grave.abstract_button_widget import AbstractButtonWidget
from grave.signal import Signal

from os.path import join, abspath, dirname

class StaticWidgetTestScene(Scene):
    def __init__(self, screen, global_things):
        super().__init__(screen, global_things, "MenuScene")

        _this_dir_ = dirname(abspath(__file__))

        img = pygame.image.load(join(_this_dir_, "window.png")).convert_alpha()
        img_2 = pygame.image.load(join(_this_dir_, "ship.png")).convert_alpha()
        img_button = pygame.image.load(join(_this_dir_, "button.png")).convert_alpha()
        pos = ((1920 // 2) - (512 // 2), (1080 // 2) - (512 // 2))

        button_pos = (img.get_width() // 2 - img_button.get_width() // 2, img.get_height() // 2 - img_button.get_height() // 2)

        self.mask = pygame.mask.from_surface(img)
        self.mask_2 = pygame.mask.from_surface(img_2)

        self._show_masks = False
        self._overlap_mask = None

        self.b = StaticWindowWidget(surface=screen, image=img_2)
        self.a = StaticWindowWidget(surface=screen, image=img, position=pos)
        self.button = AbstractButtonWidget(surface=screen, image=img_button, position=button_pos)

        Signal.connect(self.button.on_hover, lambda : print("Hovering entered"))
        Signal.connect(self.button.on_hover_exit, lambda : print("Hovering exited"))
        Signal.connect(self.button.on_clicked, lambda : print("Clicked"))
        Signal.connect(self.button.on_pressed, lambda : print("Pressed"))
        Signal.connect(self.button.on_released, lambda : print("Released"))

        self.a.add_widget(self.b)
        self.a.add_widget(self.button)

    def draw(self):
        self._screen.fill((255, 0, 0))
        if not self._show_masks:
            self.a.draw()
        else:
            self._screen.blit(self.mask.to_surface(), self.a.position)
            self._screen.blit(self.mask_2.to_surface(), self.b.position)
            if self._overlap_mask is not None:
                self._screen.blit(self._overlap_mask.to_surface(unsetcolor=(0,0,0,0), setcolor=(0,0,255,255)), self.b.position)

    def update_scene(self):
        m_x, m_y = pygame.mouse.get_pos()
        self.b.position = (m_x - (256 // 2), m_y - (256 // 2))

        o_x = self.a.x - self.b.x
        o_y = self.a.y - self.b.y
        self._overlap_mask = self.mask_2.overlap_mask(self.mask, (o_x, o_y))

        self.a.update()

    def process_event(self, event):
        super().process_event(event)

        self.button.process_events(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            self._show_masks = not self._show_masks

        if event.type == pygame.MOUSEBUTTONUP:
            m_x, m_y = event.pos
            self.a.position = (m_x - (512 // 2), m_y - (512 // 2))
            for widget in self.a._widgets:
                x, y = self.a.position
                widget.position = (x + (self.a._image.get_width() // 2) - (widget._image.get_width() // 2), y + (self.a._image.get_width() // 2) - (widget._image.get_height() // 2))
