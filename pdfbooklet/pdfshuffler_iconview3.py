#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

 PdfShuffler 0.6.0 - GTK+ based utility for splitting, rearrangement and
 modification of PDF documents.
 Copyright (C) 2008-2012 Konstantinos Poulios
 <https://sourceforge.net/projects/pdfshuffler>

 This file is part of PdfShuffler.

 PdfShuffler is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License along
 with this program; if not, write to the Free Software Foundation, Inc.,
 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""

from gi.repository import Gtk, GObject
import cairo

from math import pi as M_PI

class CellRendererImage(Gtk.CellRenderer):
    __gproperties__ = {
            "image": (GObject.TYPE_PYOBJECT, "Image", "Image",
                      GObject.PARAM_READWRITE),
            "width": (GObject.TYPE_FLOAT, "Width", "Width",
                      0., 1.e4, 0., GObject.PARAM_READWRITE),
            "height": (GObject.TYPE_FLOAT, "Height", "Height",
                       0., 1.e4, 0., GObject.PARAM_READWRITE),
            "rotation": (GObject.TYPE_INT, "Rotation", "Rotation",
                         0, 360, 0, GObject.PARAM_READWRITE),
            "scale": (GObject.TYPE_FLOAT, "Scale", "Scale",
                      0.01, 100., 1., GObject.PARAM_READWRITE),
            "resample": (GObject.TYPE_FLOAT,
                     "Resample", "Resample Coefficient",
                      1., 100., 1., GObject.PARAM_READWRITE),
            "cropL": (GObject.TYPE_FLOAT, "CropL", "CropL",
                      0., 1., 0., GObject.PARAM_READWRITE),
            "cropR": (GObject.TYPE_FLOAT, "CropR", "CropR",
                      0., 1., 0., GObject.PARAM_READWRITE),
            "cropT": (GObject.TYPE_FLOAT, "CropT", "CropT",
                      0., 1., 0., GObject.PARAM_READWRITE),
            "cropB": (GObject.TYPE_FLOAT, "CropB", "CropB",
                      0., 1., 0., GObject.PARAM_READWRITE),
    }

    def __init__(self):
##        self.__GObject_init__()            Original code modified in the line below
        Gtk.CellRendererText.__init__(self)
        GObject.GObject.__init__(self)
        self.th1 = 2. # border thickness
        self.th2 = 3. # shadow thickness

    def get_geometry(self):

        rotation = int(self.rotation) % 360
        rotation = ((rotation) / 90) * 90
        if not self.image:
            w0 = w1 = self.width / self.resample
            h0 = h1 = self.height / self.resample
        else:
            w0 = self.image.get_width()
            h0 = self.image.get_height()
            if rotation == 90 or rotation == 270:
                w1, h1 = h0, w0
            else:
                w1, h1 = w0, h0

        x = self.cropL * w1
        y = self.cropT * h1

        scale = self.resample * self.scale
        w2 = int(scale * (1. - self.cropL - self.cropR) * w1)
        h2 = int(scale * (1. - self.cropT - self.cropB) * h1)

        return w0,h0,w1,h1,w2,h2,rotation

    def do_set_property(self, pspec, value):
        setattr(self, pspec.name, value)

    def do_get_property(self, pspec):
        return getattr(self, pspec.name)

    def do_render(self, window, widget, cell_area, \
                 expose_area, flags):
        if not self.image:
            return

        w0,h0,w1,h1,w2,h2,rotation = self.get_geometry()
        th = int(2*self.th1+self.th2)
        w = w2 + th
        h = h2 + th

        x = cell_area.x
        y = cell_area.y
        if cell_area and w > 0 and h > 0:
            x += self.get_property('xalign') * \
                 (cell_area.width - w - self.get_property('xpad'))
            y += self.get_property('yalign') * \
                 (cell_area.height - h - self.get_property('ypad'))

        cr = window   # cr = window.cairo_create()
        cr.translate(x,y)

        x = self.cropL * w1
        y = self.cropT * h1

        #shadow
        cr.set_source_rgb(0.5, 0.5, 1)
        cr.rectangle(th, th, w2, h2)
        cr.fill()

        #border
        cr.set_source_rgb(0, 0, 0)
        cr.rectangle(0, 0, w2+2*self.th1, h2+2*self.th1)
        cr.fill()

        #image
        cr.set_source_rgb(1, 1, 1)
        cr.rectangle(self.th1, self.th1, w2, h2)
        cr.fill_preserve()
        cr.clip()

        cr.translate(self.th1,self.th1)
        scale = self.resample * self.scale
        cr.scale(scale, scale)
        cr.translate(-x,-y)
        if rotation > 0:
            cr.translate(w1/2,h1/2)
            cr.rotate(rotation * M_PI / 180)
            cr.translate(-w0/2,-h0/2)

        cr.set_source_surface(self.image)
        cr.paint()

    def do_get_size(self, widget, cell_area=None):
        x = y = 0
        w0,h0,w1,h1,w2,h2,rotation = self.get_geometry()
        th = int(2*self.th1+self.th2)
        w = w2 + th
        h = h2 + th

        if cell_area and w > 0 and h > 0:
            x = self.get_property('xalign') * \
                (cell_area.width - w - self.get_property('xpad'))
            y = self.get_property('yalign') * \
                (cell_area.height - h - self.get_property('ypad'))
        w += 2 * self.get_property('xpad')
        h += 2 * self.get_property('ypad')
        return int(x), int(y), w, h

