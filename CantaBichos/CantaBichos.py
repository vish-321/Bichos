#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gtk
import gobject

BASE_PATH = os.path.dirname(__file__)


class CantaBichos(gtk.Table):

    def __init__(self):

        gtk.Table.__init__(self, rows=5, columns=6, homogeneous=True)

        print "Corriendo Canta Bichos . . ."

        self.modify_bg(0, gtk.gdk.color_parse("#ffffff"))

        archivos = []
        for arch in os.listdir(os.path.join(BASE_PATH, "Imagenes")):
            archivos.append(os.path.join(os.path.join(
                BASE_PATH, "Imagenes", arch)))

        index = 0
        for col in range(0, 6):
            for row in range(0, 5):
                boton = Button(archivos[index])
                self.attach(boton, col, col + 1, row, row + 1)
                index += 1

        self.show_all()


class Button(gtk.ToolButton):

    def __init__(self, image_path):

        gtk.ToolButton.__init__(self)

        self.modify_bg(0, gtk.gdk.color_parse("#ffffff"))

        self.active = False
        self.image_path = image_path
        self.nombre = os.path.basename(self.image_path).split(".")[0]

        self.imagen = gtk.Image()
        self.imagen.modify_bg(0, gtk.gdk.color_parse("#ffffff"))
        self.set_icon_widget(self.imagen)

        self.connect("size-allocate", self.__size_request)
        self.connect("expose-event", self.__redraw)
        self.connect("clicked", self.__clicked)

        self.show_all()

    def __clicked(self, widget):
        self.active = not self.active
        if self.active:
            self.modify_bg(0, gtk.gdk.color_parse("#ff0000"))
            self.imagen.modify_bg(0, gtk.gdk.color_parse("#ff0000"))
        else:
            self.modify_bg(0, gtk.gdk.color_parse("#ffffff"))
            self.imagen.modify_bg(0, gtk.gdk.color_parse("#ffffff"))

    def __size_request(self, widget, event):
        rect = self.get_allocation()
        gobject.idle_add(self.imagen.set_from_pixbuf,
            gtk.gdk.pixbuf_new_from_file_at_size(
            self.image_path, rect.width, -1))

    def __redraw(self, widget, event):
        rect = self.get_allocation()
        gobject.idle_add(self.imagen.set_from_pixbuf,
            gtk.gdk.pixbuf_new_from_file_at_size(
            self.image_path, rect.width, -1))
