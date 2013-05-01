
===================================================
TreePyO:  Object Hierarcy Tree Navigator for Python
===================================================


GENERAL
=======
TreePyO enables visual navigation of full object hierarcy within a Python
runtime. It is ideal for grasping internals of object groups and applications.
Objects, members, classes, functions, modules, lists, dicts, etc; namely,
any object hierarcy can be navigated as they are alive.


SCREENSHOT
==========
See TreePyO as it navigates itself:

https://github.com/imrn/TreePyO/blob/master/treepyo.jpg


REQUIREMENTS
============
- Python >= 3.2
- GObject Introspection (GIR)
- Python GIR wrapper
- GTK3

On Debian or Ubuntu systems issue the following command:
(Adjust versions for current releases if needed)::

    apt-get install python3-gi gir1.2-gtk-3.0


USAGE & DETAILS
===============

- For a demo, just run the file 'treepyo.py'. Object tree will appear with
  two root nodes: a) '__main__' module b) the Window itself. Browsing the tree
  is trivial. However, familarity with Python internals is recommended.
  Please see: http://docs.python.org/3.2/reference/datamodel.html

- 'Find as you type' search is available for expanded nodes.

- Collapsing and reexpanding an object node refreshes the children.
  (Except for SubGroup nodes. See below.) SubGroups are refreshed when real
  parent object is collapsed and reexpanded.

- While navigating, you'll encounter nodes with trailing '+'.
  (i.e 'Modules +', 'Functions +') They are SubGroup nodes. They do
  not correspond to actual python objects. They are logical groups whose
  members would otherwise appear right under their parent. Grouping logic
  depends on the purpose and can be customized via
  TreePyO.testExpandRow function.

- TreePyO.testExpandRow function is central in the sense that it controls
  what is/is_not shown on the tree and how. In its current form, it shows
  everything and provides some grouping: Python Internals, Modules,
  Getters/Setters, Functions and their arguments.

- TreePyO class inherits from Gtk.ScrolledWindow. You can use it like any
  other widget::


    #!/usr/bin/python3

    import __main__
    from gi.repository import Gtk
    from treepyo import TreePyO

    w = Gtk.Window()
    w.connect('delete-event', Gtk.main_quit)

    tr = TreePyO()
    it = tr.store.get_iter_first()
    tr.append(it, '__main__', __main__)   # Add __main__ module to tree
    tr.append(it, 'window', w)            # Or give it any python object

    w.add(tr)
    w.show_all()

    Gtk.main()


TODOS & PROGRESS (%)
====================

- Decide on the form of a Standard Python Environment view. (40%)

- A primitive context menu is provided.
  Decide on its use for standard view. (10%)

- Compile use cases. Provide patterns for customizing the tree,
  context menu and actions. (0%)


KNOWN ISSUES
============

- Currently, only appends are allowed. Inserts leave the tree at an
  inconsistent state.


COPYRIGHT & LICENSE
===================
Copyright 2013, Imran Geriskovan

TreePyO is released under the terms of MIT license. Please see LICENSE.txt file.
