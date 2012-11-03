#!/usr/bin/python3

# TreePyO:  Object Hierarcy Tree Navigator for Python
# https://github.com/imrn/TreePyO
#
# Copyright 2012, Imran Geriskovan
# All rights reserved.


import __main__
import inspect
import types
import gi
from gi.repository import Gtk


class TreePyO(Gtk.ScrolledWindow):

    def __init__(self):

        Gtk.ScrolledWindow.__init__(self)
        self.set_size_request(512, 320)

        self.store = Gtk.TreeStore(str, str, str)
        self.storeMap = {}

        self.view = Gtk.TreeView(self.store)
        self.add(self.view)
        self.view.connect('test-expand-row', self.testExpandRow)
        self.view.connect('row-collapsed', self.rowCollapsed)
        self.view.connect('button-press-event', self.on_button_press)

        for i in range(2):
            col = Gtk.TreeViewColumn('', Gtk.CellRendererText(), text = i)
            col.set_resizable(True)
            self.view.append_column(col)

        self.view.set_search_column(0)

        self.menu = Gtk.Menu()
        self.menu.append(Gtk.MenuItem('Hello Menu'))
        self.menu.show_all()


    def clearChildren(self, it):

        path = self.store.get_path(it)
        for pStr, (p, obj) in list(self.storeMap.items()):
            if p.is_descendant(path):
                del self.storeMap[pStr]

        while True:
            itCh = self.store.iter_children(it)
            if itCh:
                self.store.remove(itCh)

            else: break


    def append(self, it, n, obj = None, info = None, subGrp = False):

        if subGrp:
            it = self.store.append(it, (n, '', n))
        else:
            if info is None:
                if obj:
                    info = repr(obj)
                else:
                    info = ''

            if len(info) > 80:
                info = info[:80] + '...'

            it = self.store.append(it, (n, info, ''))
            self.store.append(it, ('', '', ''))

        path = self.store.get_path(it)
        self.storeMap[path.to_string()] = (path, obj)

        return it


    def appendList(self, it, pairs):

        for n, obj in pairs:
            self.append(it, n, obj)


    def rowCollapsed(self, treeview, it, pIn):

        if self.store[it][2]: return

        self.clearChildren(it)
        self.store.append(it, ('', '', ''))


    def testExpandRow(self, treeview, it, pIn):

        if self.store[it][2]: return
        self.clearChildren(it)

        path, obj = self.storeMap[pIn.to_string()]

        if hasattr(obj, '__class__'):
            cl = obj.__class__
            if cl is not obj:
                self.append(it, '__class__', cl)

        if hasattr(obj, '__bases__'):
            bases = obj.__bases__
            self.append(it, '__bases__', bases)

        if hasattr(obj, '__slots__'):
            slots = list(obj.__slots__)
            slots.sort()
            self.appendSubGroup(it, '__slots__', slots)
            self.appendList(it, [(s, getattr(obj, s)) for s in slots])

        if type(obj) is types.FunctionType:
            args = inspect.getfullargspec(obj)
            self.append(it, 'args', args)

        if hasattr(obj, '__dict__'):
            pairs = list(obj.__dict__.items())
            pairs.sort()

            mods,  pairs = Filter(lambda p: type(p[1]) in enums.moduleTypes, pairs)
            funcs, pairs = Filter(lambda p: type(p[1]) in enums.functionTypes + enums.methodTypes, pairs)
            ints,  pairs = Filter(lambda p: p[0] in enums.pyInternals, pairs)
            funcsNew = {}
            for n, o in funcs:
                pref, s, fn = n.partition('_')
                if s and pref in enums.getSetPrefixes:
                    fs = funcsNew.get(fn)
                    if fs:
                        fs.append((n, o))
                    else:
                        funcsNew[fn] = [(n, o)]

                else:
                    funcsNew[n] = [(n, o)]

            self.appendSubGroup(it, 'Internals', ints)
            self.appendSubGroup(it, 'Modules', mods)
            if funcsNew:
                itsub = self.append(it, 'Functions +', None, None, True)
                funcs = list(funcsNew.items())
                funcs.sort()
                for n, fs in funcs:
                    if len(fs) > 1:
                        fs.sort()
                        self.appendSubGroup(itsub, n, fs)
                    else:
                        f = fs[0][1]
                        self.append(itsub, n, f)

            self.appendList(it, pairs)

        if isinstance(obj, dict):
            d = list(obj.items())
            d.sort()
            for k, o in d:
                self.append(it, "[%s]"%str(k), o)

        elif hasattr(obj, '__len__') and obj.__class__ not in enums.noExpand:
            try:
                i = 0
                for o in obj:
                    self.append(it, "[%s]"%str(i), o)
                    i += 1
            except: pass


    def appendSubGroup(self, it, gName, mems):

        if mems:
            itsub = self.append(it, gName + ' +', None, None, True)
            for n, o in mems:
                self.append(itsub, n, o)


    def on_button_press(self, widget, event):

        if event.button == 3:
            pathTup = self.view.get_path_at_pos(int(event.x), int(event.y))
            if pathTup:
                path, column, x, y = pathTup
                self.view.grab_focus()
                self.view.set_cursor(path, column, 0)
                self.menu.popup(None, None, None, None, event.button, event.time)
            return True


class enums:

    noExpand = [bytearray, bytes, str]
    moduleTypes = [types.ModuleType, gi.module.DynamicModule, gi.module.IntrospectionModule]
    getSetPrefixes = ['get', 'set', 'unset']
    functionTypes = [types.FunctionType, gi.types.NativeVFunc]
    methodTypes = [types.MethodType, staticmethod, classmethod]
    pyInternals = ['__builtins__', '__cached__', '__dict__', '__doc__', '__file__',
                   '__gtype__', '__info__',
                   '__module__', '__name__', '__package__', '__version__', '__weakref__']


def Filter(func, lIn):

    tList, fList = [], []
    for i in lIn:
        if func(i):
            tList.append(i)
        else:
            fList.append(i)

    return tList, fList



if __name__ == '__main__':

    w = Gtk.Window()
    w.connect('delete-event', Gtk.main_quit)

    tr = TreePyO()
    it = tr.store.get_iter_first()
    tr.append(it, '__main__', __main__) # Add __main__ module to tree
    tr.append(it, 'window', w)          # Or give it any python object

    w.add(tr)
    w.show_all()

    Gtk.main()