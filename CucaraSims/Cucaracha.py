#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Cucaracha.py por:
#   Flavio Danesse <fdanesse@gmail.com>

import os
import pygame
from pygame.sprite import Sprite
import random
from math import sin
from math import cos
from math import radians

from Timer import Timer

BASE_PATH = os.path.dirname(__file__)

INDICE_ROTACION = 5


class Cucaracha(Sprite):

    def __init__(self, sexo, ancho, alto):

        Sprite.__init__(self)

        self.sexo = sexo

        random.seed()
        path = ""
        if self.sexo == "macho":
            self.imagen = random.choice(["cucaracha1.png", "cucaracha2.png"])
            path = os.path.join(BASE_PATH, "Imagenes", self.imagen)
            self.imagen = pygame.image.load(path)
        elif self.sexo == "hembra":
            self.imagen = random.choice(["cucaracha3.png", "cucaracha4.png"])
            path = os.path.join(BASE_PATH, "Imagenes", self.imagen)
            self.imagen = pygame.image.load(path)

        imagen_escalada = pygame.transform.scale(self.imagen, (60, 50))
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

        random.seed()
        self.muerte = random.randrange(340, 365, 1)  # morirá este dia
        self.mudas = {
            9: (73, 60),
            21: (83, 70),
            32: (93, 80),
            43: (103, 90)}
        #self.repro = [51, 62, 73]

        self.timer = Timer(1)
        self.edad = {
            "Años": 0,
            "Dias": 0,
            "Horas": 0}
        self.timer.connect("new-time", self.__update_time)

    def __update_time(self, widget, _dict):
        self.edad = dict(_dict)
        print self.edad["Dias"], self.edad["Horas"]
        if self.edad["Dias"] in self.mudas.keys() and self.edad["Horas"] == 0:
            self.__set_muda(escala=self.mudas[self.edad["Dias"]])

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

    def __set_muda(self, escala=(63, 50)):
        print "muda", escala
        self.imagen_original = pygame.transform.scale(self.imagen, escala)
        self.image = pygame.transform.rotate(
            self.imagen_original, -self.angulo)
        x = self.rect.centerx
        y = self.rect.centery
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        #self.emit("muda", (x, y), escala)

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

    def set_edad(self, dias, horas):
        self.timer.dias = dias
        self.timer.horas = horas
        mudas = self.mudas.keys()
        escala = (60, 50)
        if self.timer.dias in range(0, mudas[0]):
            escala = (60, 50)
        elif self.timer.dias in range(mudas[0], mudas[1] + 1):
            escala = self.mudas[mudas[0]]
        elif self.timer.dias in range(mudas[1], mudas[2] + 1):
            escala = self.mudas[mudas[1]]
        elif self.timer.dias in range(mudas[2], mudas[3] + 1):
            escala = self.mudas[mudas[2]]
        else:
            escala = self.mudas[mudas[3]]
        self.__set_muda(escala=escala)

    def morir(self):
        self.timer.salir()
        self.kill()
