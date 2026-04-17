import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
import os
import subprocess

MODULES = {
    "daily-use": [],
    "developer-stack": [],
    "exploitation": [],
    "network": [],
    "osint": [],
    "password-cracking": [],
    "reverse-engineering": [],
    "websecurity": [],
    "wireless": []
}

def get_apps():
    apps = []
    apps_dir = "/usr/share/applications"
    local_dir = os.path.expanduser("~/.local/share/applications")

    for path in [apps_dir, local_dir]:
        if os.path.exists(path):
            for f in os.listdir(path):
                if f.endswith(".desktop"):
                    apps.append(f.replace(".desktop",""))
    return apps


class VisionX(Gtk.Window):
    def __init__(self):
        super().__init__(title="VisionX Launcher")
        self.set_default_size(1000, 600)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.add(box)

        # LEFT PANEL
        self.left = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        box.pack_start(self.left, False, False, 10)

        self.add_button("All Applications", self.show_all_apps)

        for m in MODULES:
            self.add_button(m, lambda w, m=m: self.show_module(m))

        # RIGHT PANEL
        self.right = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.pack_start(self.right, True, True, 10)

        self.label = Gtk.Label(label="Select a module")
        self.right.pack_start(self.label, True, True, 10)

    def add_button(self, name, callback):
        btn = Gtk.Button(label=name)
        btn.connect("clicked", callback)
        self.left.pack_start(btn, False, False, 0)

    def show_all_apps(self, widget):
        apps = get_apps()
        self.display(apps)

    def show_module(self, module):
        self.display([module + " apps placeholder"])

    def display(self, items):
        for child in self.right.get_children():
            self.right.remove(child)

        for i in items:
            btn = Gtk.Button(label=i)
            btn.connect("clicked", self.launch_app)
            self.right.pack_start(btn, False, False, 0)

        self.right.show_all()

    def launch_app(self, widget):
        name = widget.get_label()
        try:
            subprocess.Popen(name)
        except:
            subprocess.Popen(["bash", "-c", name])

win = VisionX()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
