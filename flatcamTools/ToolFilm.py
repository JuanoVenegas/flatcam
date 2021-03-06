from FlatCAMTool import FlatCAMTool

from GUIElements import RadioSet, FloatEntry
from PyQt5 import QtGui, QtCore, QtWidgets


class Film(FlatCAMTool):

    toolName = "Film PCB Tool"

    def __init__(self, app):
        FlatCAMTool.__init__(self, app)

        # Title
        title_label = QtWidgets.QLabel("<font size=4><b>%s</b></font>" % self.toolName)
        self.layout.addWidget(title_label)

        # Form Layout
        tf_form_layout = QtWidgets.QFormLayout()
        self.layout.addLayout(tf_form_layout)

        # Type of object for which to create the film
        self.tf_type_obj_combo = QtWidgets.QComboBox()
        self.tf_type_obj_combo.addItem("Gerber")
        self.tf_type_obj_combo.addItem("Excellon")
        self.tf_type_obj_combo.addItem("Geometry")

        # we get rid of item1 ("Excellon") as it is not suitable for creating film
        self.tf_type_obj_combo.view().setRowHidden(1, True)
        self.tf_type_obj_combo.setItemIcon(0, QtGui.QIcon("share/flatcam_icon16.png"))
        self.tf_type_obj_combo.setItemIcon(2, QtGui.QIcon("share/geometry16.png"))

        self.tf_type_obj_combo_label = QtWidgets.QLabel("Object Type:")
        self.tf_type_obj_combo_label.setToolTip(
            "Specify the type of object for which to create the film.\n"
            "The object can be of type: Gerber or Geometry.\n"
            "The selection here decide the type of objects that will be\n"
            "in the Film Object combobox."
        )
        tf_form_layout.addRow(self.tf_type_obj_combo_label, self.tf_type_obj_combo)

        # List of objects for which we can create the film
        self.tf_object_combo = QtWidgets.QComboBox()
        self.tf_object_combo.setModel(self.app.collection)
        self.tf_object_combo.setRootModelIndex(self.app.collection.index(0, 0, QtCore.QModelIndex()))
        self.tf_object_combo.setCurrentIndex(1)
        self.tf_object_label = QtWidgets.QLabel("Film Object:")
        self.tf_object_label.setToolTip(
            "Object for which to create the film."
        )
        tf_form_layout.addRow(self.tf_object_label, self.tf_object_combo)

        # Type of Box Object to be used as an envelope for film creation
        # Within this we can create negative
        self.tf_type_box_combo = QtWidgets.QComboBox()
        self.tf_type_box_combo.addItem("Gerber")
        self.tf_type_box_combo.addItem("Excellon")
        self.tf_type_box_combo.addItem("Geometry")

        # we get rid of item1 ("Excellon") as it is not suitable for box when creating film
        self.tf_type_box_combo.view().setRowHidden(1, True)
        self.tf_type_box_combo.setItemIcon(0, QtGui.QIcon("share/flatcam_icon16.png"))
        self.tf_type_box_combo.setItemIcon(2, QtGui.QIcon("share/geometry16.png"))

        self.tf_type_box_combo_label = QtWidgets.QLabel("Box Type:")
        self.tf_type_box_combo_label.setToolTip(
            "Specify the type of object to be used as an container for\n"
            "film creation. It can be: Gerber or Geometry type."
            "The selection here decide the type of objects that will be\n"
            "in the Box Object combobox."
        )
        tf_form_layout.addRow(self.tf_type_box_combo_label, self.tf_type_box_combo)

        # Box
        self.tf_box_combo = QtWidgets.QComboBox()
        self.tf_box_combo.setModel(self.app.collection)
        self.tf_box_combo.setRootModelIndex(self.app.collection.index(0, 0, QtCore.QModelIndex()))
        self.tf_box_combo.setCurrentIndex(1)

        self.tf_box_combo_label = QtWidgets.QLabel("Box Object:")
        self.tf_box_combo_label.setToolTip(
            "The actual object that is used a container for the\n "
            "selected object for which we create the film.\n"
            "Usually it is the PCB outline but it can be also the\n"
            "same object for which the film is created.")
        tf_form_layout.addRow(self.tf_box_combo_label, self.tf_box_combo)

        # Film Type
        self.film_type = RadioSet([{'label': 'Positive', 'value': 'pos'},
                                     {'label': 'Negative', 'value': 'neg'}])
        self.film_type_label = QtWidgets.QLabel("Film Type:")
        self.film_type_label.setToolTip(
            "Generate a Positive black film or a Negative film.\n"
            "Positive means that it will print the features\n"
            "with black on a white canvas.\n"
            "Negative means that it will print the features\n"
            "with white on a black canvas.\n"
            "The Film format is SVG."
        )
        tf_form_layout.addRow(self.film_type_label, self.film_type)

        # Boundary for negative film generation

        self.boundary_entry = FloatEntry()
        self.boundary_label = QtWidgets.QLabel("Border:")
        self.boundary_label.setToolTip(
            "Specify a border around the object.\n"
            "Only for negative film.\n"
            "It helps if we use as a Box Object the same \n"
            "object as in Film Object. It will create a thick\n"
            "black bar around the actual print allowing for a\n"
            "better delimitation of the outline features which are of\n"
            "white color like the rest and which may confound with the\n"
            "surroundings if not for this border."
        )
        tf_form_layout.addRow(self.boundary_label, self.boundary_entry)

        # Buttons
        hlay = QtWidgets.QHBoxLayout()
        self.layout.addLayout(hlay)
        hlay.addStretch()

        self.film_object_button = QtWidgets.QPushButton("Save Film")
        self.film_object_button.setToolTip(
            "Create a Film for the selected object, within\n"
            "the specified box. Does not create a new \n "
            "FlatCAM object, but directly save it in SVG format\n"
            "which can be opened with Inkscape."
        )
        hlay.addWidget(self.film_object_button)

        self.layout.addStretch()

        ## Signals
        self.film_object_button.clicked.connect(self.on_film_creation)
        self.tf_type_obj_combo.currentIndexChanged.connect(self.on_type_obj_index_changed)
        self.tf_type_box_combo.currentIndexChanged.connect(self.on_type_box_index_changed)

        ## Initialize form
        self.film_type.set_value('neg')
        self.boundary_entry.set_value(0.0)

    def on_type_obj_index_changed(self, index):
        obj_type = self.tf_type_obj_combo.currentIndex()
        self.tf_object_combo.setRootModelIndex(self.app.collection.index(obj_type, 0, QtCore.QModelIndex()))
        self.tf_object_combo.setCurrentIndex(0)

    def on_type_box_index_changed(self, index):
        obj_type = self.tf_type_box_combo.currentIndex()
        self.tf_box_combo.setRootModelIndex(self.app.collection.index(obj_type, 0, QtCore.QModelIndex()))
        self.tf_box_combo.setCurrentIndex(0)

    def run(self):
        FlatCAMTool.run(self)
        self.app.ui.notebook.setTabText(2, "Film Tool")

    def on_film_creation(self):
        try:
            name = self.tf_object_combo.currentText()
        except:
            self.app.inform.emit("[error_notcl] No Film object selected. Load a Film object and retry.")
            return
        try:
            boxname = self.tf_box_combo.currentText()
        except:
            self.app.inform.emit("[error_notcl] No Box object selected. Load a Box object and retry.")
            return

        border = float(self.boundary_entry.get_value())
        if border is None:
            border = 0

        self.app.inform.emit("Generating Film ...")

        if self.film_type.get_value() == "pos":
            try:
                filename, _ = QtWidgets.QFileDialog.getSaveFileName(caption="Export SVG positive",
                                                             directory=self.app.get_last_save_folder(), filter="*.svg")
            except TypeError:
                filename, _ = QtWidgets.QFileDialog.getSaveFileName(caption="Export SVG positive")

            filename = str(filename)

            if str(filename) == "":
                self.app.inform.emit("Export SVG positive cancelled.")
                return
            else:
                self.app.export_svg_black(name, boxname, filename)
        else:
            try:
                filename, _ = QtWidgets.QFileDialog.getSaveFileName(caption="Export SVG negative",
                                                             directory=self.app.get_last_save_folder(), filter="*.svg")
            except TypeError:
                filename, _ = QtWidgets.QFileDialog.getSaveFileName(caption="Export SVG negative")

            filename = str(filename)

            if str(filename) == "":
                self.app.inform.emit("Export SVG negative cancelled.")
                return
            else:
                self.app.export_svg_negative(name, boxname, filename, border)

    def reset_fields(self):
        self.tf_object_combo.setRootModelIndex(self.app.collection.index(0, 0, QtCore.QModelIndex()))
        self.tf_box_combo.setRootModelIndex(self.app.collection.index(0, 0, QtCore.QModelIndex()))
