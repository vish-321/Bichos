#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk
import gobject

from EventTraductor.EventTraductor import MousemotionTraduce
from EventTraductor.EventTraductor import Traduce_button_press_event
from EventTraductor.EventTraductor import Traduce_button_release_event


class Escenario(gtk.DrawingArea):

    __gsignals__ = {
    "new-size": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, ))}

    def __init__(self):

        gtk.DrawingArea.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#000000"))

        self.set_events(gtk.gdk.EXPOSE |
            #gtk.gdk.KEY_PRESS | gtk.gdk.KEY_RELEASE |
            #gtk.gdk.KEY_RELEASE_MASK | gtk.gdk.KEY_PRESS_MASK |
            gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.POINTER_MOTION_HINT_MASK |
            gtk.gdk.BUTTON_MOTION_MASK | gtk.gdk.BUTTON_PRESS_MASK |
            gtk.gdk.BUTTON_RELEASE_MASK)

        self.connect("size-allocate", self.__size_request)
        self.connect("expose-event", self.__redraw)

        self.connect("button_press_event", self.__button_press_event)
        self.connect("button_release_event", self.__button_release_event)
        self.connect("motion-notify-event", self.__mouse_motion)

        self.show_all()

    def __button_press_event(self, widget, event):
        if self.get_toplevel().juego:
            Traduce_button_press_event(event,
                self.get_allocation(),
                self.get_toplevel().juego.RESOLUCION_INICIAL)
        return False

    def __button_release_event(self, widget, event):
        if self.get_toplevel().juego:
            Traduce_button_release_event(event,
                self.get_allocation(),
                self.get_toplevel().juego.RESOLUCION_INICIAL)
        return False

    def __mouse_motion(self, widget, event):
        if self.get_toplevel().juego:
            MousemotionTraduce(event,
                self.get_allocation(),
                self.get_toplevel().juego.RESOLUCION_INICIAL)
        return False

    def __size_request(self, widget, event):
        rect = self.get_allocation()
        self.emit("new-size", (rect.width, rect.height))

    def __redraw(self, widget, event):
        rect = self.get_allocation()
        self.emit("new-size", (rect.width, rect.height))
