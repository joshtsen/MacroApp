

import PyQt5
from PyQt5 import sip
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QModelIndex, Qt
from FNBinds import Binds
import json, time

config_path = "config.json"

class BindModel(QtCore.QAbstractListModel):
    def __init__(self, parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.__data = []

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        if index.row() >= len(self.__data):
            return None

        if role == Qt.DisplayRole or role == Qt.EditRole:
            return self.__data[index.row()].value[3]
        elif role == Qt.UserRole:
            return self.__data[index.row()]
        else:
            QtCore.QVariant() # This ended up being important, idk why tho...
            
    def findData(self, item):
        try:
            return self.__data.index(item)
        except ValueError:
            return -1

    def getData(self):
        return self.__data

    def addItem(self, item):
        #self.beginResetModel()
        self.beginInsertRows(QModelIndex(), 0, 0)
        self.__data.append(item)
        self.endInsertRows()
        self.dataChanged.emit(self.index(len(self.__data)-1), self.index(len(self.__data)), [])
        #self.endResetModel()
        return self.index(0)

    def removeItem(self, index):
        if not index.isValid() or index.row() >= len(self.__data):
            return False

        self.beginRemoveRows(QModelIndex(), index.row(), index.row())
        del self.__data[index.row()]
        self.endRemoveRows()
        #self.dataChanged.emit(self.index())

    def rowCount(self, parent=QModelIndex()):
        return len(self.__data)


class Ui_MainWindow(object):
    running = False
    child = None
    availBinds = None
    inUseBinds = None
    allBindsText = [name for name, member in Binds.__members__.items()]
    params = {}
    
    def on_load(self):
        parsed = {}
        fdiag = QtWidgets.QFileDialog()
        fdiag.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        fdiag.setNameFilters(["JSON files *.json"])
        fdiag.selectNameFilter("JSON files *.json")
        fname = fdiag.getOpenFileName(self.loadButton, "Open config file", './', "JSON files *.json")
        if type(fname) is not str:
            return
        with open(fname, 'r') as infile:
            parsed = json.load(infile)
        if parsed["edit_mode"] == "disabled":
            self.disableRadio.click()
        elif parsed["edit_mode"] == "hold":
            self.holdRadio.click()
        else:
            self.autoRadio.click()
        self.switchPickCheck.setChecked(parsed["switch_pick"])
        self.togglePickCheck.setChecked(parsed["toggle_pick"])
        self.instantBuildCheck.setChecked(parsed["instant_build"])
        self.singleResetCheck.setChecked(parsed["single_reset"])
        self.autoSelectCheck.setChecked(parsed["auto_select_edit"])

        #find and insert helper
        def faihelper(combobox, data):
            idx = combobox.findData(data)
            if idx < 0:
                if not self.availBinds.addItem(data[3]):
                    return False
                idx = 0
            combobox.setCurrentIndex(idx)
        
        faihelper(self.togglePickAliasCombo, Binds[parsed["toggle_pick_bind"]])
        faihelper(self.pickAliasCombo, Binds[parsed["pick_bind"]])
        faihelper(self.editAlias1Combo, Binds[parsed["edit_alias"]])
        faihelper(self.editAlias2Combo, Binds[parsed["edit_alias_2"]])
        faihelper(self.resetAliasCombo, Binds[parsed["edit_alias_3"]])
        faihelper(self.editTriggerCombo, Binds[parsed["edit_bind"]])
        faihelper(self.wallTriggerCombo, Binds[parsed["wall_bind"]])
        faihelper(self.wallAliasCombo, Binds[parsed["wall_alias"]])
        faihelper(self.floorTriggerCombo, Binds[parsed["floor_bind"]])
        faihelper(self.floorAliasCombo, Binds[parsed["floor_alias"]])
        faihelper(self.stairTriggerCombo, Binds[parsed["stair_bind"]])
        faihelper(self.stairAliasCombo, Binds[parsed["stair_alias"]])
        faihelper(self.roofTriggerCombo, Binds[parsed["roof_bind"]])
        faihelper(self.roofAliasCombo, Binds[parsed["roof_alias"]])
        faihelper(self.placeBuildAliasCombo, Binds[parsed["place_build_alias"]])
        faihelper(self.resetTriggerCombo, Binds[parsed["reset_bind"]])

        for bindname in parsed["can_cancel_edit"]:
            idx = self.inUseBinds.findData(Binds[bindname])
            if idx < 0:
                self.inUseBinds.addItem(Binds[bindname])




    def on_save(self):
        self.updateParams()
        fdiag = QtWidgets.QFileDialog()
        fdiag.setNameFilters(["JSON files *.json"])
        fdiag.selectNameFilter("JSON files *.json")
        fname = fdiag.getSaveFileName(self.saveButton, "Save config file", './', "JSON files *.json")
        if type(fname) is str:
            with open(fname, 'w+') as outfile:
                json.dump(self.params, outfile)

    def updateParams(self):
        self.params["edit_mode"] = "disabled"
        if self.holdRadio.isChecked():
            self.params["edit_mode"] = "hold"
        elif self.autoRadio.isChecked():
            self.params["edit_mode"] = "auto"
        self.params["switch_pick"] = self.switchPickCheck.isChecked()
        self.params["toggle_pick"] = self.togglePickCheck.isChecked()
        self.params["toggle_pick_bind"] = self.togglePickAliasCombo.currentData().name
        self.params["pick_bind"] = self.pickAliasCombo.currentData().name
        self.params["edit_alias"] = self.editAlias1Combo.currentData().name
        self.params["edit_alias_2"] = self.editAlias2Combo.currentData().name
        self.params["edit_alias_3"] = self.resetAliasCombo.currentData().name
        self.params["edit_bind"] = self.editTriggerCombo.currentData().name
        self.params["instant_build"] = self.instantBuildCheck.isChecked()
        self.params["wall_bind"] = self.wallTriggerCombo.currentData().name
        self.params["wall_alias"] = self.wallAliasCombo.currentData().name
        self.params["floor_bind"] = self.floorTriggerCombo.currentData().name
        self.params["floor_alias"] = self.floorAliasCombo.currentData().name
        self.params["stair_bind"] = self.stairTriggerCombo.currentData().name
        self.params["stair_alias"] = self.stairAliasCombo.currentData().name
        self.params["roof_bind"] = self.roofTriggerCombo.currentData().name
        self.params["roof_alias"] = self.roofAliasCombo.currentData().name
        self.params["place_build_alias"] = self.placeBuildAliasCombo.currentData().name
        self.params["single_reset"] = self.singleResetCheck.isChecked()
        self.params["reset_bind"] = self.resetTriggerCombo.currentData().name
        self.params["auto_select_edit"] = self.autoSelectCheck.isChecked()
        self.params["mouse_reset_bind"] = "RMB"
        self.params["can_cancel_edit"] = [b.name for b in self.inUseBinds.getData()]


    def on_click_start(self):
        if not self.running:
            self.on_save() # NEEDS TO BE CHANGED
            self.tabWidget.setEnabled(False)
            # consider setting priority
            self.child = QtCore.QProcess()
            cmd_string = "./hkmain.exe config.json"
            self.child.start(cmd_string)
            self.child.waitForStarted()
            self.running = True
            self.pushButton.setText("Stop")
        else:
            print("Attempting to kill")
            self.child.write(bytearray("q", "ascii"))
            print("Waiting")
            if not self.child.waitForFinished(5000):
                self.child.kill()
            self.running = False
            self.pushButton.setText("Start")
            self.tabWidget.setEnabled(True)
            return

    def addKeyPopup(self, view):
        newkey, status = QtWidgets.QInputDialog.getItem(self.mainTab, "Add Key/Button", "Valid Binds",  self.allBindsText, 0, False)
        if status and newkey:
            idx = view.model().addItem(Binds[newkey])
            view.setCurrentIndex(idx)

    def delKey(self, view):
        m = view.model()
        idx = view.currentIndex()
        res = m.removeItem(idx)
        return res

    # Just for disabling input fields depending on options
    def disableRadioClicked(self):
        self.editAlias1Combo.setEnabled(False)
        self.editAlias2Combo.setEnabled(False)
        self.editTriggerCombo.setEnabled(False)

    def holdRadioClicked(self):
        self.editAlias1Combo.setEnabled(True)
        self.editAlias2Combo.setEnabled(False)
        self.editTriggerCombo.setEnabled(True)

    def autoRadioClicked(self):
        self.editAlias1Combo.setEnabled(True)
        self.editAlias2Combo.setEnabled(True)
        self.editTriggerCombo.setEnabled(True)

    def singleResetCheckClicked(self):
        status = self.singleResetCheck.isChecked()
        self.resetTriggerCombo.setEnabled(status)
        self.resetAliasCombo.setEnabled(status)

    def instantBuildCheckClicked(self):
        status = self.instantBuildCheck.isChecked()
        self.wallAliasCombo.setEnabled(status)
        self.wallTriggerCombo.setEnabled(status)
        self.floorAliasCombo.setEnabled(status)
        self.floorTriggerCombo.setEnabled(status)
        self.stairAliasCombo.setEnabled(status)
        self.stairTriggerCombo.setEnabled(status)
        self.roofAliasCombo.setEnabled(status)
        self.roofTriggerCombo.setEnabled(status)
        self.placeBuildAliasCombo.setEnabled(status)

    def setupData(self):
        self.availBinds = BindModel()
        self.inUseBinds = BindModel()

        self.availKeysCol.setModel(self.availBinds)
        self.bindsInUseCol.setModel(self.inUseBinds)
        self.editAlias1Combo.setModel(self.availBinds) 
        self.editAlias2Combo.setModel(self.availBinds)
        self.editTriggerCombo.setModel(self.availBinds)
        self.pickAliasCombo.setModel(self.availBinds)
        self.togglePickAliasCombo.setModel(self.availBinds)
        self.placeBuildAliasCombo.setModel(self.availBinds)
        self.resetTriggerCombo.setModel(self.availBinds)
        self.resetAliasCombo.setModel(self.availBinds)
        self.wallTriggerCombo.setModel(self.availBinds)
        self.wallAliasCombo.setModel(self.availBinds)
        self.floorTriggerCombo.setModel(self.availBinds)
        self.floorAliasCombo.setModel(self.availBinds)
        self.stairTriggerCombo.setModel(self.availBinds)
        self.stairAliasCombo.setModel(self.availBinds)
        self.roofTriggerCombo.setModel(self.availBinds)
        self.roofAliasCombo.setModel(self.availBinds)
        self.placeBuildAliasCombo.setModel(self.availBinds)

    def defaultConfig(self):
        inuse = ["LShift", "c", "F5", "MB4", "MB5", "ONE", "TWO", "THREE", "FOUR", "FIVE", "l"]
        for s in inuse:
            self.inUseBinds.addItem(Binds[s])

        avail = ["t", "y", "g", "h", "LShift", "c", "MB4", "MB5", "e", "ZERO", "LMB", "F1", "F2", "F3", "F4"]
        for s in avail:
            self.availBinds.addItem(Binds[s])

        self.autoRadio.click()
        self.switchPickCheck.setChecked(True)
        self.togglePickCheck.setChecked(False)
        self.togglePickAliasCombo.setEnabled(False)

        #findAndSetHelper
        def fASHelper(combobox, data):
            idx = combobox.findData(data)
            combobox.setCurrentIndex(idx)
        
        fASHelper(self.editAlias1Combo, Binds.g)
        fASHelper(self.editAlias2Combo, Binds.h)
        fASHelper(self.editTriggerCombo, Binds.e)
        fASHelper(self.pickAliasCombo, Binds.ZERO)
        self.singleResetCheck.setChecked(True)
        fASHelper(self.resetTriggerCombo, Binds.t)
        fASHelper(self.resetAliasCombo, Binds.g)
        self.instantBuildCheck.setChecked(True)
        fASHelper(self.wallTriggerCombo, Binds.MB4)
        fASHelper(self.wallAliasCombo, Binds.F1)
        fASHelper(self.floorTriggerCombo, Binds.LShift)
        fASHelper(self.floorAliasCombo, Binds.F2)
        fASHelper(self.stairTriggerCombo, Binds.MB5)
        fASHelper(self.stairAliasCombo, Binds.F3)
        fASHelper(self.roofTriggerCombo, Binds.c)
        fASHelper(self.roofAliasCombo, Binds.F4)
        fASHelper(self.placeBuildAliasCombo, Binds.LMB)



    def setupUi(self, MainWindow):
        # From converted file
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(388, 562)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.loadButton = QtWidgets.QPushButton(self.centralwidget)
        self.loadButton.setGeometry(QtCore.QRect(10, 480, 101, 61))
        self.loadButton.setObjectName("loadButton")
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setGeometry(QtCore.QRect(120, 480, 101, 61))
        self.saveButton.setObjectName("saveButton")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setGeometry(QtCore.QRect(10, 20, 371, 451))
        self.tabWidget.setObjectName("tabWidget")
        self.mainTab = QtWidgets.QWidget()
        self.mainTab.setObjectName("mainTab")
        self.addBindInUse = QtWidgets.QPushButton(self.mainTab)
        self.addBindInUse.setGeometry(QtCore.QRect(10, 290, 81, 21))
        self.addBindInUse.setObjectName("addBindInUse")
        self.deleteItemInUse = QtWidgets.QPushButton(self.mainTab)
        self.deleteItemInUse.setGeometry(QtCore.QRect(100, 290, 81, 21))
        self.deleteItemInUse.setObjectName("deleteItemInUse")
        self.addAvailableKeys = QtWidgets.QPushButton(self.mainTab)
        self.addAvailableKeys.setGeometry(QtCore.QRect(190, 290, 81, 21))
        self.addAvailableKeys.setObjectName("addAvailableKeys")
        self.deleteAvailableKeys = QtWidgets.QPushButton(self.mainTab)
        self.deleteAvailableKeys.setGeometry(QtCore.QRect(280, 290, 81, 21))
        self.deleteAvailableKeys.setObjectName("deleteAvailableKeys")
        self.bindsInUseCol = QtWidgets.QListView(self.mainTab)
        self.bindsInUseCol.setGeometry(QtCore.QRect(10, 30, 171, 251))
        self.bindsInUseCol.setObjectName("bindsInUseCol")
        self.availKeysCol = QtWidgets.QListView(self.mainTab)
        self.availKeysCol.setGeometry(QtCore.QRect(190, 30, 171, 251))
        self.availKeysCol.setObjectName("availKeysCol")
        self.label_17 = QtWidgets.QLabel(self.mainTab)
        self.label_17.setGeometry(QtCore.QRect(20, 10, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(self.mainTab)
        self.label_18.setGeometry(QtCore.QRect(200, 10, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.textBrowser = QtWidgets.QTextBrowser(self.mainTab)
        self.textBrowser.setGeometry(QtCore.QRect(10, 320, 351, 101))
        font = QtGui.QFont()
        font.setPointSize(1)
        self.textBrowser.setFont(font)
        self.textBrowser.setAutoFillBackground(False)
        self.textBrowser.setTabChangesFocus(False)
        self.textBrowser.setObjectName("textBrowser")
        self.tabWidget.addTab(self.mainTab, "")
        self.editTab = QtWidgets.QWidget()
        self.editTab.setObjectName("editTab")
        self.groupBox = QtWidgets.QGroupBox(self.editTab)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 171, 361))
        self.groupBox.setObjectName("groupBox")
        self.editAlias2Combo = QtWidgets.QComboBox(self.groupBox)
        self.editAlias2Combo.setEnabled(True)
        self.editAlias2Combo.setGeometry(QtCore.QRect(10, 160, 91, 22))
        self.editAlias2Combo.setEditable(False)
        self.editAlias2Combo.setObjectName("editAlias2Combo")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 90, 61, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 140, 61, 16))
        self.label_2.setObjectName("label_2")
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        self.label_10.setGeometry(QtCore.QRect(10, 190, 91, 16))
        self.label_10.setObjectName("label_10")
        self.editTriggerCombo = QtWidgets.QComboBox(self.groupBox)
        self.editTriggerCombo.setEnabled(True)
        self.editTriggerCombo.setGeometry(QtCore.QRect(10, 210, 91, 22))
        self.editTriggerCombo.setObjectName("editTriggerCombo")
        self.holdRadio = QtWidgets.QRadioButton(self.groupBox)
        self.holdRadio.setGeometry(QtCore.QRect(10, 20, 81, 17))
        self.holdRadio.setObjectName("holdRadio")
        self.autoRadio = QtWidgets.QRadioButton(self.groupBox)
        self.autoRadio.setGeometry(QtCore.QRect(10, 40, 111, 17))
        self.autoRadio.setObjectName("autoRadio")
        self.disableRadio = QtWidgets.QRadioButton(self.groupBox)
        self.disableRadio.setGeometry(QtCore.QRect(10, 60, 151, 17))
        self.disableRadio.setObjectName("disableRadio")
        self.editAlias1Combo = QtWidgets.QComboBox(self.groupBox)
        self.editAlias1Combo.setGeometry(QtCore.QRect(10, 110, 91, 22))
        self.editAlias1Combo.setObjectName("editAlias1Combo")
        self.groupBox_4 = QtWidgets.QGroupBox(self.editTab)
        self.groupBox_4.setGeometry(QtCore.QRect(190, 10, 171, 361))
        self.groupBox_4.setObjectName("groupBox_4")
        self.pickAliasCombo = QtWidgets.QComboBox(self.groupBox_4)
        self.pickAliasCombo.setGeometry(QtCore.QRect(10, 130, 91, 22))
        self.pickAliasCombo.setObjectName("pickAliasCombo")
        self.togglePickAliasCombo = QtWidgets.QComboBox(self.groupBox_4)
        self.togglePickAliasCombo.setGeometry(QtCore.QRect(10, 80, 91, 22))
        self.togglePickAliasCombo.setObjectName("togglePickAliasCombo")
        self.label_4 = QtWidgets.QLabel(self.groupBox_4)
        self.label_4.setGeometry(QtCore.QRect(10, 110, 121, 16))
        self.label_4.setObjectName("label_4")
        self.label_3 = QtWidgets.QLabel(self.groupBox_4)
        self.label_3.setGeometry(QtCore.QRect(10, 60, 111, 16))
        self.label_3.setObjectName("label_3")
        self.togglePickCheck = QtWidgets.QCheckBox(self.groupBox_4)
        self.togglePickCheck.setGeometry(QtCore.QRect(10, 40, 151, 17))
        self.togglePickCheck.setObjectName("togglePickCheck")
        self.switchPickCheck = QtWidgets.QCheckBox(self.groupBox_4)
        self.switchPickCheck.setGeometry(QtCore.QRect(10, 20, 161, 17))
        self.switchPickCheck.setObjectName("switchPickCheck")
        self.autoSelectCheck = QtWidgets.QCheckBox(self.groupBox_4)
        self.autoSelectCheck.setGeometry(QtCore.QRect(10, 170, 141, 21))
        self.autoSelectCheck.setObjectName("autoSelectCheck")
        self.label_20 = QtWidgets.QLabel(self.groupBox_4)
        self.label_20.setGeometry(QtCore.QRect(20, 190, 141, 61))
        self.label_20.setWordWrap(True)
        self.label_20.setObjectName("label_20")
        self.tabWidget.addTab(self.editTab, "")
        self.resetTab = QtWidgets.QWidget()
        self.resetTab.setObjectName("resetTab")
        self.groupBox_3 = QtWidgets.QGroupBox(self.resetTab)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 10, 341, 181))
        self.groupBox_3.setObjectName("groupBox_3")
        self.singleResetCheck = QtWidgets.QCheckBox(self.groupBox_3)
        self.singleResetCheck.setGeometry(QtCore.QRect(10, 20, 70, 17))
        self.singleResetCheck.setObjectName("singleResetCheck")
        self.resetTriggerCombo = QtWidgets.QComboBox(self.groupBox_3)
        self.resetTriggerCombo.setGeometry(QtCore.QRect(10, 70, 91, 22))
        self.resetTriggerCombo.setObjectName("resetTriggerCombo")
        self.resetAliasCombo = QtWidgets.QComboBox(self.groupBox_3)
        self.resetAliasCombo.setGeometry(QtCore.QRect(160, 70, 91, 22))
        self.resetAliasCombo.setObjectName("resetAliasCombo")
        self.label_15 = QtWidgets.QLabel(self.groupBox_3)
        self.label_15.setGeometry(QtCore.QRect(10, 50, 101, 16))
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.groupBox_3)
        self.label_16.setGeometry(QtCore.QRect(160, 50, 51, 16))
        self.label_16.setObjectName("label_16")
        self.label_19 = QtWidgets.QLabel(self.groupBox_3)
        self.label_19.setGeometry(QtCore.QRect(160, 100, 171, 51))
        self.label_19.setWordWrap(True)
        self.label_19.setObjectName("label_19")
        self.tabWidget.addTab(self.resetTab, "")
        self.buildTab = QtWidgets.QWidget()
        self.buildTab.setObjectName("buildTab")
        self.groupBox_2 = QtWidgets.QGroupBox(self.buildTab)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 10, 341, 271))
        self.groupBox_2.setObjectName("groupBox_2")
        self.instantBuildCheck = QtWidgets.QCheckBox(self.groupBox_2)
        self.instantBuildCheck.setGeometry(QtCore.QRect(10, 20, 70, 17))
        self.instantBuildCheck.setObjectName("instantBuildCheck")
        self.label_9 = QtWidgets.QLabel(self.groupBox_2)
        self.label_9.setGeometry(QtCore.QRect(10, 190, 91, 16))
        self.label_9.setObjectName("label_9")
        self.placeBuildAliasCombo = QtWidgets.QComboBox(self.groupBox_2)
        self.placeBuildAliasCombo.setGeometry(QtCore.QRect(100, 190, 91, 22))
        self.placeBuildAliasCombo.setObjectName("placeBuildAliasCombo")
        self.label_21 = QtWidgets.QLabel(self.groupBox_2)
        self.label_21.setGeometry(QtCore.QRect(10, 40, 71, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_21.setFont(font)
        self.label_21.setObjectName("label_21")
        self.label_22 = QtWidgets.QLabel(self.groupBox_2)
        self.label_22.setGeometry(QtCore.QRect(30, 70, 51, 16))
        self.label_22.setObjectName("label_22")
        self.label_23 = QtWidgets.QLabel(self.groupBox_2)
        self.label_23.setGeometry(QtCore.QRect(30, 100, 51, 16))
        self.label_23.setObjectName("label_23")
        self.label_24 = QtWidgets.QLabel(self.groupBox_2)
        self.label_24.setGeometry(QtCore.QRect(30, 130, 47, 13))
        self.label_24.setObjectName("label_24")
        self.wallTriggerCombo = QtWidgets.QComboBox(self.groupBox_2)
        self.wallTriggerCombo.setGeometry(QtCore.QRect(60, 70, 91, 22))
        self.wallTriggerCombo.setObjectName("wallTriggerCombo")
        self.roofTriggerCombo = QtWidgets.QComboBox(self.groupBox_2)
        self.roofTriggerCombo.setGeometry(QtCore.QRect(60, 160, 91, 22))
        self.roofTriggerCombo.setObjectName("roofTriggerCombo")
        self.label_25 = QtWidgets.QLabel(self.groupBox_2)
        self.label_25.setGeometry(QtCore.QRect(30, 160, 51, 16))
        self.label_25.setObjectName("label_25")
        self.floorTriggerCombo = QtWidgets.QComboBox(self.groupBox_2)
        self.floorTriggerCombo.setGeometry(QtCore.QRect(60, 100, 91, 22))
        self.floorTriggerCombo.setObjectName("floorTriggerCombo")
        self.stairTriggerCombo = QtWidgets.QComboBox(self.groupBox_2)
        self.stairTriggerCombo.setGeometry(QtCore.QRect(60, 130, 91, 22))
        self.stairTriggerCombo.setObjectName("stairTriggerCombo")
        self.label_26 = QtWidgets.QLabel(self.groupBox_2)
        self.label_26.setGeometry(QtCore.QRect(170, 40, 71, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_26.setFont(font)
        self.label_26.setObjectName("label_26")
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setGeometry(QtCore.QRect(190, 70, 51, 16))
        self.label_7.setObjectName("label_7")
        self.stairAliasCombo = QtWidgets.QComboBox(self.groupBox_2)
        self.stairAliasCombo.setGeometry(QtCore.QRect(220, 130, 91, 22))
        self.stairAliasCombo.setObjectName("stairAliasCombo")
        self.floorAliasCombo = QtWidgets.QComboBox(self.groupBox_2)
        self.floorAliasCombo.setGeometry(QtCore.QRect(220, 100, 91, 22))
        self.floorAliasCombo.setObjectName("floorAliasCombo")
        self.wallAliasCombo = QtWidgets.QComboBox(self.groupBox_2)
        self.wallAliasCombo.setGeometry(QtCore.QRect(220, 70, 91, 22))
        self.wallAliasCombo.setObjectName("wallAliasCombo")
        self.roofAliasCombo = QtWidgets.QComboBox(self.groupBox_2)
        self.roofAliasCombo.setGeometry(QtCore.QRect(220, 160, 91, 22))
        self.roofAliasCombo.setObjectName("roofAliasCombo")
        self.label_11 = QtWidgets.QLabel(self.groupBox_2)
        self.label_11.setGeometry(QtCore.QRect(190, 100, 51, 16))
        self.label_11.setObjectName("label_11")
        self.label_13 = QtWidgets.QLabel(self.groupBox_2)
        self.label_13.setGeometry(QtCore.QRect(190, 130, 51, 16))
        self.label_13.setObjectName("label_13")
        self.label_27 = QtWidgets.QLabel(self.groupBox_2)
        self.label_27.setGeometry(QtCore.QRect(190, 160, 31, 16))
        self.label_27.setObjectName("label_27")
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setGeometry(QtCore.QRect(20, 220, 171, 51))
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName("label_5")
        self.tabWidget.addTab(self.buildTab, "")
        self.startStopButton = QtWidgets.QPushButton(self.centralwidget)
        self.startStopButton.setGeometry(QtCore.QRect(280, 480, 101, 61))
        self.startStopButton.setObjectName("startStopButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        # end
        
        self.setupData()
        self.defaultConfig()
        self.startStopButton.clicked.connect(self.on_click_start)
        self.loadButton.clicked.connect(self.on_load)
        self.saveButton.clicked.connect(self.on_save)
        self.switchPickCheck.clicked.connect(lambda: self.pickAliasCombo.setEnabled(self.switchPickCheck.isChecked()))
        self.togglePickCheck.clicked.connect(lambda: self.togglePickAliasCombo.setEnabled(self.togglePickCheck.isChecked()))
        self.holdRadio.clicked.connect(self.holdRadioClicked)
        self.autoRadio.clicked.connect(self.autoRadioClicked)
        self.disableRadio.clicked.connect(self.disableRadioClicked)
        self.singleResetCheck.clicked.connect(self.singleResetCheckClicked)
        self.instantBuildCheck.clicked.connect(self.instantBuildCheckClicked)
        self.addAvailableKeys.clicked.connect(lambda: self.addKeyPopup(self.availKeysCol))
        self.addBindInUse.clicked.connect(lambda: self.addKeyPopup(self.bindsInUseCol))
        self.deleteAvailableKeys.clicked.connect(lambda: self.delKey(self.availKeysCol))
        self.deleteItemInUse.clicked.connect(lambda: self.delKey(self.bindsInUseCol))
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Monty's Macros"))
        self.loadButton.setText(_translate("MainWindow", "Load"))
        self.saveButton.setText(_translate("MainWindow", "Save"))
        self.addBindInUse.setText(_translate("MainWindow", "Add"))
        self.deleteItemInUse.setText(_translate("MainWindow", "Delete"))
        self.addAvailableKeys.setText(_translate("MainWindow", "Add"))
        self.deleteAvailableKeys.setText(_translate("MainWindow", "Delete"))
        self.label_17.setText(_translate("MainWindow", "Binds in use"))
        self.label_18.setText(_translate("MainWindow", "Available for Macros"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:1pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">Note: Binds in use should include item slot binds, pickaxe bind and build binds (if you are using \"Instant Build\" include the triggers instead of binds). <br />Available binds should include keys/buttons which are otherwise unused within Fortnite and any keys you want to trigger the macro</span></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.mainTab), _translate("MainWindow", "Main"))
        self.groupBox.setTitle(_translate("MainWindow", "Edit Modes"))
        self.label.setText(_translate("MainWindow", "Edit Alias 1:"))
        self.label_2.setText(_translate("MainWindow", "Edit Alias 2:"))
        self.label_10.setText(_translate("MainWindow", "Edit Trigger:"))
        self.holdRadio.setText(_translate("MainWindow", "Hold to Edit"))
        self.autoRadio.setText(_translate("MainWindow", "Auto Confirm Edit"))
        self.disableRadio.setText(_translate("MainWindow", "None (disabe edit modes)"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Other Options"))
        self.label_4.setText(_translate("MainWindow", "Pickaxe Alias:"))
        self.label_3.setText(_translate("MainWindow", "Toggle Pickaxe Alias:"))
        self.togglePickCheck.setText(_translate("MainWindow", "Toggle Pickaxe After Edit"))
        self.switchPickCheck.setText(_translate("MainWindow", "Switch to Pickaxe Before Edit"))
        self.autoSelectCheck.setText(_translate("MainWindow", "Auto Select Edit"))
        self.label_20.setText(_translate("MainWindow", "Note: Assumes LMB bound as \"Select Edit\". Produces \"no click\" edits when combined with \"Hold to Edit\""))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.editTab), _translate("MainWindow", "Edit Options"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Single Tap Edit Reset"))
        self.singleResetCheck.setText(_translate("MainWindow", "Enable"))
        self.label_15.setText(_translate("MainWindow", "Reset Edit Trigger:"))
        self.label_16.setText(_translate("MainWindow", "Edit Alias:"))
        self.label_19.setText(_translate("MainWindow", "Note: If using any edit options, this alias should be the same as one of the alias\' in the \"Edit Options\" tab."))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.resetTab), _translate("MainWindow", "Edit Reset Options"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Instant Build"))
        self.instantBuildCheck.setText(_translate("MainWindow", "Enable"))
        self.label_9.setText(_translate("MainWindow", "Place Build Alias: "))
        self.label_21.setText(_translate("MainWindow", "Trigger: "))
        self.label_22.setText(_translate("MainWindow", "Wall"))
        self.label_23.setText(_translate("MainWindow", "Floor"))
        self.label_24.setText(_translate("MainWindow", "Stair"))
        self.label_25.setText(_translate("MainWindow", "Roof"))
        self.label_26.setText(_translate("MainWindow", "Alias:"))
        self.label_7.setText(_translate("MainWindow", "Wall"))
        self.label_11.setText(_translate("MainWindow", "Floor"))
        self.label_13.setText(_translate("MainWindow", "Stair"))
        self.label_27.setText(_translate("MainWindow", "Roof"))
        self.label_5.setText(_translate("MainWindow", "Note: Not recommended to use LMB as a \"place build\" bind if using instant building."))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.buildTab), _translate("MainWindow", "Instant Build"))
        self.startStopButton.setText(_translate("MainWindow", "Start"))

    


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
