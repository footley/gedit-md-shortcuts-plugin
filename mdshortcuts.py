"""
A Gedit plug in which provides keyboard shortcuts for common markdown
syntax, bold, italics etc.
"""

import re
import os
from gi.repository import GObject, Gtk, Gdk, Gedit # pylint: disable=E0611

class SpellcheckOnSave(GObject.Object, Gedit.ViewActivatable):
    """
    Provides keyboard shortcuts for common markdown syntax, bold, 
    italics etc.
    """
    __gtype_name__ = "mdshortcuts"
    view = GObject.property(type=Gedit.View)
    
    def __init__(self):
        GObject.Object.__init__(self)
        self._doc = None
        self._mime_types = ["text/x-markdown"]
        self._handlers = []
        self._shortcuts = {
            Gdk.KEY_b: (self.surround_selection, ('**', '**')),
            Gdk.KEY_i: (self.surround_selection, ('_', '_')),
        }
    
    def do_activate(self):
        """called when plugin is activated"""
        self._doc = self.view.get_buffer()
        if self._doc.get_mime_type() in self._mime_types:
            self._handlers.append((self.view, 
                self.view.connect('key-press-event', self.on_key_down)))        
    def do_deactivate(self):
        """called when plugin is deactivated, cleanup"""
        for obj, _id in self._handlers:
            obj.disconnect(_id)
    
    def do_update_state(self):
        """state requires update"""
        pass
        
    def on_key_down(self, view, event):
        """
        callback for key down event
        """
        modifier_mask = Gtk.accelerator_get_default_mod_mask()
        event_state = event.state & modifier_mask
        if event_state == Gdk.ModifierType.CONTROL_MASK:
            try:
                func, args = self._shortcuts[event.keyval]
                return func(*args)
            except KeyError:
                pass
    
    def surround_selection(self, prefix, postfix):
        if self._doc.get_has_selection():
            start, end = self._doc.get_selection_bounds()
            self._doc.begin_user_action()
            self._doc.insert(start, prefix)
            start, end = self._doc.get_selection_bounds()
            self._doc.insert(end, postfix)
            self._doc.end_user_action()
            return True



