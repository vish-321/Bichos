#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Cucaracha.py por:
#   Flavio Danesse <fdanesse@gmail.com>

import os
import gobject
import pygame
from pygame.sprite import Sprite
import random
from math import sin
from math import cos
from math import radians

from Timer import Timer

BASE_PATH = os.path.dirname(__file__)

INDICE_ROTACION = 5


class Cucaracha(Sprite, gobject.GObject):

    __gsignals__ = {
    #"new-edad": (gobject.SIGNAL_RUN_LAST,
    #    gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, )),
    "muere": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,
        gobject.TYPE_PYOBJECT)),
    "muda": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, []),
    "reproduce": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, ))}

    def __init__(self, sexo, ancho, alto, TIME):

        Sprite.__init__(self)
        gobject.GObject.__init__(self)

        self.sexo = sexo
        self.hambre = 0
        self.sed = 0

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

        self.escala = (53, 40)
        imagen_escalada = pygame.transform.scale(self.imagen, self.escala)
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
            10: (53, 40),
            30: (63, 50),
            50: (73, 60),
            90: (83, 70),
            130: (93, 80),
            180: (103, 90)}
        self.repro = range(190, 330, 30)

        self.timer = Timer(TIME)
        self.edad = {
            "Años": 0,
            "Dias": 0,
            "Horas": 0}
        self.timer.connect("new-time", self.__update_time)

    def __update_time(self, widget, _dict):
        self.edad = dict(_dict)
        #self.emit("new-edad", self.edad)
        if self.edad["Dias"] in self.mudas.keys() and self.edad["Horas"] == 0:
            self.__set_muda(escala=self.mudas[self.edad["Dias"]])
            self.emit("muda")
        elif self.edad["Dias"] in self.repro and self.edad["Horas"] == 0:
            self.emit("reproduce", (self.angulo,
                self.rect.centerx, self.rect.centery))
            #Fixme: Si es hembra y hay machos en el escenario
        elif self.edad["Dias"] >= self.muerte:
            self.emit("muere", (self.angulo,
                self.rect.centerx, self.rect.centery), self.escala)
            self.morir()

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
        """
        Muda de exoesqueleto, cambia de tamaño.
        """
        self.escala = escala
        self.imagen_original = pygame.transform.scale(self.imagen, self.escala)
        self.image = pygame.transform.rotate(
            self.imagen_original, -self.angulo)
        x = self.rect.centerx
        y = self.rect.centery
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

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
        """
        Para Forzar edad.
        """
        self.timer.dias = dias
        self.timer.horas = horas
        m = self.mudas.keys()
        mudas = []
        for x in m:
            mudas.append(int(x))
        mudas.sort()
        if self.timer.dias in range(0, mudas[0]):
            self.escala = (60, 50)
        elif self.timer.dias in range(mudas[0], mudas[1] + 1):
            self.escala = self.mudas[mudas[0]]
        elif self.timer.dias in range(mudas[1], mudas[2] + 1):
            self.escala = self.mudas[mudas[1]]
        elif self.timer.dias in range(mudas[2], mudas[3] + 1):
            self.escala = self.mudas[mudas[2]]
        elif self.timer.dias in range(mudas[3], mudas[4] + 1):
            self.escala = self.mudas[mudas[3]]
        elif self.timer.dias in range(mudas[4], mudas[5] + 1):
            self.escala = self.mudas[mudas[4]]
        else:
            self.escala = self.mudas[mudas[5]]
        self.__set_muda(escala=self.escala)

    def morir(self):
        self.timer.salir()
        self.emit("muere", (self.rect.centerx, self.rect.centery), self.escala)
        self.kill()


class Muerta(Sprite):

    def __init__(self, pos, escala, TIME):

        Sprite.__init__(self)

        path = os.path.join(BASE_PATH, "Imagenes", "muerta.png")
        imagen = pygame.image.load(path)
        imagen_escalada = pygame.transform.scale(imagen, escala)
        self.image = imagen_escalada.convert_alpha()
        self.rect = self.image.get_rect()

        self.image = pygame.transform.rotate(self.image, -pos[0])
        self.rect.centerx = pos[1]
        self.rect.centery = pos[2]

        self.timer = Timer(TIME)
        self.edad = {
            "Años": 0,
            "Dias": 0,
            "Horas": 0}
        self.timer.connect("new-time", self.__update_time)

    def __update_time(self, widget, _dict):
        self.edad = dict(_dict)
        if self.edad["Dias"] >= 3:
            self.morir()

    def morir(self):
        self.timer.salir()
        self.kill()
