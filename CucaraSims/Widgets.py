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
import gobject


class Widget_Leccion(gtk.Dialog):

    def __init__(self, parent=None):

        gtk.Dialog.__init__(self, parent=parent,
            buttons=("Cerrar", gtk.RESPONSE_ACCEPT))

        #self.set_decorated(False)
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#ffffff"))
        self.set_border_width(15)

        #imagen = gtk.Image()
        #imagen.set_from_file(os.path.join(BASE_PATH,
        #    "Iconos", "JAMediaCredits.svg"))

        self.vbox.pack_start(Panel(), True, True, 0)
        self.vbox.show_all()


class Panel(gtk.HPaned):

    def __init__(self):

        gtk.HPaned.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#ffffff"))

        #self.pack1(Derecha(), resize=False, shrink=False)
        #self.pack2(Derecha(), resize=False, shrink=False)
        self.show_all()
