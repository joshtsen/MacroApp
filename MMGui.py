

import PyQt5
from PyQt5 import sip
from PyQt5 import QtCore, QtGui, QtWidgets
from FNBinds import Binds
import json, time

config_path = "config.json"

class Ui_MainWindow(object):
    running = False
    child = None
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
            return

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(637, 562)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 341, 181))
        self.groupBox.setObjectName("groupBox")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton.setGeometry(QtCore.QRect(10, 20, 131, 17))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_2.setGeometry(QtCore.QRect(10, 40, 131, 17))
        self.radioButton_2.setObjectName("radioButton_2")
        self.checkBox = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox.setGeometry(QtCore.QRect(160, 20, 141, 17))
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_2.setGeometry(QtCore.QRect(160, 50, 121, 17))
        self.checkBox_2.setObjectName("checkBox_2")
        self.comboBox_4 = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_4.setGeometry(QtCore.QRect(260, 90, 69, 22))
        self.comboBox_4.setObjectName("comboBox_4")
        self.comboBox_5 = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_5.setGeometry(QtCore.QRect(260, 120, 69, 22))
        self.comboBox_5.setObjectName("comboBox_5")
        self.comboBox_6 = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_6.setGeometry(QtCore.QRect(70, 120, 69, 22))
        self.comboBox_6.setObjectName("comboBox_6")
        self.radioButton_3 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_3.setGeometry(QtCore.QRect(10, 60, 101, 17))
        self.radioButton_3.setObjectName("radioButton_3")
        self.comboBox_11 = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_11.setGeometry(QtCore.QRect(70, 90, 69, 22))
        self.comboBox_11.setObjectName("comboBox_11")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 90, 61, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 120, 61, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(160, 90, 101, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(160, 120, 61, 16))
        self.label_4.setObjectName("label_4")
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        self.label_10.setGeometry(QtCore.QRect(10, 150, 51, 16))
        self.label_10.setObjectName("label_10")
        self.comboBox_16 = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_16.setGeometry(QtCore.QRect(70, 150, 69, 22))
        self.comboBox_16.setObjectName("comboBox_16")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 200, 341, 171))
        self.groupBox_2.setObjectName("groupBox_2")
        self.checkBox_3 = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_3.setGeometry(QtCore.QRect(10, 20, 70, 17))
        self.checkBox_3.setObjectName("checkBox_3")
        self.comboBox = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox.setGeometry(QtCore.QRect(210, 50, 69, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox_2 = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_2.setGeometry(QtCore.QRect(70, 140, 69, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_3 = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_3.setGeometry(QtCore.QRect(70, 110, 69, 22))
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_8 = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_8.setGeometry(QtCore.QRect(70, 50, 69, 22))
        self.comboBox_8.setObjectName("comboBox_8")
        self.comboBox_9 = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_9.setGeometry(QtCore.QRect(70, 80, 69, 22))
        self.comboBox_9.setObjectName("comboBox_9")
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setGeometry(QtCore.QRect(10, 50, 51, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setGeometry(QtCore.QRect(150, 50, 51, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setGeometry(QtCore.QRect(10, 80, 51, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        self.label_8.setGeometry(QtCore.QRect(150, 80, 51, 16))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.groupBox_2)
        self.label_9.setGeometry(QtCore.QRect(100, 20, 91, 16))
        self.label_9.setObjectName("label_9")
        self.label_11 = QtWidgets.QLabel(self.groupBox_2)
        self.label_11.setGeometry(QtCore.QRect(10, 110, 47, 13))
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.groupBox_2)
        self.label_12.setGeometry(QtCore.QRect(150, 110, 51, 16))
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.groupBox_2)
        self.label_13.setGeometry(QtCore.QRect(10, 140, 51, 16))
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.groupBox_2)
        self.label_14.setGeometry(QtCore.QRect(150, 140, 51, 16))
        self.label_14.setObjectName("label_14")
        self.comboBox_12 = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_12.setGeometry(QtCore.QRect(210, 80, 69, 22))
        self.comboBox_12.setObjectName("comboBox_12")
        self.comboBox_13 = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_13.setGeometry(QtCore.QRect(210, 110, 69, 22))
        self.comboBox_13.setObjectName("comboBox_13")
        self.comboBox_14 = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_14.setGeometry(QtCore.QRect(210, 140, 69, 22))
        self.comboBox_14.setObjectName("comboBox_14")
        self.comboBox_15 = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_15.setGeometry(QtCore.QRect(190, 20, 69, 22))
        self.comboBox_15.setObjectName("comboBox_15")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 380, 341, 81))
        self.groupBox_3.setObjectName("groupBox_3")
        self.checkBox_4 = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkBox_4.setGeometry(QtCore.QRect(10, 20, 70, 17))
        self.checkBox_4.setObjectName("checkBox_4")
        self.comboBox_7 = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBox_7.setGeometry(QtCore.QRect(80, 50, 69, 22))
        self.comboBox_7.setObjectName("comboBox_7")
        self.comboBox_10 = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBox_10.setGeometry(QtCore.QRect(230, 50, 69, 22))
        self.comboBox_10.setObjectName("comboBox_10")
        self.label_15 = QtWidgets.QLabel(self.groupBox_3)
        self.label_15.setGeometry(QtCore.QRect(10, 50, 61, 16))
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.groupBox_3)
        self.label_16.setGeometry(QtCore.QRect(170, 50, 51, 16))
        self.label_16.setObjectName("label_16")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 470, 101, 61))
        self.pushButton.setObjectName("pushButton")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(360, 20, 256, 291))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(130, 470, 101, 61))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(250, 470, 101, 61))
        self.pushButton_3.setObjectName("pushButton_3")
        self.lineEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(360, 340, 251, 191))
        self.lineEdit.setObjectName("lineEdit")
        self.label_17 = QtWidgets.QLabel(self.centralwidget)
        self.label_17.setGeometry(QtCore.QRect(370, 320, 81, 21))
        self.label_17.setObjectName("label_17")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        all_binds = [name for name, member in Binds.__members__.items()]
        self.comboBox_4.addItems(all_binds)
        self.comboBox_5.addItems(all_binds)
        self.comboBox_6.addItems(all_binds)
        self.comboBox_11.addItems(all_binds)
        self.comboBox_2.addItems(all_binds)
        self.comboBox_3.addItems(all_binds)
        self.comboBox_8.addItems(all_binds)
        self.comboBox_9.addItems(all_binds)
        self.comboBox.addItems(all_binds)
        self.comboBox_10.addItems(all_binds)
        self.comboBox_12.addItems(all_binds)
        self.comboBox_13.addItems(all_binds)
        self.comboBox_14.addItems(all_binds)
        self.comboBox_15.addItems(all_binds)
        self.comboBox_7.addItems(all_binds)
        self.comboBox_16.addItems(all_binds)

        self.fields["switch_pick"] = self.checkBox
        self.fields["toggle_pick"] = self.checkBox_2
        self.fields["toggle_pick_bind"] = self.comboBox_4
        self.fields["pick_bind"] = self.comboBox_5
        self.fields["edit_alias"] = self.comboBox_11
        self.fields["edit_alias_2"] = self.comboBox_6
        self.fields["edit_bind"] = self.comboBox_16
        self.fields["instant_build"] = self.checkBox_3
        self.fields["wall_bind"] = self.comboBox_8
        self.fields["wall_alias"] = self.comboBox
        self.fields["floor_bind"] = self.comboBox_9
        self.fields["floor_alias"] = self.comboBox_12
        self.fields["stair_bind"] = self.comboBox_3
        self.fields["stair_alias"] = self.comboBox_13
        self.fields["roof_bind"] = self.comboBox_2
        self.fields["roof_alias"] = self.comboBox_14
        self.fields["place_build_alias"] = self.comboBox_15
        self.fields["single_reset"] = self.checkBox_4
        self.fields["reset_bind"] = self.comboBox_7
        self.fields["edit_alias_3"] = self.comboBox_10
        self.fields["can_cancel"] = self.lineEdit

        self.pushButton.clicked.connect(self.on_click_start)
        self.pushButton_2.clicked.connect(self.on_load)
        self.pushButton_3.clicked.connect(self.on_save)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Monty's Macros"))
        self.groupBox.setTitle(_translate("MainWindow", "Edit Modes"))
        self.radioButton.setText(_translate("MainWindow", "Hold to edit"))
        self.radioButton_2.setText(_translate("MainWindow", "Auto confirm edit"))
        self.checkBox.setText(_translate("MainWindow", "Switch to Pickaxe Before"))
        self.checkBox_2.setText(_translate("MainWindow", "Toggle Pickaxe After"))
        self.radioButton_3.setText(_translate("MainWindow", "None (disabed)"))
        self.comboBox_11.setItemText(0, _translate("MainWindow", "a"))
        self.comboBox_11.setItemText(1, _translate("MainWindow", "b"))
        self.comboBox_11.setItemText(2, _translate("MainWindow", "c"))
        self.comboBox_11.setItemText(3, _translate("MainWindow", "d"))
        self.comboBox_11.setItemText(4, _translate("MainWindow", "e"))
        self.label.setText(_translate("MainWindow", "Edit Alias 1"))
        self.label_2.setText(_translate("MainWindow", "Edit Alias 2"))
        self.label_3.setText(_translate("MainWindow", "Toggle Pickaxe Bind"))
        self.label_4.setText(_translate("MainWindow", "Pickaxe Bind"))
        self.label_10.setText(_translate("MainWindow", "Edit Bind"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Instant Build"))
        self.checkBox_3.setText(_translate("MainWindow", "Enable"))
        self.label_5.setText(_translate("MainWindow", "Wall Bind"))
        self.label_6.setText(_translate("MainWindow", "Wall Alias"))
        self.label_7.setText(_translate("MainWindow", "Floor Bind"))
        self.label_8.setText(_translate("MainWindow", "Floor Alias"))
        self.label_9.setText(_translate("MainWindow", "Place Build Alias"))
        self.label_11.setText(_translate("MainWindow", "Stair Bind"))
        self.label_12.setText(_translate("MainWindow", "Stair Alias"))
        self.label_13.setText(_translate("MainWindow", "Roof Bind"))
        self.label_14.setText(_translate("MainWindow", "Roof Alias"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Single Tap Edit Reset"))
        self.checkBox_4.setText(_translate("MainWindow", "Enable"))
        self.label_15.setText(_translate("MainWindow", "Reset Bind"))
        self.label_16.setText(_translate("MainWindow", "Edit Alias"))
        self.pushButton.setText(_translate("MainWindow", "Start"))
        self.textBrowser_2.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">Notes:</span></p>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\"\" style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&quot;Binds&quot; are keys/buttons you will press</li>\n"
"<li style=\"\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&quot;Alias&quot; are keys/buttons which should be bound in game settings</li>\n"
"<li style=\"\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Auto confirm edit requires two edit binds</li>\n"
"<li style=\"\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Hold to edit uses only Edit Alias 1</li>\n"
"<li style=\"\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">It is recommended to not use LMB as &quot;place build alias&quot; because accidental or habitual clicks could cause you to stop turbo building.</li>\n"
"<li style=\"\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Edit Alias for Single Tap Edit Reset should be the same as &quot;Edit Alias 1&quot; under &quot;Edit Modes&quot; (if using edit modes)</li>\n"
"<li syyle=\"\" style=\" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Can Cancel Edit should be a comma separated list of binds which would cancel an edit (i.e. all weapon binds and build binds)</ul></body></html>"))
        self.pushButton_2.setText(_translate("MainWindow", "Load"))
        self.pushButton_3.setText(_translate("MainWindow", "Save"))
        self.label_17.setText(_translate("MainWindow", "Can Cancel Edit"))

        self.radioButton_2.setChecked(True)
        self.fields["instant_build"].setChecked(True)
        self.fields["single_reset"].setChecked(True)
        self.fields["edit_alias"].setCurrentText('g')
        self.fields["edit_alias_2"].setCurrentText('h')
        self.fields["edit_alias_3"].setCurrentText('g')
        self.fields["switch_pick"].setChecked(True)
        self.fields["toggle_pick"].setChecked(True)
        self.fields["toggle_pick_bind"].setCurrentText('l')
        self.fields["pick_bind"].setCurrentText('ZERO')
        self.fields["edit_bind"].setCurrentText('e')
        self.fields["wall_bind"].setCurrentText('MB4')
        self.fields["wall_alias"].setCurrentText('F1')
        self.fields["floor_bind"].setCurrentText('LShift')
        self.fields["floor_alias"].setCurrentText('F2')
        self.fields["roof_bind"].setCurrentText('c')
        self.fields["roof_alias"].setCurrentText('F4')
        self.fields["stair_bind"].setCurrentText('MB5')
        self.fields["stair_alias"].setCurrentText('F3')
        self.fields["place_build_alias"].setCurrentText('j')
        self.fields["reset_bind"].setCurrentText('t')
        can_cancel_list = ["ZERO", "ONE", "TWO", "THREE", "FOUR", "FIVE", "F1", "F2", "F3", "F4"]
        self.fields["can_cancel"].setPlainText(", ".join(can_cancel_list))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
