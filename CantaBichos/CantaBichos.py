#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gtk
import gobject

from player import Player

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

    def get_sounds(self):
        sounds = 0
        for child in self.get_children():
            if child.active:
                sounds += 1
        return sounds

    def salir(self):
        for child in self.get_children():
            child.salir()


class Button(gtk.EventBox):

    def __init__(self, image_path):

        gtk.EventBox.__init__(self)

        self.modify_bg(0, gtk.gdk.color_parse("#ffffff"))

        audio = "%s.%s" % (os.path.basename(image_path).split(".")[0], "ogg")
        self.sonido = os.path.join(BASE_PATH, "Sonidos", audio)
        self.player = Player()
        self.player.connect("endfile", self.__replay)

        self.image_path = image_path
        self.nombre = os.path.basename(self.image_path).split(".")[0]
        self.active = False

        boton = gtk.ToolButton()
        boton.modify_bg(0, gtk.gdk.color_parse("#ffffff"))

        self.imagen = gtk.Image()
        self.imagen.modify_bg(0, gtk.gdk.color_parse("#ffffff"))
        boton.set_icon_widget(self.imagen)

        boton.connect("size-allocate", self.__size_request)
        boton.connect("expose-event", self.__redraw)
        boton.connect("clicked", self.__clicked)

        self.add(boton)
        self.show_all()

    def __replay(self, player):
        if self.player:
            self.player.stop()
            self.player.disconnect_by_func(self.__replay)
            del(self.player)
            self.player = False
        self.player = Player()
        self.player.connect("endfile", self.__replay)
        self.player.load(self.sonido)

    def __clicked(self, widget):
        if self.active == False:
            if self.get_parent().get_sounds() < 8:
                self.active = True
                self.modify_bg(0, gtk.gdk.color_parse("#e9b96e"))
                self.imagen.modify_bg(0, gtk.gdk.color_parse("#e9b96e"))
                self.player.load(self.sonido)
            else:
                print "no puedes activar mas de 8 sonidos simultaneos"
        elif self.active == True:
            self.active = False
            self.modify_bg(0, gtk.gdk.color_parse("#ffffff"))
            self.imagen.modify_bg(0, gtk.gdk.color_parse("#ffffff"))
            self.player.stop()

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

    def salir(self):
        self.player.stop()
