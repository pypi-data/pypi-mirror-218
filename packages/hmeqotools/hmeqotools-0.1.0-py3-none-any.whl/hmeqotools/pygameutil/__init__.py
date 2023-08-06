import typing as t

import pygame


class Entity:

    def __init__(self, surface: pygame.surface.Surface, rect: pygame.rect.Rect):
        self.surface = surface
        self.rect = rect

    def blit_to(self, target: pygame.surface.Surface):
        target.blit(self.surface, self.rect)

    def contain(self, pos: tuple[int, int]):
        return (
            self.rect.x <= pos[0] < self.rect.right
            and self.rect.y <= pos[1] < self.rect.bottom
        )


class Scene:

    def __init__(self):
        self.enable = True
        self.entities: list[Entity] = []

    def blit_to(self, target: pygame.surface.Surface):
        for entity in self.entities:
            entity.blit_to(target)

    def on_mouse_button_down(self, event: pygame.event.Event):
        pass


class SceneManager:

    class Event:

        prevented = False

    def __init__(self, scenes: t.Tuple[Scene, ...]):
        self.scenes = scenes

    def set(self, scene: t.Union[int, Scene]):
        if isinstance(scene, int):
            scene = self.scenes[scene]
        for i in self.scenes:
            i.enable = i is scene

    def emit(self, method: t.Callable, *args, **kwds):
        self.Event.prevented = False
        for scense in self.scenes:
            if self.Event.prevented:
                break
            if not scense.enable:
                continue
            getattr(scense, method.__name__)(*args, **kwds)

    def prevent(self):
        self.Event.prevented = True
