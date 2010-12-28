#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright 2008-2010 Steffen Schaumburg
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU Affero General Public License as published by
#the Free Software Foundation, version 3 of the License.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU Affero General Public License
#along with this program. If not, see <http://www.gnu.org/licenses/>.
#In the "official" distribution you can find the license in agpl-3.0.txt.

import L10n
_ = L10n.get_translation()

import pygtk
pygtk.require('2.0')
import gtk
import os
import sys

import Charset

DEBUG = False

class GuiStove():

    def __init__(self, config, parent, debug=True):
        """Constructor for GraphViewer"""
        self.conf = config
        self.parent = parent

        self.mainHBox = gtk.HBox(False, 0)

        # hierarchy:  self.mainHBox / self.notebook

        self.notebook = gtk.Notebook()
        self.notebook.set_tab_pos(gtk.POS_TOP)
        self.notebook.set_show_tabs(True)
        self.notebook.set_show_border(True)

        self.createFlopTab()
        self.createStudTab()
        self.createDrawTab()


        self.mainHBox.add(self.notebook)

        self.mainHBox.show_all()

        if DEBUG == False:
            warning_string = _("Stove is a GUI mockup of a EV calculation page, and completely non functional.\n")
            warning_string += _("Unless you are interested in developing this feature, please ignore this page.\n")
            warning_string += _("If you are interested in developing the code further see GuiStove.py and Stove.py\n")
            warning_string += _("Thank you")
            self.warning_box(warning_string)


    def warning_box(self, str, diatitle=_("FPDB WARNING")):
        diaWarning = gtk.Dialog(title=diatitle, parent=self.parent, flags=gtk.DIALOG_DESTROY_WITH_PARENT, buttons=(gtk.STOCK_OK,gtk.RESPONSE_OK))

        label = gtk.Label(str)
        diaWarning.vbox.add(label)
        label.show()

        response = diaWarning.run()
        diaWarning.destroy()
        return response


    def get_active_text(combobox):
        model = combobox.get_model()
        active = combobox.get_active()
        if active < 0:
            return None
        return model[active][0]

    def create_combo_box(self, strings):
        combobox = gtk.combo_box_new_text()
        for label in strings:
            combobox.append_text(label)
        combobox.set_active(0)
        return combobox

    def createDrawTab(self):
        tab_title = "Draw"
        label = gtk.Label(tab_title)

        ddbox = gtk.VBox(False, 0)
        self.notebook.append_page(ddbox, label)

    def createStudTab(self):
        tab_title = "Stud"
        label = gtk.Label(tab_title)

        ddbox = gtk.VBox(False, 0)
        self.notebook.append_page(ddbox, label)

    def createFlopTab(self):
        # hierarchy: hbox / ddbox     / ddhbox / Label + flop_games_cb | label + players_cb
        #                 / gamehbox / in_frame / table /
        #                            / out_frame

        tab_title = "Flop"
        label = gtk.Label(tab_title)

        ddbox = gtk.VBox(False, 0)
        self.notebook.append_page(ddbox, label)

        ddhbox = gtk.HBox(False, 0)
        gamehbox = gtk.HBox(False, 0)

        ddbox.add(ddhbox)
        ddbox.add(gamehbox)

        # Combo boxes in the top row

        games =   [ "Holdem", "Omaha", "Omaha 8", ]
        players = [ "2", "3", "4", "5", "6", "7", "8", "9", "10" ]
        flop_games_cb = self.create_combo_box(games)
        players_cb = self.create_combo_box(players)

        label = gtk.Label("Gametype:")
        ddhbox.add(label)
        ddhbox.add(flop_games_cb)
        label = gtk.Label("Players:")
        ddhbox.add(label)
        ddhbox.add(players_cb)

        # Frames for Stove input and output

        in_frame = gtk.Frame("Input:")
        out_frame = gtk.Frame("Output:")

        gamehbox.add(in_frame)
        gamehbox.add(out_frame)

        outstring = """
No board given. Using Monte-Carlo simulation...
Enumerated 2053443 possible plays.
Your hand: (Ad Ac)
Against the range: {
                    AhAd, AhAs, AdAs, KhKd, KhKs, 
                    KhKc, KdKs, KdKc, KsKc, QhQd, 
                    QhQs, QhQc, QdQs, QdQc, QsQc, 
                    JhJd, JhJs, JhJc, JdJs, JdJc, 
                    JsJc
                   }

  Win       Lose       Tie
 69.91%    15.83%    14.26%

"""
        self.outputlabel = gtk.Label(outstring)
        out_frame.add(self.outputlabel)

        # Input Frame
        table = gtk.Table(4, 4, True)
        label = gtk.Label("Board:")
        board = gtk.Entry()
        board.connect("changed", self.set_board_flop, board)

        btn1 = gtk.Button()
        btn1.set_image(gtk.image_new_from_stock(gtk.STOCK_INDEX, gtk.ICON_SIZE_BUTTON))
        #btn.connect('clicked', self._some_function, arg)
        table.attach(label, 0, 1, 0, 1, xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)
        table.attach(board, 1, 2, 0, 1, xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)
        table.attach(btn1, 2, 3, 0, 1, xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)


        label = gtk.Label("Player1:")
        board = gtk.Entry()
        board.connect("changed", self.set_hero_cards_flop, board)
        btn2 = gtk.Button()
        btn2.set_image(gtk.image_new_from_stock(gtk.STOCK_INDEX, gtk.ICON_SIZE_BUTTON))
        #btn.connect('clicked', self._some_function, arg)
        btn3 = gtk.Button()
        btn3.set_image(gtk.image_new_from_stock(gtk.STOCK_INDEX, gtk.ICON_SIZE_BUTTON))
        #btn.connect('clicked', self._some_function, arg)
        table.attach(label, 0, 1, 1, 2, xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)
        table.attach(board, 1, 2, 1, 2, xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)
        table.attach(btn2, 2, 3, 1, 2, xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)
        table.attach(btn3, 3, 4, 1, 2, xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)


        label = gtk.Label("Player2:")
        board = gtk.Entry()
        board.connect("changed", self.set_villain_cards_flop, board)
        btn4 = gtk.Button()
        btn4.set_image(gtk.image_new_from_stock(gtk.STOCK_INDEX, gtk.ICON_SIZE_BUTTON))
        #btn.connect('clicked', self._some_function, arg)
        btn5 = gtk.Button()
        btn5.set_image(gtk.image_new_from_stock(gtk.STOCK_INDEX, gtk.ICON_SIZE_BUTTON))
        #btn.connect('clicked', self._some_function, arg)
        table.attach(label, 0, 1, 2, 3, xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)
        table.attach(board, 1, 2, 2, 3, xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)
        table.attach(btn4, 2, 3, 2, 3, xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)
        table.attach(btn5, 3, 4, 2, 3, xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)
        
        #table.attach(label, i, i+1, j, j+1,)
        in_frame.add(table)

    def set_board_flop(self, caller, string):
        print "DEBUG: called set_board_flop: '%s' '%s'" %(caller ,string)

    def set_hero_cards_flop(self, caller, string):
        print "DEBUG: called set_hero_cards_flop"

    def set_villain_cards_flop(self, caller, string):
        print "DEBUG: called set_villain_cards_flop"



    def get_vbox(self):
        """returns the vbox of this thread"""
        return self.mainHBox
    #end def get_vbox