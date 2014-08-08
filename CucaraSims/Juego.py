#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gobject
import pygame
import gtk
import random

from pygame.locals import HWSURFACE
from Cucaracha import Cucaracha
from Cucaracha import Muerta
from Huevos import Huevo
from Timer import Timer

RESOLUCION_INICIAL = (800, 600)
TIME = 1
MAX = 15
BASE_PATH = os.path.dirname(__file__)
BASE_PATH = os.path.dirname(BASE_PATH)

gobject.threads_init()


class CucaraSims(gobject.GObject):

    __gsignals__ = {
    "exit": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, []),
    "lectura": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, ))}

    def __init__(self):

        gobject.GObject.__init__(self)

        self.RESOLUCION_INICIAL = RESOLUCION_INICIAL
        self.resolucionreal = RESOLUCION_INICIAL
        self.ventana_real = False
        self.escenario = False
        self.ventana = False
        self.reloj = False
        self.estado = 0
        self.timer = False
        self.edad = {
            "Años": 0,
            "Dias": 0,
            "Horas": 0}

        self.musica = False

        self.cucas = pygame.sprite.RenderUpdates()
        self.huevos = pygame.sprite.RenderUpdates()
        self.muertas = pygame.sprite.RenderUpdates()
        #self.widgets = pygame.sprite.RenderUpdates()

    def __handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.emit("exit")
                    return
        pygame.event.clear()

    def __stop_timer(self, objeto):
        #objeto.disconnect_by_func(self.__update_edad)
        try:
            objeto.disconnect_by_func(self.__event_muerte)
        except:
            pass
        try:
            objeto.disconnect_by_func(self.__event_muda)
        except:
            pass
        try:
            objeto.disconnect_by_func(self.__event_repro)
        except:
            pass
        objeto.morir()

    def __connect_signals(self, objeto):
        #objeto.connect("new-edad", self.__update_edad)
        objeto.connect("muere", self.__event_muerte)
        objeto.connect("muda", self.__event_muda)
        objeto.connect("reproduce", self.__event_repro)

    def __update_time(self, widget, _dict):
        """
        Actualiza el Tiempo de Juego.
        """
        self.edad = dict(_dict)

    def __event_muda(self, cuca):
        """
        Una Cucaracha Muda su Exoesqueleto.
        """
        self.emit("lectura", "muda")

    def __event_muerte(self, cuca, pos, escala):
        """
        Una Cucaracha Muere.
        """
        self.muertas.add(Muerta(pos, escala, TIME))
        self.emit("lectura", "muerte")

    def __event_repro(self, cuca, pos):
        """
        Cucarachas ponen Huevos.
        """
        huevo = Huevo(pos, TIME)
        self.huevos.add(huevo)
        huevo.connect("nacer", self.__event_nacer)
        self.emit("lectura", "reproduccion")

    def __event_nacer(self, huevo, h_m, pos):
        """
        Una Ooteca eclosiona.
        """
        hembras, machos = h_m
        for h in range(hembras):
            cucaracha = Cucaracha("hembra", RESOLUCION_INICIAL[0],
                RESOLUCION_INICIAL[1], TIME)
            self.cucas.add(cucaracha)
            cucaracha.rect.centerx = pos[0]
            cucaracha.rect.centery = pos[1]
        for m in range(machos):
            cucaracha = Cucaracha("macho", RESOLUCION_INICIAL[0],
                RESOLUCION_INICIAL[1], TIME)
            self.cucas.add(cucaracha)
            cucaracha.rect.centerx = pos[0]
            cucaracha.rect.centery = pos[1]
        map(self.__connect_signals, self.cucas.sprites())
        self.emit("lectura", "ciclo-vital")

    #def __update_edad(self, widget, _dict):
    #    print _dict

    def __pausar(self, objeto):
        objeto.timer.new_handle(False)

    def __des_pausar(self, objeto):
        objeto.timer.new_handle(True)

    def pause(self):
        map(self.__pausar, self.cucas.sprites())
        map(self.__pausar, self.huevos.sprites())
        map(self.__pausar, self.muertas.sprites())
        self.timer.new_handle(False)

    def unpause(self):
        map(self.__des_pausar, self.cucas.sprites())
        map(self.__des_pausar, self.huevos.sprites())
        map(self.__des_pausar, self.muertas.sprites())
        self.timer.new_handle(True)

    def run(self):
        print "Corriendo CucaraSims . . ."
        self.estado = 1
        self.ventana.blit(self.escenario, (0, 0))
        self.ventana_real.blit(pygame.transform.scale(self.ventana,
            self.resolucionreal), (0, 0))
        pygame.display.update()

        try:
            while self.estado:
                self.reloj.tick(35)
                while gtk.events_pending():
                    gtk.main_iteration()
                #if len(self.cucas.cucas()) < 5:
                #    gobject.idle_add(self.cucas.add,
                #        Bicho(RESOLUCION_INICIAL[0],
                #        RESOLUCION_INICIAL[1]))
                self.huevos.clear(self.ventana, self.escenario)
                self.muertas.clear(self.ventana, self.escenario)
                self.cucas.clear(self.ventana, self.escenario)
                #self.widgets.clear(self.ventana, self.escenario)
                #self.huevos.update()
                #self.muertas.update()
                self.cucas.update()
                #self.widgets.update()
                self.__handle_event()
                self.huevos.draw(self.ventana)
                self.muertas.draw(self.ventana)
                self.cucas.draw(self.ventana)
                #self.widgets.draw(self.ventana)
                self.ventana_real.blit(pygame.transform.scale(
                    self.ventana, self.resolucionreal), (0, 0))
                pygame.display.update()
                if len(self.cucas.sprites()) >= 15:
                    self.emit("lectura", "plaga")
                pygame.time.wait(3)
        except:
            pass

    def salir(self, widget=False):
        self.estado = 0
        self.timer.salir()
        map(self.__stop_timer, self.cucas.sprites())
        map(self.__stop_timer, self.huevos.sprites())
        pygame.quit()

    def escalar(self, resolucion):
        self.resolucionreal = resolucion

    def config(self):
        pygame.init()
        self.reloj = pygame.time.Clock()

        from pygame.locals import MOUSEMOTION
        from pygame.locals import MOUSEBUTTONUP
        from pygame.locals import MOUSEBUTTONDOWN
        from pygame.locals import JOYAXISMOTION
        from pygame.locals import JOYBALLMOTION
        from pygame.locals import JOYHATMOTION
        from pygame.locals import JOYBUTTONUP
        from pygame.locals import JOYBUTTONDOWN
        from pygame.locals import VIDEORESIZE
        from pygame.locals import VIDEOEXPOSE
        from pygame.locals import USEREVENT
        from pygame.locals import QUIT
        from pygame.locals import ACTIVEEVENT
        from pygame.locals import KEYDOWN
        from pygame.locals import KEYUP

        pygame.event.set_blocked([
            JOYAXISMOTION, JOYBALLMOTION, JOYHATMOTION, JOYBUTTONUP,
            JOYBUTTONDOWN, ACTIVEEVENT, USEREVENT])
        pygame.event.set_allowed([QUIT, VIDEORESIZE, VIDEOEXPOSE,
            KEYDOWN, KEYUP, MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN])
        pygame.key.set_repeat(15, 15)

        pygame.display.set_mode(
            (0, 0), pygame.DOUBLEBUF | pygame.FULLSCREEN, 0)

        pygame.display.set_caption("CucaraSims")

        path = os.path.join(BASE_PATH, "CucaraSims", "Imagenes", "arena1.png")
        imagen = pygame.image.load(path)
        self.escenario = pygame.transform.scale(
            imagen, RESOLUCION_INICIAL).convert_alpha()

        self.ventana = pygame.Surface((RESOLUCION_INICIAL[0],
            RESOLUCION_INICIAL[1]), flags=HWSURFACE)
        self.ventana_real = pygame.display.get_surface()

        self.timer = Timer(TIME)  # 1 segundo == 1 hora
        self.timer.connect("new-time", self.__update_time)

        for x in range (2):
            cucaracha = Cucaracha("macho", RESOLUCION_INICIAL[0],
                RESOLUCION_INICIAL[1], TIME)
            random.seed()
            dias = random.randrange(181, 325, 1)
            horas = random.randrange(1, 24, 1)
            cucaracha.set_edad(dias, horas)
            self.cucas.add(cucaracha)

        for x in range (2):
            cucaracha = Cucaracha("hembra", RESOLUCION_INICIAL[0],
                RESOLUCION_INICIAL[1], TIME)
            random.seed()
            dias = 189#random.randrange(181, 325, 1)
            horas = random.randrange(1, 24, 1)
            cucaracha.set_edad(dias, horas)
            self.cucas.add(cucaracha)

        map(self.__connect_signals, self.cucas.sprites())

        #path = os.path.join(BASE_PATH, "CucaraSims", "Sonidos", "musica.ogg")
        #pygame.mixer.music.load(path)
        #pygame.mixer.music.play(-1, 0.0)
