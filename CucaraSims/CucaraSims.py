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


class CucaraSimsWidget(gtk.HPaned):

    def __init__(self):

        gtk.HPaned.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#000000"))

        self.lecciones = []

        self.pack2(Derecha(), resize=False, shrink=False)
        self.show_all()

    def run_lectura(self, juego, lectura):
        if not lectura in self.lecciones:
            self.lecciones.append(lectura)
            self.get_toplevel().juego.pause()
            dialog = Widget_Leccion(parent=self.get_toplevel())
            dialog.run()
            dialog.destroy()
            self.get_toplevel().juego.unpause()
        print lectura

    def salir(self):
        pass


class Derecha(gtk.EventBox):

    def __init__(self):

        gtk.EventBox.__init__(self)

        box = gtk.VBox()

        box.pack_start(gtk.Button("Ciclo"), False, False, 0)
        box.pack_start(gtk.Button("Muda"), False, False, 0)
        box.pack_start(gtk.Button("Reproducción"), False, False, 0)
        box.pack_start(gtk.Button("Plaga"), False, False, 0)
        box.pack_start(gtk.Button("Muerte"), False, False, 0)
        box.pack_start(gtk.Button("General"), False, False, 0)
        box.pack_end(gtk.Button("Salir"), False, False, 0)

        self.add(box)
        self.show_all()

        self.set_size_request(100, -1)
