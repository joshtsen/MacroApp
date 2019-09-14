# from PyQt5 import QtCore
from pynput import mouse, keyboard
from pynput.keyboard import Key, KeyCode
from pynput.mouse import Button
from enum import Enum
from FNBinds import Binds
# import threading

# Assumes select edit is LMB and reset edit is RMB

class HKThread():
	edit_open = False
	edit_reset = False
	keyController = keyboard.Controller()
	mouseController = mouse.Controller()
	mouselistener = None
	keylistener = None
	build_count = 0
	params = None
	open_edit = None
	close_edit = None
	handlers = {}
	can_cancel = []

	def press_bind(self,bind):
		bind[1].press(bind[0])

	def release_bind(self, bind):
		bind[1].release(bind[0])

	def tap_bind(self, bind):
		self.press_bind(bind)
		self.release_bind(bind)


	def instant_build(self, alias, pressed):
		if pressed:
			self.tap_bind(alias)
			self.build_count += 1
			self.press_bind(self.params.place_build_alias.value)
		else:
			self.build_count -= 1
			if self.build_count <= 0:
				self.release_bind(self.params.place_build_alias.value)

	def reset_edit(self, pressed):
		if pressed:
			self.tap_bind(self.params.edit_alias.value)
			self.edit_open = True
		else:
			self.tap_bind(self.params.mouse_reset_bind.value)
			self.tap_bind(self.params.edit_alias.value)
			self.edit_open = False

	def hold_to_edit(self, pressed):
		if pressed:
			if not self.edit_open:
				self.open_edit()
				self.edit_open = True
			else:
				self.close_edit()
				self.edit_open = False
		elif self.edit_open:
			self.edit_open = False
			self.close_edit()

	def auto_edit_key(self, pressed):
		if pressed:
			#print(self.edit_open)
			if not self.edit_open:
				self.open_edit()
				#print("FUCK")
				self.edit_open = True
				self.edit_selected = False
				#print("FUCKED")
			else:
				self.edit_open = False
				self.close_edit()

	def on_press(self, key):
		#print(key)
		if self.edit_open:
			if key in self.can_cancel:
				#print("CANCELLED")
				self.edit_open = False
				self.edit_reset = False
		if key in self.handlers:
			self.handlers[key](True)

	def on_release(self, key):
		if key in self.handlers:
			self.handlers[key](False)

	def on_click_auto(self, x, y, button, pressed):
		#print(button)
		#print(pressed)
		#print(self.edit_open)
		if self.edit_open:
			if button == Button.left:
				if not pressed:
					if not self.edit_reset and self.edit_selected:
						self.edit_open = False
						self.edit_reset = False #not needed?
						self.close_edit()
						return
				else:
					if self.edit_open:
						self.edit_selected = True
					self.edit_reset = False
					return
			elif button == self.params.mouse_reset_bind.value[0] and self.edit_open and pressed:
				self.edit_reset = True
			elif pressed and button in self.can_cancel: # NOT NECESSARILY
				# cancelled by mb4 or mb5
				self.edit_open = False
		if button in self.handlers:
			self.handlers[button](pressed)

	def on_click(self, x, y, button, pressed):
		#print(button)
		#print("on_click")
		#print(self.edit_open)
		if self.edit_open: # does nothing if edit mode = disabled
			if pressed and button in self.can_cancel:
				print("Cancelled")
				self.edit_open = False
		if button in self.handlers:
			self.handlers[button](pressed)

	def quit(self):
		self.mouselistener.stop()
		self.keylistener.stop()

	def run(self, input_p):
		input_params = input_p
		translated = {}
		bind_names = [item.name for item in Binds]
		for k, val in input_params.items():
			if val in bind_names:
				key_info = Binds[val].value
				kc = key_info[0]
				if not key_info[1]:
					kc = KeyCode.from_char(kc)
				if key_info[2]:
					translated[k] = (kc, self.keyController)
				else:
					translated[k] = (kc, self.mouseController)
		self.params = Enum("Params", translated)

		for s in input_params["can_cancel"]:
			if s in bind_names:
				key_info = Binds[s].value
				if not key_info[1]:
					self.can_cancel.append(KeyCode.from_char(key_info[0]))
				else:
					self.can_cancel.append(key_info[0])
		#print(self.can_cancel)

		if input_params["instant_build"]:
			self.handlers[self.params.wall_bind.value[0]] = lambda p: self.instant_build(self.params.wall_alias.value, p)
			self.handlers[self.params.floor_bind.value[0]] = lambda p: self.instant_build(self.params.floor_alias.value, p)
			self.handlers[self.params.stair_bind.value[0]] = lambda p: self.instant_build(self.params.stair_alias.value, p)
			self.handlers[self.params.roof_bind.value[0]] = lambda p: self.instant_build(self.params.roof_alias.value, p)

		if input_params["single_reset"]:
			self.handlers[self.params.reset_bind.value[0]] = lambda p: self.reset_edit(p)

		if input_params["edit_mode"] == "hold":
			self.handlers[self.params.edit_bind.value[0]] = lambda p: self.hold_to_edit(p)

		elif input_params["edit_mode"] == "auto":
			self.handlers[self.params.edit_bind.value[0]] = lambda p: self.auto_edit_key(p)

		self.close_edit = lambda: self.tap_bind(self.params.edit_alias_2.value)
		def toggle_close():
			self.tap_bind(self.params.edit_alias_2.value)
			self.tap_bind(self.params.toggle_pick_bind.value)
		if input_params["toggle_pick"]:
			self.close_edit = toggle_close

		self.open_edit = lambda: self.tap_bind(self.params.edit_alias.value)
		def switch_pick_open():
			#print("OPENIN")
			#print(self.edit_open)
			self.tap_bind(self.params.pick_bind.value)
			self.tap_bind(self.params.edit_alias.value)

		if input_params["switch_pick"]:
			self.open_edit = switch_pick_open#lambda: (self.tap_bind(self.params.pick_bind.value), self.tap_bind(self.params.edit_alias.value))
		self.keylistener = keyboard.Listener(on_press = self.on_press, on_release = self.on_release)
		self.keylistener.start()
		if input_params["edit_mode"] == "auto":
			self.mouselistener = mouse.Listener(on_click = self.on_click_auto)
		else:
			self.mouselistener = mouse.Listener(on_click=self.on_click)
		#self.mouselistener.start()
		with self.mouselistener as listener:
			listener.join()

if __name__ == "__main__":
	import json, sys
	if len(sys.argv) > 1:
		cfg_path = sys.argv[1]
	else:
		cfg_path = "./config.json"
	with open(cfg_path, 'r') as cfg:
		config = json.load(cfg)
	hk = HKThread()
	hk.run(config)
	while 1:
		pass
	ret = sys.stdin.read(1)
	if ret == "q":
		hk.quit()
		#sys.exit(0)
	#sys.exit(1)


	
