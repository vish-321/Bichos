#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gobject
import pygame
import gtk

#from CeibalJAM_Lib.JAMElipseButton import JAMElipseButton

from Bicho import Bicho

RESOLUCION_INICIAL = (800, 600)
BASE_PATH = os.path.dirname(__file__)
BASE_PATH = os.path.dirname(BASE_PATH)

gobject.threads_init()


class Intro(gobject.GObject):

    __gsignals__ = {
    "exit": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, [])}

    def __init__(self):

        gobject.GObject.__init__(self)

        self.resolucionreal = RESOLUCION_INICIAL
        self.ventana_real = False
        self.escenario = False
        self.ventana = False
        self.reloj = False
        self.estado = 0

        self.sprites = pygame.sprite.RenderUpdates()
        self.widgets = pygame.sprite.RenderUpdates()

    def __handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.emit("exit")
                    return
            #else:
            #    print event
        pygame.event.clear()

    def run(self):
        print "Corriendo Intro . . ."
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
                while len(self.sprites.sprites()) < 5:
                    self.sprites.add(Bicho(RESOLUCION_INICIAL[0],
                        RESOLUCION_INICIAL[1]))
                self.sprites.clear(self.ventana, self.escenario)
                self.widgets.clear(self.ventana, self.escenario)
                self.sprites.update()
                self.widgets.update()
                self.__handle_event()
                self.sprites.draw(self.ventana)
                self.widgets.draw(self.ventana)
                self.ventana_real.blit(pygame.transform.scale(self.ventana,
                    self.resolucionreal), (0, 0))
                pygame.display.update()
        except:
            print "ERROR"
            #pygame.quit()

    def salir(self):
        self.estado = 0
        pygame.quit()

    def escalar(self, resolucion):
        self.resolucionreal = resolucion

    def config(self):
        pygame.init()
        self.reloj = pygame.time.Clock()

        #from pygame.locals import MOUSEMOTION
        #from pygame.locals import MOUSEBUTTONUP
        #from pygame.locals import MOUSEBUTTONDOWN
        #from pygame.locals import JOYAXISMOTION
        #from pygame.locals import JOYBALLMOTION
        #from pygame.locals import JOYHATMOTION
        #from pygame.locals import JOYBUTTONUP
        #from pygame.locals import JOYBUTTONDOWN
        #from pygame.locals import VIDEORESIZE
        #from pygame.locals import VIDEOEXPOSE
        #from pygame.locals import USEREVENT
        #from pygame.locals import QUIT
        #from pygame.locals import ACTIVEEVENT
        #from pygame.locals import KEYDOWN
        #from pygame.locals import KEYUP

        #pygame.event.set_blocked([MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN,
        #    JOYAXISMOTION, JOYBALLMOTION, JOYHATMOTION, JOYBUTTONUP,
        #    JOYBUTTONDOWN, ACTIVEEVENT, USEREVENT, KEYDOWN, KEYUP])
        #pygame.event.set_allowed([QUIT, VIDEORESIZE, VIDEOEXPOSE])
        pygame.key.set_repeat(15, 15)

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
        '''
        path = os.path.join(BASE_PATH, "Iconos", "creditos.png")
        boton = JAMElipseButton(texto="", tamanio_panel=(200, 130),
            imagen=path, tamanio_imagen=(127,77))
		#boton.connect(callback=self.get_creditos,
		#   sonido_select=self.sonido_select)
        x = (RESOLUCION_INICIAL[0] / 9) * 4
        y = (RESOLUCION_INICIAL[1] / 9) * 3
        boton.set_posicion(punto=(x,y))
        self.widgets.add(boton)

        path = os.path.join(BASE_PATH, "Iconos", "cucarasims.png")
        boton = JAMElipseButton(imagen=path, tamanio_imagen=(190,97),
            texto="", tamanio_panel=(250, 180))
        #boton.connect(callback=self.get_cucarasims,
        #   sonido_select=self.sonido_select)
        x = (RESOLUCION_INICIAL[0] / 9) * 6
        y = (RESOLUCION_INICIAL[1] / 9) * 1
        boton.set_posicion(punto=(x,y))
        self.widgets.add(boton)
        '''
        '''
		boton = JAMElipseButton(imagen=bichos_cantores_logo, tamanio_imagen=(128,77), texto="", tamanio_panel=(250, 180))
		boton.connect(callback=self.get_bichos_cantores, sonido_select=self.sonido_select)
		x = w*7
		y = h*3
		boton.set_posicion(punto=(x,y))
		self.widgets.add(boton)

		# Boton Salir
		boton = JAMElipseButton(texto="Salir", tamanio_panel=(200, 130), tamanio_de_letra=50)
		boton.connect(callback=self.selecciona_mensaje_cerrar, sonido_select=self.sonido_select)
		x = w*6
		y = h*5
		boton.set_posicion(punto=(x,y))
		self.widgets.add(boton)

		# Boton Ojos Compuestos
		boton = JAMElipseButton(texto="", tamanio_panel=(250, 180), imagen=ojos_compuestos_logo, tamanio_imagen=(165,77))
		boton.connect(callback=self.get_ojos_compuestos, sonido_select=self.sonido_select)
		x = w*3 + w/2
		y = h*1 - h/2
		boton.set_posicion(punto=(x,y))
		self.widgets.add(boton)
        '''
        path = os.path.join(BASE_PATH, "Iconos", "bichos.png")
        imagen = pygame.image.load(path)
        titulo = pygame.sprite.Sprite()
        titulo.image = imagen
        titulo.rect = titulo.image.get_rect()
        titulo.rect.centerx = RESOLUCION_INICIAL[0] / 2
        titulo.rect.centery = RESOLUCION_INICIAL[1] / 2
        self.widgets.add(titulo)
