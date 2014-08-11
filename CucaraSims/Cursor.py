#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Cursor.py por:
#   Flavio Danesse <fdanesse@gmail.com>

import os
import pygame
from pygame.sprite import Sprite

BASE_PATH = os.path.dirname(__file__)


class Cursor(Sprite):

    def __init__(self, tipo):

        Sprite.__init__(self)

        self.tipo = tipo

        path = ""
        if self.tipo == "agua":
            path = os.path.join(BASE_PATH, "Imagenes", "jarra.png")
        elif self.tipo == "alimento":
            path = os.path.join(BASE_PATH, "Imagenes", "pan.png")

        self.image = pygame.image.load(path)
        # pygame.transform.scale(pygame.image.load(path), (24, 48))
        self.rect = self.image.get_rect()

    def pos(self, pos):
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
