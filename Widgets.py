#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk
import gobject


class Escenario(gtk.DrawingArea):

    __gsignals__ = {
    "new-size": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, ))}

    def __init__(self):

        gtk.DrawingArea.__init__(self)

        self.modify_bg(0, gtk.gdk.color_parse("#000000"))

        self.connect("expose-event", self.__redraw)
        self.show_all()

    def __redraw(self, widget, event):
        rect = self.get_allocation()
        self.emit("new-size", (rect.width, rect.height))
