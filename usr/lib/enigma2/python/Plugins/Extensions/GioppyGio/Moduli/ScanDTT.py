#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Please don't remove this disclaimer
# Code by Madhouse
from __future__ import print_function,division
_K='FrontendInfo'
_J='transponder'
_I='network'
_H='scan_state'
_G='Service'
_F='ScanDTThd.xml'
_E='ScanDTTfhd.xml'
_D='scan'
_C='scan_progress'
_B='servicelist'
_A=True
from.import _
import Screens.InfoBar
from enigma import eServiceReference,eTimer,getDesktop
from Screens.Screen import Screen
from Components.ServiceScan import ServiceScan as CScan
from Components.ProgressBar import ProgressBar
from Components.Label import Label
from Components.ActionMap import ActionMap
from Screens.Standby import TryQuitMainloop
from Screens.MessageBox import MessageBox
from Components.MenuList import MenuList
from Screens.Console import Console
from Components.Sources.FrontendInfo import FrontendInfo
from Components.config import config
from.Setting import install_epg
import os,glob
from.Config import version
if getDesktop(0).size().width()==1920:skins='/usr/lib/enigma2/python/Plugins/Extensions/GioppyGio/Skin/fhd/'
else:skins='/usr/lib/enigma2/python/Plugins/Extensions/GioppyGio/Skin/hd/'
class FIFOList(MenuList):
	def __init__(A,len=10):A.len=len;A.list=[];MenuList.__init__(A,A.list)
	def addItem(A,item):A.list.append(item);A.l.setList(A.list[-A.len:])
	def clear(A):del A.list[:];A.l.setList(A.list)
	def getCurrentSelection(A):return A.list and A.getCurrent()or None
	def listAll(A):A.l.setList(A.list);A.selectionEnabled(_A)
class ServiceScanDTT(Screen):
	def __init__(A,session,showStepSlider=_A):
		if getDesktop(0).size().width()==1920:B=skins+_E
		else:B=skins+_F
		C=open(B,'r');A.skin=C.read();C.close();Screen.__init__(A,session);A.setup_title=_('GioppyGio - ScanDTT');Screen.setTitle(A,A.setup_title);A[_G]=Label(_('No service'));A[_C]=ProgressBar()
	def updateProgress(A,value):A[_C].setValue(value)
	def updateService(A,name):A[_G].setText(name)
class Scandtt(Screen):
	def up(A):
		A[_B].up();B=A[_B].getCurrentSelection()
		if B:A.session.summary.updateService(B[0])
	def down(A):
		A[_B].down();B=A[_B].getCurrentSelection()
		if B:A.session.summary.updateService(B[0])
	def cancel(A):A.close()
	def doCloseRecursive(A):A.close()
	def ok(A):
		if A[_D].isDone():A.session.openWithCallback(A.downloadepg,MessageBox,_('DTTerrestrial LCN bouquet successfully created.\n\nDo you want to download the Epg?\nThe download takes place in the background.'),MessageBox.TYPE_YESNO,default=_A,timeout=15)
	def downloadepg(A,answer):
		if answer is _A:
			if os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/EPGImport/plugin.pyo')or os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/EPGImport/plugin.py')or os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/EPGImport/plugin.pyc'):
				if not os.path.exists('/etc/enigma2/epgimport.conf'):os.system('cp /usr/lib/enigma2/python/Plugins/Extensions/GioppyGio/Panel/epgimport.conf /etc/enigma2/')
				from Plugins.Extensions.EPGImport.plugin import AutoStartTimer,autoStartTimer as B,channelFilter,config,epgimport as C
				if B is not None and not C.isImportRunning():B.runImport();A.close()
			else:A.session.openWithCallback(A.installepg,MessageBox,_('Epg Importer not found! Do you want to install it?'),MessageBox.TYPE_YESNO,default=_A,timeout=15)
		else:A.close()
	def installepg(A,answer):
		if answer is _A:A.session.openWithCallback(A.instepg,Console,_('Install Epg Import'),[install_epg],closeOnSuccess=_A)
		else:A.close()
	def instepg(A,string=''):B=_('Do you want to restart the GUI\nto apply the changes?');A.session.openWithCallback(A.downloadepginst,MessageBox,B,MessageBox.TYPE_YESNO,default=_A,timeout=15)
	def downloadepginst(A,answer):
		if answer is _A:A.session.open(TryQuitMainloop,3)
		else:A.close()
	def __init__(A,session,scanList):
		B=session
		if getDesktop(0).size().width()==1920:C=skins+_E
		else:C=skins+_F
		D=open(C,'r');A.skin=D.read();D.close();Screen.__init__(A,B);A['Title']=Label(_('Scanning...'));A.scanList=scanList
		if hasattr(B,'infobar'):
			A.currentInfobar=Screens.InfoBar.InfoBar.instance
			if A.currentInfobar:
				A.currentServiceList=A.currentInfobar.servicelist
				if A.session.pipshown and A.currentServiceList:
					if A.currentServiceList.dopipzap:A.currentServiceList.togglePipzap()
					if hasattr(A.session,'pip'):del A.session.pip
					A.session.pipshown=False
		else:A.currentInfobar=None
		A.session.nav.stopService();A[_C]=ProgressBar();A[_H]=Label(_('scan state'));A[_I]=Label();A[_J]=Label();A['version']=Label(_('Settings & Picons V.%s by GioppyGio')%version);A['pass']=Label('');A[_B]=FIFOList(len=10);A[_K]=FrontendInfo();A['key_red']=Label(_('Cancel'));A['key_green']=Label(_('OK'));A['actions']=ActionMap(['SetupActions','MenuActions','ColorActions'],{'up':A.up,'down':A.down,'ok':A.ok,'save':A.ok,'green':A.ok,'cancel':A.cancel,'menu':A.doCloseRecursive},-2);A.setTitle(_('GioppyGio - Service scan'));A.onFirstExecBegin.append(A.doServiceScan);A.scanTimer=eTimer();A.scanTimer.callback.append(A.scanPoll)
	def scanPoll(A):
		if A[_D].isDone():A.scanTimer.stop()
	def doServiceScan(A):A[_B].len=A[_B].instance.size().height()//A[_B].l.getItemSize().height();A[_D]=CScan(A[_C],A[_H],A[_B],A['pass'],A.scanList,A[_I],A[_J],A[_K],A.session.summary);A.scanTimer.start(250)
	def createSummary(A):return ServiceScanDTT
