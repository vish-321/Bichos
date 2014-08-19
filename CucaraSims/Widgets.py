#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Widgets.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   Uruguay

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import os
import gtk
import pygame
from pygame.sprite import Sprite

BASE_PATH = os.path.dirname(__file__)


def get_separador(draw=False, ancho=0, expand=False):
    separador = gtk.SeparatorToolItem()
    separador.props.draw = draw
    separador.set_size_request(ancho, -1)
    separador.set_expand(expand)
    return separador


class Widget_Leccion(gtk.Dialog):

    def __init__(self, parent=None, lectura=""):

        gtk.Dialog.__init__(self, parent=parent,
            buttons=("Cerrar", gtk.RESPONSE_ACCEPT))

        self.set_decorated(False)
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#ffffff"))
        self.set_border_width(15)

        self.vbox.pack_start(Panel(), True, True, 0)
        self.vbox.show_all()

        rect = parent.get_allocation()
        self.set_size_request(rect.width, rect.height)

        parent.connect("check-resize", self.__resize)

    def __resize(self, parent):
        rect = parent.get_allocation()
        self.set_size_request(rect.width, rect.height)


class Panel(gtk.HPaned):

    def __init__(self):

        gtk.HPaned.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#ffffff"))

        #self.pack1(Derecha(), resize=False, shrink=False)
        #self.pack2(Derecha(), resize=False, shrink=False)
        self.show_all()


class Cursor(Sprite):

    def __init__(self, tipo):

        Sprite.__init__(self)

        self.tipo = tipo

        path = ""
        if self.tipo == "agua":
            path = os.path.join(BASE_PATH, "Imagenes", "jarra.png")
        elif self.tipo == "alimento":
            path = os.path.join(BASE_PATH, "Imagenes", "pan.png")

        self.image = pygame.image.load(path)
        # pygame.transform.scale(pygame.image.load(path), (24, 48))
        self.rect = self.image.get_bounding_rect()

    def pos(self, pos):
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]


class Alimento(Sprite):

    def __init__(self, tipo, pos):

        Sprite.__init__(self)

        self.tipo = tipo
        self.cantidad = 1500.0

        path = ""
        if self.tipo == "agua":
            path = os.path.join(BASE_PATH, "Imagenes", "jarra.png")
        elif self.tipo == "alimento":
            path = os.path.join(BASE_PATH, "Imagenes", "pan.png")

        self.image = pygame.image.load(path)
        # pygame.transform.scale(pygame.image.load(path), (24, 48))
        self.rect = self.image.get_bounding_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]

    def update(self):
        if self.cantidad <= 0.0:
            self.kill()


class Toolbar(gtk.EventBox):

    def __init__(self):

        gtk.EventBox.__init__(self)

        toolbar = gtk.Toolbar()

        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#ffffff"))
        toolbar.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#ffffff"))

        toolbar.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        imagen = gtk.Image()
        icono = os.path.join(BASE_PATH, "Imagenes", "cucaracha2.png")
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(icono,
            -1, 24)
        imagen.set_from_pixbuf(pixbuf)
        #imagen.modify_bg(0, Gdk.Color(0, 0, 0))
        imagen.show()
        item = gtk.ToolItem()
        item.add(imagen)
        toolbar.insert(item, -1)

        item = gtk.ToolItem()
        self.labelcucas = gtk.Label(" 0H + 0M = 0")
        self.labelcucas.modify_fg(gtk.STATE_NORMAL,
            gtk.gdk.color_parse("#000000"))
        self.labelcucas.show()
        item.add(self.labelcucas)
        toolbar.insert(item, -1)

        toolbar.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        imagen = gtk.Image()
        icono = os.path.join(BASE_PATH, "Imagenes", "huevos.png")
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(icono,
            -1, 24)
        imagen.set_from_pixbuf(pixbuf)
        #imagen.modify_bg(0, Gdk.Color(0, 0, 0))
        imagen.show()
        item = gtk.ToolItem()
        item.add(imagen)
        toolbar.insert(item, -1)

        item = gtk.ToolItem()
        self.labelootecas = gtk.Label(" = 0")
        self.labelootecas.modify_fg(gtk.STATE_NORMAL,
            gtk.gdk.color_parse("#000000"))
        self.labelootecas.show()
        item.add(self.labelootecas)
        toolbar.insert(item, -1)

        #toolbar.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        imagen = gtk.Image()
        icono = os.path.join(BASE_PATH, "Imagenes", "jarra.png")
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(icono, -1, 24)
        imagen.set_from_pixbuf(pixbuf)
        #imagen.modify_bg(0, Gdk.Color(0, 0, 0))
        imagen.show()
        item = gtk.ToolItem()
        item.add(imagen)
        toolbar.insert(item, -1)

        item = gtk.ToolItem()
        self.labelagua = gtk.Label(" = 0")
        self.labelagua.modify_fg(gtk.STATE_NORMAL,
            gtk.gdk.color_parse("#000000"))
        self.labelagua.show()
        item.add(self.labelagua)
        toolbar.insert(item, -1)

        toolbar.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        imagen = gtk.Image()
        icono = os.path.join(BASE_PATH, "Imagenes", "pan.png")
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(icono, -1, 24)
        imagen.set_from_pixbuf(pixbuf)
        #imagen.modify_bg(0, Gdk.Color(0, 0, 0))
        imagen.show()
        item = gtk.ToolItem()
        item.add(imagen)
        toolbar.insert(item, -1)

        item = gtk.ToolItem()
        self.labelalimento = gtk.Label(" = 0")
        self.labelalimento.modify_fg(gtk.STATE_NORMAL,
            gtk.gdk.color_parse("#000000"))
        self.labelalimento.show()
        item.add(self.labelalimento)
        toolbar.insert(item, -1)

        toolbar.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        item = gtk.ToolItem()
        self.labeltiempo = gtk.Label(" Años: 0 Dias: 0 Horas: 0")
        self.labeltiempo.modify_fg(gtk.STATE_NORMAL,
            gtk.gdk.color_parse("#000000"))
        self.labeltiempo.show()
        item.add(self.labeltiempo)
        toolbar.insert(item, -1)

        toolbar.insert(get_separador(draw=False, ancho=0, expand=True), -1)

        self.add(toolbar)
        self.show_all()

    def set_info(self, infocucas, infoootecas, infoagua, infoalimento, tiempo):
        self.labelcucas.set_text(infocucas)
        self.labelootecas.set_text(infoootecas)
        self.labelagua.set_text(infoagua)
        self.labelalimento.set_text(infoalimento)
        self.labeltiempo.set_text(tiempo)


class ToolbarEstado(gtk.EventBox):

    def __init__(self):

        gtk.EventBox.__init__(self)

        toolbar = gtk.Toolbar()

        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#ffffff"))
        toolbar.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#ffffff"))

        toolbar.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        item = gtk.ToolItem()
        self.label = gtk.Label()
        self.label.modify_fg(gtk.STATE_NORMAL,
            gtk.gdk.color_parse("#000000"))
        self.label.show()
        item.add(self.label)
        toolbar.insert(item, -1)

        toolbar.insert(get_separador(draw=False, ancho=0, expand=True), -1)

        self.add(toolbar)
        self.show_all()

    def set_info(self, info):
        self.label.set_text(info)
