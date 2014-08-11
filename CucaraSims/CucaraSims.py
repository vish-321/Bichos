#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   CucaraSims.py por:
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
import gobject

from Widgets import Widget_Leccion

BASE_PATH = os.path.dirname(__file__)


class CucaraSimsWidget(gtk.HPaned):

    __gsignals__ = {
    "exit": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, []),
    "set-cursor": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, ))}

    def __init__(self):

        gtk.HPaned.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#ffffff"))

        self.lecciones = []

        derecha = Derecha()
        self.pack2(derecha, resize=False, shrink=False)

        derecha.connect("select", self.__set_cursor)
        derecha.connect("lectura", self.__run_lectura)

        self.show_all()

        self.agua_cursor = False
        self.alimento_cursor = False
        self.cursor_root = False
        self.cursor_tipo = False

        gobject.idle_add(self.__config_cursors)

    def __config_cursors(self):
        icono = os.path.join(BASE_PATH, "Imagenes", "jarra.png")
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(icono, -1, 24)
        self.agua_cursor = gtk.gdk.Cursor(
            gtk.gdk.display_get_default(), pixbuf, 0, 0)

        icono = os.path.join(BASE_PATH, "Imagenes", "pan.png")
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(icono, -1, 24)
        self.alimento_cursor = gtk.gdk.Cursor(
            gtk.gdk.display_get_default(), pixbuf, 0, 0)

        self.cursor_root = self.get_toplevel().get_property(
            "window").get_cursor()
        return False

    def __set_cursor(self, widget, tipo):
        win = self.get_toplevel().get_property("window")
        if tipo == "agua":
            if self.cursor_tipo == "agua":
                win.set_cursor(self.cursor_root)
                self.cursor_tipo = False
            else:
                win.set_cursor(self.agua_cursor)
                self.cursor_tipo = "agua"
        elif tipo == "alimento":
            if self.cursor_tipo == "alimento":
                win.set_cursor(self.cursor_root)
                self.cursor_tipo = False
            else:
                win.set_cursor(self.alimento_cursor)
                self.cursor_tipo = "alimento"
        self.emit("set-cursor", self.cursor_tipo)

    def __run_lectura(self, derecha, lectura):
        if lectura == "Salir":
            #self.emit("exit")
            #FIXME: Dialogo para confirmar salir
            return

        self.get_toplevel().juego.pause()
        dialog = Widget_Leccion(
            parent=self.get_toplevel(), lectura=lectura)
        dialog.run()
        dialog.destroy()
        self.get_toplevel().juego.unpause()

    def run_lectura(self, juego, lectura):
        if not lectura in self.lecciones:
            self.lecciones.append(lectura)
            self.get_toplevel().juego.pause()
            dialog = Widget_Leccion(
                parent=self.get_toplevel(), lectura=lectura)
            dialog.run()
            dialog.destroy()
            self.get_toplevel().juego.unpause()

    def salir(self):
        print self.salir


class Derecha(gtk.EventBox):

    __gsignals__ = {
    "lectura": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, )),
    "select": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, ))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#ffffff"))
        self.set_border_width(4)

        box = gtk.VBox()

        l = ["Ciclo Vital", "Muda de Exoesqueleto", "Reproducción",
            "Plaga", "Muerte", "Lectura General"]

        for leccion in l:
            button = gtk.Button(leccion)
            box.pack_start(button, False, False, 5)
            button.connect("clicked", self.__emit_lectura)

        button = ButtonImagen("agua")
        button.connect("select", self.__select_imagen)
        box.pack_start(button, False, False, 5)

        button = ButtonImagen("alimento")
        button.connect("select", self.__select_imagen)
        box.pack_start(button, False, False, 5)

        button = gtk.Button("Salir")
        box.pack_end(button, False, False, 5)
        button.connect("clicked", self.__emit_lectura)

        self.add(box)
        self.show_all()

        self.set_size_request(120, -1)

    def __select_imagen(self, widget, tipo):
        self.emit("select", tipo)

    def __emit_lectura(self, button):
        self.emit("lectura", button.get_label())


class ButtonImagen(gtk.EventBox):

    __gsignals__ = {
    "select": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, ))}

    def __init__(self, tipo):

        gtk.EventBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#ffffff"))
        self.set_border_width(4)

        self.tipo = tipo

        archivo = "jarra.png"
        if self.tipo == "agua":
            archivo = "jarra.png"
        elif self.tipo == "alimento":
            archivo = "pan.png"

        imagen = gtk.Image()
        path = os.path.join(BASE_PATH, "Imagenes", archivo)
        imagen.set_from_file(path)

        self.add(imagen)
        self.show_all()
        self.connect("button-press-event", self.__clicked_image)

    def __clicked_image(self, imagen, event):
        self.emit("select", self.tipo)
