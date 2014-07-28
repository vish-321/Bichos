#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gobject
import pygame
import gtk

from Bicho import Bicho

RESOLUCION_INICIAL = (800, 600)
BASE_PATH = os.path.dirname(__file__)

gobject.threads_init()


class Intro(gobject.GObject):

    def __init__(self):

        gobject.GObject.__init__(self)

        self.resolucionreal = RESOLUCION_INICIAL
        self.escenario = False
        self.ventana = False
        self.reloj = False
        self.estado = 0

        self.sprites = pygame.sprite.RenderUpdates()

    def run(self):
        print "Corriendo Intro . . ."
        self.estado = 1
        self.ventana.blit(self.escenario, (0, 0))
        pygame.display.update()

        try:
            while self.estado:
                self.reloj.tick(35)
                while gtk.events_pending():
                    gtk.main_iteration()
                while len(self.sprites.sprites()) < 10:
                    self.sprites.add(Bicho(RESOLUCION_INICIAL[0],
                        RESOLUCION_INICIAL[1]))
                self.sprites.clear(self.ventana, self.escenario)
                self.sprites.update()
                pygame.event.pump()
                pygame.event.clear()
                self.sprites.draw(self.ventana)
                self.ventana_real.blit(pygame.transform.scale(self.ventana,
                    self.resolucionreal), (0, 0))
                pygame.display.update()
        except pygame.error, message:
            print pygame.error, message
            pygame.quit()

    def salir(self):
        self.estado = 0
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

        pygame.event.set_blocked([MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN,
            JOYAXISMOTION, JOYBALLMOTION, JOYHATMOTION, JOYBUTTONUP,
            JOYBUTTONDOWN, ACTIVEEVENT, USEREVENT, KEYDOWN, KEYUP])
        pygame.event.set_allowed([QUIT, VIDEORESIZE, VIDEOEXPOSE])

        pygame.display.set_mode(
            (0, 0), pygame.DOUBLEBUF | pygame.FULLSCREEN, 0)

        pygame.display.set_caption("Bichos")

        path = os.path.join(BASE_PATH, "Fondos", "arena1.png")
        imagen = pygame.image.load(path)
        self.escenario = pygame.transform.scale(
            imagen, RESOLUCION_INICIAL).convert_alpha()

        self.ventana = pygame.Surface((RESOLUCION_INICIAL[0],
            RESOLUCION_INICIAL[1]))
        self.ventana_real = pygame.display.get_surface()
