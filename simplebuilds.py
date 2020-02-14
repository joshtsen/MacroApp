# from PyQt5 import QtCore
from pynput import mouse, keyboard
from pynput.keyboard import Key, KeyCode
from pynput.mouse import Button
from enum import Enum
from FNBinds import Binds
# import threading

# Assumes select edit is LMB and reset edit is RMB

class HKThread():
	keyController = keyboard.Controller()
	mouseController = mouse.Controller()
	mouselistener = None
	keylistener = None
	build_count = 0
	placekc = KeyCode.from_char('j')
	floorkc = KeyCode.from_char('c')
	resetkc = KeyCode.from_char('t')
	editkc = KeyCode.from_char('g')
	wallkc = KeyCode.from_char('u')
	rampkc = KeyCode.from_char('k')
	rampreleased = True
	floorreleased = True
	wallreleased = True
	conereleased = True


	def instant_build(self, pressed):
		if pressed:
			self.build_count += 1
			self.keyController.press(self.placekc)
		else:
			self.build_count -= 1
			if self.build_count <= 0:
				self.keyController.release(self.placekc)

	def on_press(self, key):
		if key == self.wallkc and self.wallreleased:
			self.wallreleased = False
			self.instant_build(True)
		elif key == self.floorkc and self.floorreleased:
			self.floorreleased = False
			self.instant_build(True)
		elif key == self.rampkc and self.rampreleased:
			self.rampreleased = False
			self.instant_build(True)
		elif key == Key.shift_l and self.conereleased:
			self.conereleased = False
			self.instant_build(True)

	def on_release(self, key):
		if key == self.wallkc:
			self.wallreleased = True
			self.instant_build(False)
		elif key == self.floorkc:
			self.floorreleased = True
			self.instant_build(False)
		elif key == self.rampkc:
			self.rampreleased = True
			self.instant_build(False)
		elif key == Key.shift_l:
			self.conereleased = True
			self.instant_build(False)

	def on_click(self, x, y, button, pressed):
		if button == Button.four:
			self.keyController.press(self.wallkc)
			self.keyController.release(self.wallkc)
			self.instant_build(pressed)
		elif button == Button.five:
			self.keyController.press(self.rampkc)
			self.keyController.release(self.rampkc)
			self.instant_build(pressed)

	def quit(self):
		self.mouselistener.stop()
		self.keylistener.stop()

	def run(self):
		self.keylistener = keyboard.Listener(on_press = self.on_press, on_release = self.on_release)
		self.keylistener.start()
		self.mouselistener = mouse.Listener(on_click=self.on_click)
		self.mouselistener.start()

if __name__ == "__main__":
	import sys
	hk = HKThread()
	hk.run()
	while "q" != sys.stdin.read(1):
		continue
	hk.quit()


	
