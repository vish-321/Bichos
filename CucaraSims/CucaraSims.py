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

    #__gsignals__ = {
    #"exit": (gobject.SIGNAL_RUN_LAST,
    #    gobject.TYPE_NONE, [])}

    def __init__(self):

        gtk.HPaned.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#ffffff"))

        self.lecciones = []

        derecha = Derecha()
        self.pack2(derecha, resize=False, shrink=False)

        derecha.connect("lectura", self.__run_lectura)

        self.show_all()

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
        gobject.TYPE_NONE, (gobject.TYPE_STRING, ))}

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
        box.pack_start(button, False, False, 5)

        button = ButtonImagen("alimento")
        box.pack_start(button, False, False, 5)

        button = gtk.Button("Salir")
        box.pack_end(button, False, False, 5)
        button.connect("clicked", self.__emit_lectura)

        self.add(box)
        self.show_all()

        self.set_size_request(120, -1)

    def __emit_lectura(self, button):
        self.emit("lectura", button.get_label())


class ButtonImagen(gtk.EventBox):

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
        print imagen
