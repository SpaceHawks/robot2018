from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType, parameterTypes
from pyqtgraph.Qt import QtGui, QtWidgets, QtCore# (the example applies equally well to PySide)
import pyqtgraph as pg
class WheelParameterItem(parameterTypes.WidgetParameterItem):
    emptySignal = QtCore.pyqtSignal()
    def __init__(self, param, depth):
        parameterTypes.WidgetParameterItem.__init__(self, param, depth)
        self.hideWidget = False
        self.subItem = QtGui.QTreeWidgetItem()
        self.addChild(self.subItem)

    def treeWidgetChanged(self):
        ## TODO: fix so that superclass method can be called
        ## (WidgetParameter should just natively support this style)
        # WidgetParameterItem.treeWidgetChanged(self)
        self.treeWidget().setFirstItemColumnSpanned(self.subItem, True)
        self.treeWidget().setItemWidget(self.subItem, 0, self.widget)

        # for now, these are copied from ParameterItem.treeWidgetChanged
        self.setHidden(not self.param.opts.get('visible', True))
        self.setExpanded(self.param.opts.get('expanded', True))

    def setValue(self, value):
        self.frontLeft.setText(str(value[0]))
        self.frontRight.setText(str(value[1]))
        self.rearRight.setText(str(value[2]))
        self.rearLeft.setText(str(value[3]))

    def value(self):
        # output = []
        # val = self.frontLeft.text()
        # if val != '':
        #     output.append(int(val))
        # val = self.frontRight.text()
        # if val != '':
        #     output.append(int(val))
        # val = self.rearRight.text()
        # if val != '':
        #     output.append(int(val))
        # val = self.rearLeft.text()
        # if val != '':
        #     output.append(int(val))
        # return output
        return None



    def makeWidget(self):
        self.widget = QtWidgets.QWidget()
        self.layout = QtWidgets.QGridLayout()
        self.widget.setLayout(self.layout)
        self.frontLeft = QtWidgets.QLabel()
        self.frontRight = QtWidgets.QLabel()
        self.rearLeft = QtWidgets.QLabel()
        self.rearRight = QtWidgets.QLabel()
        self.frontRight = QtWidgets.QLabel()
        self.frontLeft.setText("Front Left")
        self.frontRight.setText("Front Right")
        self.rearRight.setText("Rear Righ")
        self.rearLeft.setText("Rear Left")
        self.layout.addWidget(self.frontLeft, 1, 1)
        self.layout.addWidget(self.frontRight, 1, 2)
        self.layout.addWidget(self.rearLeft, 2, 1)
        self.layout.addWidget(self.rearRight, 2, 2)
        self.widget.setValue = self.setValue
        self.widget.value = self.value
        self.widget.sigChanged = self.frontLeft.linkHovered
        return self.widget

class WheelParameter(Parameter):
    """Editable string; displayed as large text box in the tree."""
    itemClass = WheelParameterItem

class TilterParameterItem(parameterTypes.WidgetParameterItem):
    emptySignal = QtCore.pyqtSignal()
    def __init__(self, param, depth):
        parameterTypes.WidgetParameterItem.__init__(self, param, depth)
        self.hideWidget = False
        self.subItem = QtGui.QTreeWidgetItem()
        self.addChild(self.subItem)

    def treeWidgetChanged(self):
        ## TODO: fix so that superclass method can be called
        ## (WidgetParameter should just natively support this style)
        # WidgetParameterItem.treeWidgetChanged(self)
        self.treeWidget().setFirstItemColumnSpanned(self.subItem, True)
        self.treeWidget().setItemWidget(self.subItem, 0, self.widget)

        # for now, these are copied from ParameterItem.treeWidgetChanged
        self.setHidden(not self.param.opts.get('visible', True))
        self.setExpanded(self.param.opts.get('expanded', True))

    def setValue(self, value):
        self.leftSliderLabel.setText("Left: "+str(value[0]))
        self.rightSliderLabel.setText("Right: "+str(value[1]))

        self.leftSlider.setValue(value[0])
        self.rightSlider.setValue(value[1])

    def value(self):
        return None

    def makeWidget(self):
        self.widget = QtWidgets.QWidget()
        self.layout = QtWidgets.QGridLayout()
        self.widget.setLayout(self.layout)
        # self.layout.setAlignment(pg.QtCore.Qt.AlignCenter)

        self.leftSlider = QtWidgets.QSlider()
        self.rightSlider = QtWidgets.QSlider()
        self.leftSliderLabel = QtWidgets.QLabel()
        self.rightSliderLabel = QtWidgets.QLabel()
        self.leftSlider.setEnabled(False)
        self.rightSlider.setEnabled(False)

        self.leftSliderLabel.setText("Left: ---")
        self.rightSliderLabel.setText("Right: ---")
        self.lineEditSetPos = QtWidgets.QLineEdit()
        self.labelSetPos = QtWidgets.QLabel()
        self.labelSetPos.setText("Set Pos: ")
        self.layout.addWidget(self.leftSlider, 1, 1)
        self.layout.addWidget(self.rightSlider, 1, 2)
        self.layout.addWidget(self.leftSliderLabel, 2, 1)
        self.layout.addWidget(self.rightSliderLabel, 2, 2)
        self.layout.addWidget(self.labelSetPos, 3, 1)
        self.layout.addWidget(self.lineEditSetPos, 3, 2)

        self.widget.setValue = self.setValue
        self.widget.value = self.value
        self.widget.sigChanged = self.lineEditSetPos.returnPressed
        self.lineEditSetPos.returnPressed.connect(self.setPosChange)
        return self.widget

    def setPosChange(self):
        text = self.lineEditSetPos.text()
        if text.isnumeric():
            value = int(text)
            self.param.sigChanged.emit(value)
        else:
            pass




class TilterParameter(Parameter):
    """Editable string; displayed as large text box in the tree."""
    sigChanged = QtCore.Signal(int)
    itemClass = TilterParameterItem

class SliderParameterItem(parameterTypes.WidgetParameterItem):
    emptySignal = QtCore.pyqtSignal()
    def __init__(self, param, depth):
        parameterTypes.WidgetParameterItem.__init__(self, param, depth)
        self.hideWidget = False
        self.subItem = QtGui.QTreeWidgetItem()
        self.addChild(self.subItem)

    def treeWidgetChanged(self):
        ## TODO: fix so that superclass method can be called
        ## (WidgetParameter should just natively support this style)
        # WidgetParameterItem.treeWidgetChanged(self)
        self.treeWidget().setFirstItemColumnSpanned(self.subItem, True)
        self.treeWidget().setItemWidget(self.subItem, 0, self.widget)

        # for now, these are copied from ParameterItem.treeWidgetChanged
        self.setHidden(not self.param.opts.get('visible', True))
        self.setExpanded(self.param.opts.get('expanded', True))

    def setValue(self, value):
        self.posLabel.setText("Curr Pos: "+str(value))
        self.slider.setValue(value)

    def value(self):
        return None

    def makeWidget(self):
        self.widget = QtWidgets.QWidget()
        self.layout = QtWidgets.QGridLayout()
        self.widget.setLayout(self.layout)
        # self.layout.setAlignment(pg.QtCore.Qt.AlignCenter)

        self.slider = QtWidgets.QSlider()
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setEnabled(False)

        self.posLabel = QtWidgets.QLabel()
        self.posLabel.setText("Curr Pos: ---")

        self.lineEditSetPos = QtWidgets.QLineEdit()
        self.labelSetPos = QtWidgets.QLabel()
        self.labelSetPos.setText("Set Pos: ")

        self.layout.addWidget(self.posLabel, 1, 1)
        self.layout.addWidget(self.slider, 1, 2)
        self.layout.addWidget(self.labelSetPos, 2, 1)
        self.layout.addWidget(self.lineEditSetPos, 2, 2)

        self.widget.setValue = self.setValue
        self.widget.value = self.value

        self.widget.sigChanged = self.lineEditSetPos.returnPressed
        self.widget.sigChanged.connect(self.setPosChange)

        return self.widget

    def setPosChange(self):
        text = self.lineEditSetPos.text()
        if text.isnumeric():
            value = int(text)
            self.param.sigChanged.emit(value)
        else:
            pass

class SliderParameter(Parameter):
    """Editable string; displayed as large text box in the tree."""
    sigChanged = QtCore.Signal(int)
    itemClass = SliderParameterItem

class AugerParameterItem(parameterTypes.WidgetParameterItem):
    sigForwardClicked = QtCore.pyqtSignal()
    sigReverseClicked = QtCore.pyqtSignal()
    sigStoplicked = QtCore.pyqtSignal()
    def __init__(self, param, depth):
        parameterTypes.WidgetParameterItem.__init__(self, param, depth)
        self.hideWidget = False
        self.subItem = QtGui.QTreeWidgetItem()
        self.addChild(self.subItem)

    def treeWidgetChanged(self):
        ## TODO: fix so that superclass method can be called
        ## (WidgetParameter should just natively support this style)
        # WidgetParameterItem.treeWidgetChanged(self)
        self.treeWidget().setFirstItemColumnSpanned(self.subItem, True)
        self.treeWidget().setItemWidget(self.subItem, 0, self.widget)

        # for now, these are copied from ParameterItem.treeWidgetChanged
        self.setHidden(not self.param.opts.get('visible', True))
        self.setExpanded(self.param.opts.get('expanded', True))

    def setValue(self, value):
        pass

    def value(self):
        return None

    def makeWidget(self):
        self.widget = QtWidgets.QWidget()
        self.layout = QtWidgets.QGridLayout()
        self.widget.setLayout(self.layout)
        # self.layout.setAlignment(pg.QtCore.Qt.AlignCenter)

        self.buttonForward = QtWidgets.QPushButton("Forward")
        self.buttonStop = QtWidgets.QPushButton("Stop")
        self.buttonReverse = QtWidgets.QPushButton("Reversed")

        self.layout.addWidget(self.buttonForward, 1, 3)
        self.layout.addWidget(self.buttonStop, 1, 2)
        self.layout.addWidget(self.buttonReverse, 1, 1)

        self.widget.setValue = self.setValue
        self.widget.value = self.value

        self.widget.sigChanged = self.buttonStop.clicked
        self.param.sigForwardClicked = self.buttonForward.clicked
        self.param.sigReverseClicked = self.buttonReverse.clicked
        self.param.sigStopClicked = self.buttonStop.clicked

        return self.widget

class AugerParameter(Parameter):
    """Editable string; displayed as large text box in the tree."""
    sigForwardClicked = QtCore.Signal()
    sigBackwardClicked = QtCore.Signal()
    sigStopClicked = QtCore.Signal()
    itemClass = AugerParameterItem


registerParameterType('wheels', WheelParameter, override=True)
registerParameterType('tilter', TilterParameter, override=True)
registerParameterType('slider', SliderParameter, override=True)
registerParameterType('auger', AugerParameter, override=True)