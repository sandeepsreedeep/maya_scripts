"""
#----------------------------------------------------------------------
#    This file is part of "transfer Attribute"
#    and covered by a BSD-style license
#
#
#    Author:      P Sandeep
#    Contact:     sandeepsreedeep@gmail.com
#	 For more details check [LICENSE]
#----------------------------------------------------------------------
"""

import maya.cmds as cmds
import maya.OpenMayaUI as omui
import sys
import pymel.core as pm
from PySide.QtGui import QMainWindow
from PySide import QtCore
from ui._2016 import Ui_MainWindow
import shiboken


ver = cmds.about(version = True)

def get_main_window():
	ptr = omui.MQtUtil.mainWindow()
	return shiboken.wrapInstance(long(ptr), QMainWindow)

class AttributeTransfer(QMainWindow):
	def __init__(self, parent = get_main_window()):
		super(AttributeTransfer, self).__init__(parent = parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.ui.move_up_But.clicked.connect(self.move_Up)
		self.ui.move_Down_But.clicked.connect(self.move_Down)
		self.ui.delete_But.clicked.connect(self.del_Attr)
		self.ui.reload_But.clicked.connect(self.load_Object)
		self.ui.keyable_But.clicked.connect(self.toggle_Keyable)
		self.ui.lock_But.clicked.connect(self.toggle_Lock)
		self.ui.hide_But.clicked.connect(self.toggle_Hidden)
		self.ui.transfer_But.clicked.connect(self.transfer_Attr)
		self.ui.keyable_check_Box.stateChanged.connect(self.load_Object)
		self.ui.delete_Source_Check.stateChanged.connect(self.toggle_Trans)
		self.attr_List = None

	def toggle_Trans(self):
		if self.ui.delete_Source_Check.isChecked():
			self.ui.transfer_connections_Check.setChecked(True)
			self.ui.transfer_connections_Check.setEnabled(False)
		else:
			self.ui.transfer_connections_Check.setEnabled(True)


	def load_Object(self):
		self.ui.attr_listView.clear()
		sel_Obj = pm.ls(sl = True)[0]
		if sel_Obj:
			if self.ui.keyable_check_Box.isChecked():
				self.attr_List = pm.listAttr(sel_Obj, ud = True, k  = True)
			else:
				self.attr_List = pm.listAttr(sel_Obj, ud = True)
			self.ui.object_name.setText(sel_Obj.name())
			self.ui.attr_listView.addItems(self.attr_List)

	def move_Up(self):
		cur_item = self.ui.attr_listView.selectedItems()[0].text()
		cur_index = self.attr_List.index(cur_item)
		self.attr_List[cur_index] =  self.attr_List[cur_index - 1]
		self.attr_List[cur_index - 1] = cur_item
		self.ui.attr_listView.clear()
		for each in self.attr_List:
			lock = pm.getAttr(self.ui.object_name.text() +'.'+ each, l = True)
			pm.setAttr(self.ui.object_name.text() +'.'+ each, l = False)
			pm.deleteAttr(self.ui.object_name.text() +'.'+ each)
			pm.undo()
			pm.setAttr(self.ui.object_name.text() +'.'+ each, l = lock)

		self.ui.attr_listView.addItems(self.attr_List)
		self.ui.attr_listView.setCurrentRow( cur_index - 1 )


	def move_Down(self):
		cur_item = self.ui.attr_listView.selectedItems()[0].text()
		cur_index = self.attr_List.index(cur_item)
		self.attr_List[cur_index] =  self.attr_List[cur_index + 1]
		self.attr_List[cur_index + 1] = cur_item
		self.ui.attr_listView.clear()
		for each in self.attr_List:
			lock = pm.getAttr(self.ui.object_name.text() +'.'+ each, l = True)
			pm.setAttr(self.ui.object_name.text() +'.'+ each, l = False)
			pm.deleteAttr(self.ui.object_name.text() +'.'+ each)
			pm.undo()
			pm.setAttr(self.ui.object_name.text() +'.'+ each, l = lock)

		self.ui.attr_listView.addItems(self.attr_List)
		self.ui.attr_listView.setCurrentRow( cur_index + 1 )

	def del_Attr(self):
		cur_Items = self.ui.attr_listView.selectedItems()
		for each in cur_Items:
			cur_item = each.text()
			pm.setAttr(self.ui.object_name.text() +'.'+ cur_item, l = False)
			pm.deleteAttr(self.ui.object_name.text() +'.'+ cur_item)
		self.load_Object()

	def toggle_Keyable(self):
		cur_Items = self.ui.attr_listView.selectedItems()
		for each in cur_Items:
			cur_item = each.text()
			key = pm.getAttr(self.ui.object_name.text() +'.'+ cur_item, k = True)
			if key:
				pm.setAttr(self.ui.object_name.text() +'.'+ cur_item, k = False,cb = True)
			else:
				pm.setAttr(self.ui.object_name.text() +'.'+ cur_item, k = True)


	def toggle_Lock(self):
		cur_Items = self.ui.attr_listView.selectedItems()
		for each in cur_Items:
			cur_item = each.text()
			lock = pm.getAttr(self.ui.object_name.text() +'.'+ cur_item, l = True)
			if lock:
				pm.setAttr(self.ui.object_name.text() +'.'+ cur_item, l = False,cb = True)
				pm.setAttr(self.ui.object_name.text() +'.'+ cur_item, k = True)
			else:
				pm.setAttr(self.ui.object_name.text() +'.'+ cur_item, l = True,k = True)

	def toggle_Hidden(self):
		cur_Items = self.ui.attr_listView.selectedItems()
		for each in cur_Items:
			cur_item = each.text()
			visible = pm.getAttr(self.ui.object_name.text() +'.'+ cur_item, k = True)
			if visible:
				pm.setAttr(self.ui.object_name.text() +'.'+ cur_item,k = False)
				pm.setAttr(self.ui.object_name.text() +'.'+ cur_item,l = True)
				pm.setAttr(self.ui.object_name.text() +'.'+ cur_item, cb = False)
			else:
				pm.setAttr(self.ui.object_name.text() +'.'+ cur_item,cb = True)
				pm.setAttr(self.ui.object_name.text() +'.'+ cur_item,k = True)
				pm.setAttr(self.ui.object_name.text() +'.'+ cur_item,l = False)

	def transfer_Attr(self):
		cur_Items = self.ui.attr_listView.selectedItems()
		sel_Obj = self.ui.object_name.text()
		new_Obj = pm.selected()[0]
		for each in cur_Items:
			self.add_Attr(sel_Obj,each.text(),new_Obj)
			state = self.copy_Attr_State(sel_Obj, each.text())
			if self.ui.transfer_connections_Check.isChecked():
				self.connect_input(sel_Obj,each.text(),new_Obj)
				self.connect_output(sel_Obj,each.text(),new_Obj)
			self.set_Attr_State(each.text(), new_Obj,state)
			if self.ui.delete_Source_Check.isChecked():
				pm.setAttr(sel_Obj + '.' + each.text(), k = True, l = False, cb = True)
				pm.deleteAttr(sel_Obj + '.' + each.text())


	def add_Attr( self,sel_Obj, attribute,new_Obj):
		attributeType = pm.addAttr(sel_Obj + '.' +attribute, q = True, attributeType = True,)
		dataType = pm.addAttr(sel_Obj + '.' + attribute, q = True, dt = True,)
		niceName = pm.addAttr(sel_Obj + '.' + attribute, q = True, nn = True,)
		longName = pm.addAttr(sel_Obj + '.' + attribute, q = True, ln = True,) 
		if dataType == 'string':
			if niceName:
				pm.addAttr(new_Obj, ln = longName, nn = niceName,dt = dataType)

			else:
				pm.addAttr(new_Obj, ln = longName, dt = dataType)
		else:
			if attributeType == 'enum' :
				enumName = cmds.addAttr(sel_Obj + '.' + attribute, q = True,enumName = True,)
				if niceName:
					pm.addAttr(new_Obj, ln = longName, nn = niceName,at = attributeType,en = str(enumName))

				else:
					pm.addAttr(new_Obj, ln = longName, at = attributeType,en = str(enumName))
			elif attributeType == 'long' or attributeType == 'double':
				minValue = pm.addAttr(sel_Obj + '.' + attribute, q = True, min = True,)
				maxValue = pm.addAttr(sel_Obj + '.' + attribute, q = True, max = True,)
				defaultValue = pm.addAttr(sel_Obj + '.' + attribute, q = True, dv = True,)
				if niceName:
					pm.addAttr(new_Obj, ln = longName, nn = niceName,at = attributeType,dv = defaultValue)
					try:
						pm.addAttr(new_Obj + '.' + attribute,e = True, max = maxValue)
						pm.addAttr(new_Obj + '.' + attribute,e = True, min = minValue)
					except:
						pass
				else:
					pm.addAttr(new_Obj, ln = longName,at = attributeType,dv = defaultValue)
					try:
						pm.addAttr(new_Obj + '.' + attribute,e = True, max = maxValue)
						pm.addAttr(new_Obj + '.' + attribute,e = True, min = minValue)
					except:
						pass
			elif attributeType == 'bool':
				if niceName:
					pm.addAttr(new_Obj, ln = longName, nn = niceName,at = attributeType)
				else:
					pm.addAttr(new_Obj, ln = longName,at = attributeType)
			elif attributeType == 'double3':
				if niceName:
					pm.addAttr(new_Obj,ln = longName,nn = niceName,  at = "double3")
					pm.addAttr(new_Obj, ln = longName + ".X",at = 'double', p = 'zzz')
					pm.addAttr(new_Obj, ln = longName + ".Y",at = 'double', p = 'zzz')
					pm.addAttr(new_Obj, ln = longName + ".Z",at = 'double', p = 'zzz')

					val = pm.getAttr(sel_Obj + '.' + attribute)[0]
					pm.setAttr(new_Obj + '.' + attribute,*val,type = 'double3')
				else:
					pm.addAttr(new_Obj,ln = longName, at = "double3")
					pm.addAttr(new_Obj, ln = longName + ".X",at = 'double', p = 'zzz')
					pm.addAttr(new_Obj, ln = longName + ".Y",at = 'double', p = 'zzz')
					pm.addAttr(new_Obj, ln = longName + ".Z",at = 'double', p = 'zzz')

					val = pm.getAttr(sel_Obj + '.' + attribute)[0]
					pm.setAttr(new_Obj + '.' + attribute,*val,type = 'double3')
			pm.setAttr(new_Obj + '.' + attribute,e = True, cb = True)
			pm.setAttr(new_Obj + '.' + attribute,e = True,k = True, lock = False)

	def copy_Attr_State(self,sel_Obj,attribute):
		lock = pm.getAttr(sel_Obj + '.' + attribute, lock = True,)
		keyable = pm.getAttr(sel_Obj + '.' + attribute, keyable = True,)
		hidden = pm.getAttr(sel_Obj + '.' + attribute, cb = True,)
		return [lock,keyable,hidden]

	def set_Attr_State( self,attribute,new_Obj,state):
		pm.setAttr(new_Obj + '.' + attribute,e = True, k = state[1])
		pm.setAttr(new_Obj + '.' + attribute,e = True, lock = state[0])
		if not state[1]:
			pm.setAttr(new_Obj + '.' + attribute,e = True, cb = state[2])

	def connect_input( self,sel_Obj, attribute,new_Obj):
		for each in list(pm.listConnections(sel_Obj+'.'+attribute, p = True, s = True, d = False)):
			pm.connectAttr(each, new_Obj+'.'+attribute, force = True)

	def connect_output( self,sel_Obj, attribute,new_Obj):
		for each in list(pm.listConnections(sel_Obj+'.'+attribute, p = True, d = True, s = False)):
			Obj, attr = each.split('.')
			state = self.copy_Attr_State(Obj, attr)
			pm.setAttr(each, k = True, l = False, cb = True)
			pm.connectAttr(new_Obj+'.'+attribute, each,force = True)
			self.set_Attr_State(attr, Obj, state)




def UI():
	global ui
	try:
		ui.close()
	except:
		pass
	ui = AttributeTransfer()
	if pm.selected():
		ui.load_Object()
	ui.show()

