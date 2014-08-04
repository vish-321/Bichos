#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gobject
import pygame
import gtk
import random

from pygame.locals import HWSURFACE
from Cucaracha import Cucaracha
from Timer import Timer

RESOLUCION_INICIAL = (800, 600)
BASE_PATH = os.path.dirname(__file__)
BASE_PATH = os.path.dirname(BASE_PATH)

gobject.threads_init()


class CucaraSims(gobject.GObject):

    __gsignals__ = {
    "exit": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, [])}

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

        self.cucas = pygame.sprite.RenderUpdates()
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
        objeto.disconnect_by_func(self.__event_muerte)
        objeto.disconnect_by_func(self.__event_muda)
        objeto.disconnect_by_func(self.__event_repro)
        objeto.morir()

    def __connect_signals(self, objeto):
        #objeto.connect("new-edad", self.__update_edad)
        objeto.connect("muere", self.__event_muerte)
        objeto.connect("muda", self.__event_muda)
        objeto.connect("reproduce", self.__event_repro)

    def __update_time(self, widget, _dict):
        #print _dict
        pass

    def __event_muda(self, cuca):
        print "Muda"

    def __event_muerte(self, cuca, pos, escala):
        print "Muerte", pos, escala

    def __event_repro(self, cuca, pos):
        print "Reproducción", pos

    #def __update_edad(self, widget, _dict):
    #    print _dict

    def run(self):
        print "Corriendo CucaraSims . . ."
        self.estado = 1
        self.ventana.blit(self.escenario, (0, 0))
        self.ventana_real.blit(pygame.transform.scale(self.ventana,
            self.resolucionreal), (0, 0))
        pygame.display.update()
        map(self.__connect_signals, self.cucas.sprites())

        try:
            while self.estado:
                self.reloj.tick(35)
                while gtk.events_pending():
                    gtk.main_iteration()
                #if len(self.cucas.cucas()) < 5:
                #    gobject.idle_add(self.cucas.add,
                #        Bicho(RESOLUCION_INICIAL[0],
                #        RESOLUCION_INICIAL[1]))
                self.cucas.clear(self.ventana, self.escenario)
                #self.widgets.clear(self.ventana, self.escenario)
                self.cucas.update()
                #self.widgets.update()
                self.__handle_event()
                self.cucas.draw(self.ventana)
                #self.widgets.draw(self.ventana)
                self.ventana_real.blit(pygame.transform.scale(
                    self.ventana, self.resolucionreal), (0, 0))
                pygame.display.update()
                pygame.time.wait(3)
        except:
            pass


    def salir(self, widget=False):
        self.estado = 0
        self.timer.salir()
        map(self.__stop_timer, self.cucas.sprites())
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

        self.timer = Timer(1)  # 1 segundo == 1 hora
        self.timer.connect("new-time", self.__update_time)

        for x in range (2):
            cucaracha = Cucaracha("macho", RESOLUCION_INICIAL[0],
                RESOLUCION_INICIAL[1])
            random.seed()
            dias = random.randrange(181, 325, 1)
            horas = random.randrange(1, 24, 1)
            cucaracha.set_edad(dias, horas)
            self.cucas.add(cucaracha)

        for x in range (2):
            cucaracha = Cucaracha("hembra", RESOLUCION_INICIAL[0],
                RESOLUCION_INICIAL[1])
            random.seed()
            dias = random.randrange(181, 325, 1)
            horas = random.randrange(1, 24, 1)
            cucaracha.set_edad(dias, horas)
            self.cucas.add(cucaracha)
