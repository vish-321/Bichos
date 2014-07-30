#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import gtk
import gobject
#import threading

from EventTraductor.EventTraductor import KeyPressTraduce
from EventTraductor.EventTraductor import KeyReleaseTraduce
from EventTraductor.EventTraductor import MousemotionTraduce
from EventTraductor.EventTraductor import Traduce_button_press_event
from EventTraductor.EventTraductor import Traduce_button_release_event

from Intro.Intro import Intro
from Widgets import Escenario


class Bichos(gtk.Window):

    def __init__(self):

        gtk.Window.__init__(self)

        self.set_title("Bichos")
        self.modify_bg(0, gtk.gdk.color_parse("#ffffff"))
        #self.set_icon_from_file(os.path.join(BASE, "Iconos", "bichos.svg"))
        self.set_resizable(True)
        self.set_size_request(640, 480)
        self.set_border_width(2)
        self.set_position(gtk.WIN_POS_CENTER)

        self.set_events(
            gtk.gdk.KEY_PRESS | gtk.gdk.EXPOSE |
            gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.POINTER_MOTION_HINT_MASK |
            gtk.gdk.BUTTON_MOTION_MASK | gtk.gdk.BUTTON_PRESS_MASK |
            gtk.gdk.BUTTON_RELEASE_MASK)

        self.__button_state = [0, 0, 0]
        self.__mouse_pos = (0, 0)

        self.juego = False

        self.connect("key-press-event", self.__key_press_even)
        self.connect("key-release-event", self.__key_release_even)
        #self.connect("button_press_event", self.__button_press_event)
        #self.connect("button_release_event", self.__button_release_event)
        #self.connect("motion-notify-event", self.__mouse_motion)
        self.connect("delete-event", self.__salir)
        self.connect("realize", self.__do_realize)

        self.show_all()
        print os.getpid()

    #def __button_press_event(self, widget, event):
    #    if self.juego:
    #        Traduce_button_press_event(event)
    #    return False

    #def __button_release_event(self, widget, event):
    #    if self.juego:
    #        Traduce_button_release_event(event)
    #    return False

    #def __mouse_motion(self, widget, event):
    #    if self.juego:
    #        MousemotionTraduce(event, self.juego.RESOLUCION_INICIAL)
    #    return False

    def __key_press_even(self, widget, event):
        if self.juego:
            KeyPressTraduce(event)
        return False

    def __key_release_even(self, widget, event):
        if self.juego:
            KeyReleaseTraduce(event)
        return False

    def __reset(self):
        for child in self.get_children():
            self.remove(child)
            child.destroy()

    def __do_realize(self, widget):
        self.switch(False, 1)

    def __salir(self, widget=None, event=None):
        sys.exit(0)

    def switch(self, widget, valor):
        self.__reset()
        if valor == 1:
            # Introduccion, opciones de juego.
            self.escenario = Escenario()
            self.escenario.connect("new-size", self.__redraw)
            self.add(self.escenario)
            gobject.idle_add(self.__run_intro)

    def __redraw(self, widget, size):
        if self.juego:
            self.juego.escalar(size)

    def __run_intro(self):
        xid = self.escenario.get_property('window').xid
        os.putenv('SDL_WINDOWID', str(xid))
        self.juego = Intro()
        self.juego.connect("exit", self.__salir)
        self.juego.config()
        self.juego.run()
        '''
        game_thread = threading.Thread(
            target=self.juego.run, name='game')
        game_thread.setDaemon(True)
        game_thread.start()
        #self.juego.connect("switch", self.__intro_switch)
        '''
        return False

    def do_draw(self, context):
        rect = self.get_allocation()
        if self.juego:
            self.juego.escalar((rect.width, rect.height))


if __name__ == "__main__":
    Bichos()
    gtk.main()
