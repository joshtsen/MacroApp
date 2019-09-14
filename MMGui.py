

import PyQt5
from PyQt5 import sip
from PyQt5 import QtCore, QtGui, QtWidgets
from FNBinds import Binds
import json, time

config_path = "config.json"

class BindModel(QtCore.QAbstractListModel):
    def __init__(self, parent=None):
        super(BindModel, self).__init__(parent)
        self.__data = []

    def data(self, index, role=QtDisplayRole):
        if not index.isValid():
            return None

        if index.row() > len(self.__data):
            return None

        if role == QtCore.DisplayRole or role == QtCore.EditRole:
            return self.__data[index.row()][3]
        else:
            return self.__data[index.row()]

    def rowCount(self, parent=QModelIndex()):
        return len(self.__data)

    def insertRows(self, row, count, parent=QModelIndex()):
        self.beginInsertRows(QModelIndex(), row, row + count - 1)
        self.__data.append([[] for i in range(count)])
        self.endInsertRows()
        return True

    def removeRow(self, row, count, parent=QModelIndex()):
        self.beginRemoveRows(QModelIndex(), row, row + count - 1)
        del self.__data[row:row + count]
        self.endRemoveRows()
        return True

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid() or role != Qt.EditRole:
            return False
        self.__data[index.row()] = value
        self.dataChanged.emit(index, index)
        return True


class Ui_MainWindow(object):
    running = False
    child = None
    availBinds = None
    inUseBinds = None
    fields = {x: None for x in ["edit_mode", "instant_build", "single_reset", "edit_alias", "edit_alias_2", "edit_alias_3", "switch_pick", "toggle_pick", "toggle_pick_bind", "pick_bind", "edit_bind", "wall_bind", "wall_alias", "floor_bind", "floor_alias", "roof_bind", "roof_alias", "stair_bind", "stair_alias", "place_build_alias", "reset_bind", "can_cancel"]}

    def on_load(self):
        parsed = {}
        with open(config_path, 'r') as infile:
            parsed = json.load(infile)
        if parsed["edit_mode"] == "hold":
            self.radioButton.setChecked(True)
        elif parsed["edit_mode"] == "auto":
            self.radioButton_2.setChecked(True)
        else:
            self.radioButton_3.setChecked(True)
        self.fields["single_reset"].setChecked(parsed["single_reset"])
        self.fields["edit_alias"].setCurrentText(parsed["edit_alias"])
        self.fields["edit_alias_2"].setCurrentText(parsed["edit_alias_2"])
        self.fields["edit_alias_3"].setCurrentText(parsed["edit_alias_3"])
        self.fields["instant_build"].setChecked(parsed["instant_build"])
        self.fields["switch_pick"].setChecked(parsed["switch_pick"])
        self.fields["toggle_pick"].setChecked(parsed["toggle_pick"])
        self.fields["toggle_pick_bind"].setCurrentText(parsed["toggle_pick_bind"])
        self.fields["pick_bind"].setCurrentText(parsed["pick_bind"])
        self.fields["edit_bind"].setCurrentText(parsed["edit_bind"])
        self.fields["wall_bind"].setCurrentText(parsed["wall_bind"])
        self.fields["wall_alias"].setCurrentText(parsed["wall_alias"])
        self.fields["floor_bind"].setCurrentText(parsed["floor_bind"])
        self.fields["floor_alias"].setCurrentText(parsed["floor_alias"])
        self.fields["roof_bind"].setCurrentText(parsed["roof_bind"])
        self.fields["roof_alias"].setCurrentText(parsed["roof_alias"])
        self.fields["stair_bind"].setCurrentText(parsed["stair_bind"])
        self.fields["stair_alias"].setCurrentText(parsed["stair_alias"])
        self.fields["place_build_alias"].setCurrentText(parsed["place_build_alias"])
        self.fields["reset_bind"].setCurrentText(parsed["reset_bind"])
        self.fields["can_cancel"].setPlainText(", ".join(parsed["can_cancel"]))

    def on_save(self):
        params = {"edit_mode": "disabled", "instant_build": False, "single_reset": False}
        params["edit_alias_2"] = self.fields["edit_alias"].currentText()
        if self.radioButton.isChecked():
            params["edit_mode"] = "hold"
        elif self.radioButton_2.isChecked():
            params["edit_mode"] = "auto"
            params["edit_alias_2"] = self.comboBox_6.currentText()
        params["switch_pick"] = self.checkBox.isChecked()
        params["toggle_pick"] = self.checkBox_2.isChecked()
        params["toggle_pick_bind"] = self.comboBox_4.currentText()
        params["pick_bind"] = self.comboBox_5.currentText()
        params["edit_alias"] = self.comboBox_11.currentText()
        params["edit_alias_3"] = self.comboBox_10.currentText()
        params["edit_bind"] = self.comboBox_16.currentText()
        params["instant_build"] = self.checkBox_3.isChecked()
        params["wall_bind"] = self.comboBox_8.currentText()
        params["wall_alias"] = self.comboBox.currentText()
        params["floor_bind"] = self.comboBox_9.currentText()
        params["floor_alias"] = self.comboBox_12.currentText()
        params["stair_bind"] = self.comboBox_3.currentText()
        params["stair_alias"] = self.comboBox_13.currentText()
        params["roof_bind"] = self.comboBox_2.currentText()
        params["roof_alias"] = self.comboBox_14.currentText()
        params["place_build_alias"] = self.comboBox_15.currentText()
        params["single_reset"] = self.checkBox_4.isChecked()
        params["reset_bind"] = self.comboBox_7.currentText()
        params["mouse_reset_bind"] = "RMB"
        can_cancel_list = [x for x in self.fields["can_cancel"].toPlainText().split(", ")]
        params["can_cancel"] = can_cancel_list
        with open(config_path, 'w+') as outfile:
            json.dump(params, outfile)

    def on_click_start(self):
        if not self.running:
            #self.on_save()
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

    def addKeyPopup(self, model):

    # Just for disabling input fields depending on options
    def disableRadioClicked(self):

    def editResetCheckClicked(self):

    def instantBuildCheckClicked(self):

    def setupData(self):
        self.availBinds = BindModel(self.availKeysCol)
        self.inUseBinds = BindModel(self.bindsInUseCol)

        self.availKeysCol.setModel(availBinds)
        self.bindsInUseCol.setModel(inUseBinds)
        self.editAlias1Combo.setModel(availBinds)
        self.editAlias2Combo.setModel(availBinds)
        self.editTriggerCombo.setModel(availBinds)
        self.pickAliasCombo.setModel(availBinds)
        self.togglePickAliasCombo.setModel(availBinds)
        self.placeBuildAliasCombo.setModel(availBinds)
        self.resetTriggerCombo.setModel(availBinds)
        self.resetAliasCombo.setModel(availBinds)
        self.wallTriggerCombo.setModel(availBinds)
        self.wallAliasCombo.setModel(availBinds)
        self.floorTriggerCombo.setModel(availBinds)
        self.floorAliasCombo.setModel(availBinds)
        self.stairTriggerCombo.setModel(availBinds)
        self.stairAliasCombo.setModel(availBinds)
        self.roofTriggerCombo.setModel(availBinds)
        self.roofAliasCombo.setModel(availBinds)
        self.placeBuildAliasCombo.setModel(availBinds)

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
        self.scrollArea = QtWidgets.QScrollArea(self.mainTab)
        self.scrollArea.setGeometry(QtCore.QRect(10, 30, 171, 251))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 169, 249))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.bindsInUseCol = QtWidgets.QColumnView(self.scrollAreaWidgetContents)
        self.bindsInUseCol.setGeometry(QtCore.QRect(0, 0, 171, 501))
        self.bindsInUseCol.setObjectName("bindsInUseCol")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scrollArea_2 = QtWidgets.QScrollArea(self.mainTab)
        self.scrollArea_2.setGeometry(QtCore.QRect(190, 30, 171, 251))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 169, 249))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.availKeysCol = QtWidgets.QColumnView(self.scrollAreaWidgetContents_2)
        self.availKeysCol.setGeometry(QtCore.QRect(0, 0, 171, 501))
        self.availKeysCol.setObjectName("availKeysCol")
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
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
        self.resetTriggerCombo.setObjectName("resetTriggerCrombo")
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
        self.startStopButton.clicked.connect(self.on_click_start)
        self.loadButton.clicked.connect(self.on_load)
        self.saveButton.clicked.connect(self.on_save)
        self.addAvailableKeys.connect(lambda: self.addKeyPopup(self.availKeysCol.model()))
        self.addBindInUse.connect(lambda: self.addKeyPopup(self.bindsInUseCol.model()))
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
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">Note: Binds in use should include item slot, pickaxe and build binds (any binds that will cancel editing). It should not include binds such as movement. <br />Available binds SHOULD include keys/buttons which can be used as binds within Fortnite and should NOT include the keys you want to trigger the macro</span></p></body></html>"))
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
