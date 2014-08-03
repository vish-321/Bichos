#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Cucaracha.py por:
#   Flavio Danesse <fdanesse@gmail.com>

import os
import pygame
from pygame.sprite import Sprite
import random
from math import sin, cos, radians

BASE_PATH = os.path.dirname(__file__)
#BASE_PATH = os.path.dirname(BASE_PATH)

INDICE_ROTACION = 5


class Cucaracha(Sprite):

    def __init__(self, sexo, ancho, alto):

        Sprite.__init__(self)

        self.sexo = sexo

        random.seed()
        path = ""
        if self.sexo == "macho":
            imagen = random.choice(["cucaracha1.png", "cucaracha2.png"])
            path = os.path.join(BASE_PATH, "Imagenes", imagen)
            imagen = pygame.image.load(path)
        elif self.sexo == "hembra":
            imagen = random.choice(["cucaracha3.png", "cucaracha4.png"])
            path = os.path.join(BASE_PATH, "Imagenes", imagen)
            imagen = pygame.image.load(path)

        imagen_escalada = pygame.transform.scale(imagen, (60, 50))
        self.imagen_original = imagen_escalada.convert_alpha()

        self.dx = 0
        self.dy = 0
        self.angulo = 0
        self.velocidad = 8
        self.escena = pygame.Rect(35, 35, ancho - 70, alto - 70)

        self.image = self.imagen_original.copy()
        self.rect = self.image.get_rect()

        self.rect.centerx = self.escena.w / 2
        self.rect.centery = self.escena.h / 2

    def __actualizar_posicion(self):
        x = self.rect.centerx + self.dx
        y = self.rect.centery + self.dy
        if self.escena.collidepoint(x, y):
            self.image = pygame.transform.rotate(
                self.imagen_original, -self.angulo)
            self.rect.centerx = x
            self.rect.centery = y
        else:
            self.angulo = self.angulo * 1.25
            self.image = pygame.transform.rotate(
                self.imagen_original, -self.angulo)
            self.dx = 0
            self.dx = 0

    def __get_vector(self, angulo):
        radianes = radians(angulo)
        x = int(cos(radianes) * self.velocidad)
        y = int(sin(radianes) * self.velocidad)
        return x, y

    def update(self):
        acciones = ["camina", "gira", "quieto"]
        random.seed()
        accion = random.choice(acciones)
        if accion == "gira":
            sent = random.randrange(1, 3, 1)
            if sent == 1:
                self.angulo -= int(0.7 * INDICE_ROTACION)
                if self.angulo < -360:
                    self.angulo += 360
            elif sent == 2:
                self.angulo += int(0.7 * INDICE_ROTACION)
                if self.angulo > 360:
                    self.angulo -= 360
            self.dx, self.dy = self.__get_vector(self.angulo)
            self.__actualizar_posicion()
