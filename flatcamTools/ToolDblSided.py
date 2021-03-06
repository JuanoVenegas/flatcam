from PyQt5 import QtGui
from GUIElements import RadioSet, EvalEntry, LengthEntry
from FlatCAMTool import FlatCAMTool
from FlatCAMObj import *
from shapely.geometry import Point
from shapely import affinity
from PyQt5 import QtCore

class DblSidedTool(FlatCAMTool):

    toolName = "Double-Sided PCB Tool"

    def __init__(self, app):
        FlatCAMTool.__init__(self, app)

        ## Title
        title_label = QtWidgets.QLabel("<font size=4><b>%s</b></font>" % self.toolName)
        self.layout.addWidget(title_label)

        self.empty_lb = QtWidgets.QLabel("")
        self.layout.addWidget(self.empty_lb)

        ## Grid Layout
        grid_lay = QtWidgets.QGridLayout()
        self.layout.addLayout(grid_lay)

        ## Gerber Object to mirror
        self.gerber_object_combo = QtWidgets.QComboBox()
        self.gerber_object_combo.setModel(self.app.collection)
        self.gerber_object_combo.setRootModelIndex(self.app.collection.index(0, 0, QtCore.QModelIndex()))
        self.gerber_object_combo.setCurrentIndex(1)

        self.botlay_label = QtWidgets.QLabel("<b>GERBER:</b>")
        self.botlay_label.setToolTip(
            "Gerber  to be mirrored."
        )

        self.mirror_gerber_button = QtWidgets.QPushButton("Mirror")
        self.mirror_gerber_button.setToolTip(
            "Mirrors (flips) the specified object around \n"
            "the specified axis. Does not create a new \n"
            "object, but modifies it."
        )
        self.mirror_gerber_button.setFixedWidth(40)

        # grid_lay.addRow("Bottom Layer:", self.object_combo)
        grid_lay.addWidget(self.botlay_label, 0, 0)
        grid_lay.addWidget(self.gerber_object_combo, 1, 0, 1, 2)
        grid_lay.addWidget(self.mirror_gerber_button, 1, 3)

        ## Excellon Object to mirror
        self.exc_object_combo = QtWidgets.QComboBox()
        self.exc_object_combo.setModel(self.app.collection)
        self.exc_object_combo.setRootModelIndex(self.app.collection.index(1, 0, QtCore.QModelIndex()))
        self.exc_object_combo.setCurrentIndex(1)

        self.excobj_label = QtWidgets.QLabel("<b>EXCELLON:</b>")
        self.excobj_label.setToolTip(
            "Excellon Object to be mirrored."
        )

        self.mirror_exc_button = QtWidgets.QPushButton("Mirror")
        self.mirror_exc_button.setToolTip(
            "Mirrors (flips) the specified object around \n"
            "the specified axis. Does not create a new \n"
            "object, but modifies it."
        )
        self.mirror_exc_button.setFixedWidth(40)

        # grid_lay.addRow("Bottom Layer:", self.object_combo)
        grid_lay.addWidget(self.excobj_label, 2, 0)
        grid_lay.addWidget(self.exc_object_combo, 3, 0, 1, 2)
        grid_lay.addWidget(self.mirror_exc_button, 3, 3)

        ## Geometry Object to mirror
        self.geo_object_combo = QtWidgets.QComboBox()
        self.geo_object_combo.setModel(self.app.collection)
        self.geo_object_combo.setRootModelIndex(self.app.collection.index(2, 0, QtCore.QModelIndex()))
        self.geo_object_combo.setCurrentIndex(1)

        self.geoobj_label = QtWidgets.QLabel("<b>GEOMETRY</b>:")
        self.geoobj_label.setToolTip(
            "Geometry Obj to be mirrored."
        )

        self.mirror_geo_button = QtWidgets.QPushButton("Mirror")
        self.mirror_geo_button.setToolTip(
            "Mirrors (flips) the specified object around \n"
            "the specified axis. Does not create a new \n"
            "object, but modifies it."
        )
        self.mirror_geo_button.setFixedWidth(40)

        # grid_lay.addRow("Bottom Layer:", self.object_combo)
        grid_lay.addWidget(self.geoobj_label, 4, 0)
        grid_lay.addWidget(self.geo_object_combo, 5, 0, 1, 2)
        grid_lay.addWidget(self.mirror_geo_button, 5, 3)

        ## Axis
        self.mirror_axis = RadioSet([{'label': 'X', 'value': 'X'},
                                     {'label': 'Y', 'value': 'Y'}])
        self.mirax_label = QtWidgets.QLabel("Mirror Axis:")
        self.mirax_label.setToolTip(
            "Mirror vertically (X) or horizontally (Y)."
        )
        # grid_lay.addRow("Mirror Axis:", self.mirror_axis)
        self.empty_lb1 = QtWidgets.QLabel("")
        grid_lay.addWidget(self.empty_lb1, 6, 0)
        grid_lay.addWidget(self.mirax_label, 7, 0)
        grid_lay.addWidget(self.mirror_axis, 7, 1)

        ## Axis Location
        self.axis_location = RadioSet([{'label': 'Point', 'value': 'point'},
                                       {'label': 'Box', 'value': 'box'}])
        self.axloc_label = QtWidgets.QLabel("Axis Ref:")
        self.axloc_label.setToolTip(
            "The axis should pass through a <b>point</b> or cut\n "
            "a specified <b>box</b> (in a Geometry object) in \n"
            "the middle."
        )
        # grid_lay.addRow("Axis Location:", self.axis_location)
        grid_lay.addWidget(self.axloc_label, 8, 0)
        grid_lay.addWidget(self.axis_location, 8, 1)

        self.empty_lb2 = QtWidgets.QLabel("")
        grid_lay.addWidget(self.empty_lb2, 9, 0)

        ## Point/Box
        self.point_box_container = QtWidgets.QVBoxLayout()
        self.pb_label = QtWidgets.QLabel("<b>Point/Box:</b>")
        self.pb_label.setToolTip(
            "Specify the point (x, y) through which the mirror axis \n "
            "passes or the Geometry object containing a rectangle \n"
            "that the mirror axis cuts in half."
        )
        # grid_lay.addRow("Point/Box:", self.point_box_container)

        self.add_point_button = QtWidgets.QPushButton("Add")
        self.add_point_button.setToolTip(
            "Add the <b>point (x, y)</b> through which the mirror axis \n "
            "passes or the Object containing a rectangle \n"
            "that the mirror axis cuts in half.\n"
            "The point is captured by pressing SHIFT key\n"
            "and left mouse clicking on canvas or you can enter them manually."
        )
        self.add_point_button.setFixedWidth(40)

        grid_lay.addWidget(self.pb_label, 10, 0)
        grid_lay.addLayout(self.point_box_container, 11, 0, 1, 3)
        grid_lay.addWidget(self.add_point_button, 11, 3)

        self.point_entry = EvalEntry()

        self.point_box_container.addWidget(self.point_entry)
        self.box_combo = QtWidgets.QComboBox()
        self.box_combo.setModel(self.app.collection)
        self.box_combo.setRootModelIndex(self.app.collection.index(0, 0, QtCore.QModelIndex()))
        self.box_combo.setCurrentIndex(1)

        self.box_combo_type = QtWidgets.QComboBox()
        self.box_combo_type.addItem("Gerber   Reference Box Object")
        self.box_combo_type.addItem("Excellon Reference Box Object")
        self.box_combo_type.addItem("Geometry Reference Box Object")

        self.point_box_container.addWidget(self.box_combo_type)
        self.point_box_container.addWidget(self.box_combo)
        self.box_combo.hide()
        self.box_combo_type.hide()


        ## Alignment holes
        self.ah_label = QtWidgets.QLabel("<b>Alignment Drill Coordinates:</b>")
        self.ah_label.setToolTip(
            "Alignment holes (x1, y1), (x2, y2), ... "
            "on one side of the mirror axis. For each set of (x, y) coordinates\n"
            "entered here, a pair of drills will be created: one on the\n"
            "coordinates entered and one in mirror position over the axis\n"
            "selected above in the 'Mirror Axis'."
        )
        self.layout.addWidget(self.ah_label)

        grid_lay1 = QtWidgets.QGridLayout()
        self.layout.addLayout(grid_lay1)

        self.alignment_holes = EvalEntry()

        self.add_drill_point_button = QtWidgets.QPushButton("Add")
        self.add_drill_point_button.setToolTip(
            "Add alignment drill holes coords (x1, y1), (x2, y2), ... \n"
            "on one side of the mirror axis.\n"
            "The point(s) can be captured by pressing SHIFT key\n"
            "and left mouse clicking on canvas. Or you can enter them manually."
        )
        self.add_drill_point_button.setFixedWidth(40)

        grid_lay1.addWidget(self.alignment_holes, 0, 0, 1, 2)
        grid_lay1.addWidget(self.add_drill_point_button, 0, 3)

        ## Drill diameter for alignment holes
        self.dt_label = QtWidgets.QLabel("<b>Alignment Drill Creation</b>:")
        self.dt_label.setToolTip(
            "Create a set of alignment drill holes\n"
            "with the specified diameter,\n"
            "at the specified coordinates."
        )
        self.layout.addWidget(self.dt_label)

        grid_lay2 = QtWidgets.QGridLayout()
        self.layout.addLayout(grid_lay2)

        self.drill_dia = LengthEntry()
        self.dd_label = QtWidgets.QLabel("Drill diam.:")
        self.dd_label.setToolTip(
            "Diameter of the drill for the "
            "alignment holes."
        )
        grid_lay2.addWidget(self.dd_label, 0, 0)
        grid_lay2.addWidget(self.drill_dia, 0, 1)

        ## Buttons
        self.create_alignment_hole_button = QtWidgets.QPushButton("Create Excellon Object")
        self.create_alignment_hole_button.setToolTip(
            "Creates an Excellon Object containing the\n"
            "specified alignment holes and their mirror\n"
            "images.")
        # self.create_alignment_hole_button.setFixedWidth(40)
        grid_lay2.addWidget(self.create_alignment_hole_button, 1,0, 1, 2)

        self.reset_button = QtWidgets.QPushButton("Reset")
        self.reset_button.setToolTip(
            "Resets all the fields.")
        self.reset_button.setFixedWidth(40)
        grid_lay2.addWidget(self.reset_button, 1, 2)

        self.layout.addStretch()

        ## Signals
        self.create_alignment_hole_button.clicked.connect(self.on_create_alignment_holes)
        self.mirror_gerber_button.clicked.connect(self.on_mirror_gerber)
        self.mirror_exc_button.clicked.connect(self.on_mirror_exc)
        self.mirror_geo_button.clicked.connect(self.on_mirror_geo)
        self.add_point_button.clicked.connect(self.on_point_add)
        self.add_drill_point_button.clicked.connect(self.on_drill_add)
        self.reset_button.clicked.connect(self.reset_fields)

        self.box_combo_type.currentIndexChanged.connect(self.on_combo_box_type)

        self.axis_location.group_toggle_fn = self.on_toggle_pointbox

        self.drill_values = ""

        ## Initialize form
        self.mirror_axis.set_value('X')
        self.axis_location.set_value('point')
        self.drill_dia.set_value(1)

    def on_combo_box_type(self):
        obj_type = self.box_combo_type.currentIndex()
        self.box_combo.setRootModelIndex(self.app.collection.index(obj_type, 0, QtCore.QModelIndex()))
        self.box_combo.setCurrentIndex(0)

    def on_create_alignment_holes(self):
        axis = self.mirror_axis.get_value()
        mode = self.axis_location.get_value()

        if mode == "point":
            try:
                px, py = self.point_entry.get_value()
            except TypeError:
                self.app.inform.emit("[warning_notcl] 'Point' reference is selected and 'Point' coordinates "
                                     "are missing. Add them and retry.")
                return
        else:
            selection_index = self.box_combo.currentIndex()
            model_index = self.app.collection.index(selection_index, 0, self.gerber_object_combo.rootModelIndex())
            bb_obj = model_index.internalPointer().obj
            xmin, ymin, xmax, ymax = bb_obj.bounds()
            px = 0.5 * (xmin + xmax)
            py = 0.5 * (ymin + ymax)

        xscale, yscale = {"X": (1.0, -1.0), "Y": (-1.0, 1.0)}[axis]

        dia = self.drill_dia.get_value()
        tools = {"1": {"C": dia}}

        # holes = self.alignment_holes.get_value()
        holes = eval('[{}]'.format(self.alignment_holes.text()))
        if not holes:
            self.app.inform.emit("[warning_notcl] There are no Alignment Drill Coordinates to use. Add them and retry.")
            return

        drills = []

        for hole in holes:
            point = Point(hole)
            point_mirror = affinity.scale(point, xscale, yscale, origin=(px, py))
            drills.append({"point": point, "tool": "1"})
            drills.append({"point": point_mirror, "tool": "1"})

        def obj_init(obj_inst, app_inst):
            obj_inst.tools = tools
            obj_inst.drills = drills
            obj_inst.create_geometry()

        self.app.new_object("excellon", "Alignment Drills", obj_init)
        self.drill_values = ''

    def on_mirror_gerber(self):
        selection_index = self.gerber_object_combo.currentIndex()
        # fcobj = self.app.collection.object_list[selection_index]
        model_index = self.app.collection.index(selection_index, 0, self.gerber_object_combo.rootModelIndex())
        try:
            fcobj = model_index.internalPointer().obj
        except Exception as e:
            self.app.inform.emit("[warning_notcl] There is no Gerber object loaded ...")
            return

        if not isinstance(fcobj, FlatCAMGerber):
            self.app.inform.emit("[error_notcl] Only Gerber, Excellon and Geometry objects can be mirrored.")
            return

        axis = self.mirror_axis.get_value()
        mode = self.axis_location.get_value()

        if mode == "point":
            try:
                px, py = self.point_entry.get_value()
            except TypeError:
                self.app.inform.emit("[warning_notcl] 'Point' coordinates missing. "
                                     "Using Origin (0, 0) as mirroring reference.")
                px, py = (0, 0)

        else:
            selection_index_box = self.box_combo.currentIndex()
            model_index_box = self.app.collection.index(selection_index_box, 0, self.box_combo.rootModelIndex())
            try:
                bb_obj = model_index_box.internalPointer().obj
            except Exception as e:
                self.app.inform.emit("[warning_notcl] There is no Box object loaded ...")
                return

            xmin, ymin, xmax, ymax = bb_obj.bounds()
            px = 0.5 * (xmin + xmax)
            py = 0.5 * (ymin + ymax)

        fcobj.mirror(axis, [px, py])
        self.app.object_changed.emit(fcobj)
        fcobj.plot()

    def on_mirror_exc(self):
        selection_index = self.exc_object_combo.currentIndex()
        # fcobj = self.app.collection.object_list[selection_index]
        model_index = self.app.collection.index(selection_index, 0, self.exc_object_combo.rootModelIndex())
        try:
            fcobj = model_index.internalPointer().obj
        except Exception as e:
            self.app.inform.emit("[warning_notcl] There is no Excellon object loaded ...")
            return

        if not isinstance(fcobj, FlatCAMExcellon):
            self.app.inform.emit("[error_notcl] Only Gerber, Excellon and Geometry objects can be mirrored.")
            return

        axis = self.mirror_axis.get_value()
        mode = self.axis_location.get_value()

        if mode == "point":
            px, py = self.point_entry.get_value()
        else:
            selection_index_box = self.box_combo.currentIndex()
            model_index_box = self.app.collection.index(selection_index_box, 0, self.box_combo.rootModelIndex())
            try:
                bb_obj = model_index_box.internalPointer().obj
            except Exception as e:
                self.app.inform.emit("[warning_notcl] There is no Box object loaded ...")
                return

            xmin, ymin, xmax, ymax = bb_obj.bounds()
            px = 0.5 * (xmin + xmax)
            py = 0.5 * (ymin + ymax)

        fcobj.mirror(axis, [px, py])
        self.app.object_changed.emit(fcobj)
        fcobj.plot()

    def on_mirror_geo(self):
        selection_index = self.geo_object_combo.currentIndex()
        # fcobj = self.app.collection.object_list[selection_index]
        model_index = self.app.collection.index(selection_index, 0, self.geo_object_combo.rootModelIndex())
        try:
            fcobj = model_index.internalPointer().obj
        except Exception as e:
            self.app.inform.emit("[warning_notcl] There is no Geometry object loaded ...")
            return

        if not isinstance(fcobj, FlatCAMGeometry):
            self.app.inform.emit("[error_notcl] Only Gerber, Excellon and Geometry objects can be mirrored.")
            return

        axis = self.mirror_axis.get_value()
        mode = self.axis_location.get_value()

        if mode == "point":
            px, py = self.point_entry.get_value()
        else:
            selection_index_box = self.box_combo.currentIndex()
            model_index_box = self.app.collection.index(selection_index_box, 0, self.box_combo.rootModelIndex())
            try:
                bb_obj = model_index_box.internalPointer().obj
            except Exception as e:
                self.app.inform.emit("[warning_notcl] There is no Box object loaded ...")
                return

            xmin, ymin, xmax, ymax = bb_obj.bounds()
            px = 0.5 * (xmin + xmax)
            py = 0.5 * (ymin + ymax)

        fcobj.mirror(axis, [px, py])
        self.app.object_changed.emit(fcobj)
        fcobj.plot()

    def on_point_add(self):
        val = self.app.defaults["global_point_clipboard_format"] % (self.app.pos[0], self.app.pos[1])
        self.point_entry.set_value(val)

    def on_drill_add(self):
        self.drill_values += (self.app.defaults["global_point_clipboard_format"] %
                              (self.app.pos[0], self.app.pos[1])) + ','
        self.alignment_holes.set_value(self.drill_values)

    def on_toggle_pointbox(self):
        if self.axis_location.get_value() == "point":
            self.point_entry.show()
            self.box_combo.hide()
            self.box_combo_type.hide()
            self.add_point_button.setDisabled(False)
        else:
            self.point_entry.hide()
            self.box_combo.show()
            self.box_combo_type.show()
            self.add_point_button.setDisabled(True)

    def reset_fields(self):
        self.gerber_object_combo.setRootModelIndex(self.app.collection.index(0, 0, QtCore.QModelIndex()))
        self.exc_object_combo.setRootModelIndex(self.app.collection.index(1, 0, QtCore.QModelIndex()))
        self.geo_object_combo.setRootModelIndex(self.app.collection.index(2, 0, QtCore.QModelIndex()))
        self.box_combo.setRootModelIndex(self.app.collection.index(0, 0, QtCore.QModelIndex()))

        self.gerber_object_combo.setCurrentIndex(0)
        self.exc_object_combo.setCurrentIndex(0)
        self.geo_object_combo.setCurrentIndex(0)
        self.box_combo.setCurrentIndex(0)
        self.box_combo_type.setCurrentIndex(0)


        self.drill_values = ""
        self.point_entry.set_value("")
        self.alignment_holes.set_value("")
        ## Initialize form
        self.mirror_axis.set_value('X')
        self.axis_location.set_value('point')
        self.drill_dia.set_value(1)

    def run(self):
        FlatCAMTool.run(self)
        self.app.ui.notebook.setTabText(2, "2-Sided Tool")
        self.reset_fields()
