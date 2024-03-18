#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Please don't remove this disclaimer
# Code by Madhouse
_I='dateDow'
_H='namesat'
_G='/etc/enigma2'
_F='text'
_E='---'
_D='/usr/lib/enigma2/python/Plugins/Extensions/GioppyGio/Moduli/Settings/Select'
_C=True
_B='1'
_A='B'
from.import _
from Components.Label import Label
from Components.ConfigList import ConfigListScreen,ConfigList
from Components.ActionMap import ActionMap
from Components.MenuList import MenuList
from Components.Pixmap import Pixmap
from Plugins.Plugin import PluginDescriptor
from Tools.LoadPixmap import LoadPixmap
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.MultiContent import MultiContentEntryText,MultiContentEntryPixmapAlphaTest
import sys,os,glob,shutil
from.Config import*
from enigma import getDesktop,eListboxPythonMultiContent,gFont,RT_HALIGN_LEFT,RT_HALIGN_RIGHT,RT_VALIGN_CENTER,RT_HALIGN_CENTER,eDVBDB
if getDesktop(0).size().width()==1920:skins='/usr/lib/enigma2/python/Plugins/Extensions/GioppyGio/Skin/fhd/';giopath='/usr/lib/enigma2/python/Plugins/Extensions/GioppyGio/Panel/'
else:skins='/usr/lib/enigma2/python/Plugins/Extensions/GioppyGio/Skin/hd/';giopath='/usr/lib/enigma2/python/Plugins/Extensions/GioppyGio/Panel/default/'
class MenuListSelect(MenuList):
	def __init__(self,list,enableWrapAround=_C):
		A='gioppyregular';MenuList.__init__(self,list,enableWrapAround,eListboxPythonMultiContent);screenwidth=getDesktop(0).size().width()
		if screenwidth and screenwidth==1920:self.l.setFont(0,gFont(A,32));self.l.setFont(1,gFont(A,24));self.l.setItemHeight(80)
		else:self.l.setFont(0,gFont(A,20));self.l.setFont(1,gFont(A,14));self.l.setItemHeight(50)
class ListSelect:
	def __init__(self):0
	def readSaveList(self):
		try:
			jw=open(_D);jjw=jw.readlines();jw.close();list=[]
			for x in jjw:
				try:jx=x.split(_E);list.append((jx[0],jx[1].strip()))
				except:pass
			return list
		except:pass
	def SaveList(self,list):
		jw=open(_D,'w')
		for(dir,name,value)in list:
			if value==_B:jw.write(dir+_E+name+'\n')
		jw.close()
	def readBouquetsList(self,pwd,bouquetname):
		try:f=open(pwd+'/'+bouquetname)
		except Exception as e:print(e);return
		ret=[]
		while _C:
			line=f.readline()
			if line=='':break
			if line[:8]!='#SERVICE':continue
			tmp=line.strip().split(':');line=tmp[len(tmp)-1];filename=None
			if line[:12]=='FROM BOUQUET':tmp=line[13:].split(' ');filename=tmp[0].strip('"')
			else:filename=line
			if filename:
				try:fb=open(pwd+'/'+filename)
				except Exception as e:continue
				tmp=fb.readline().strip()
				if tmp[:6]=='#NAME ':ret.append([filename,tmp[6:]])
				else:ret.append([filename,filename])
				fb.close()
		return ret
	def readBouquetsTvList(self,pwd):return self.readBouquetsList(pwd,'bouquets.tv')
	def TvList(self):
		jload=self.readSaveList();self.bouquetlist=[]
		for x in self.readBouquetsTvList(_G):
			value='0'
			try:
				for(j,jx)in jload:
					if j==x[0]and jx.find(x[1])!=-1:value=_B;break
			except:pass
			self.bouquetlist.append((x[0],x[1],value))
		return self.bouquetlist
class MenuSelect(Screen,ConfigListScreen):
	def __init__(self,session):
		self.session=session
		if getDesktop(0).size().width()==1920:skin=skins+'MenuSelectfhd.xml'
		else:skin=skins+'MenuSelecthd.xml'
		f=open(skin,'r');self.skin=f.read();f.close();Screen.__init__(self,session);self.ListSelect=ListSelect();self['autotimer']=Label('');self[_H]=Label('');self[_F]=Label('');self[_I]=Label('');self['Key_Red']=Label(_('Exit'));self['Key_Green']=Label(_('Customize'));self['Key_Personal']=Label('');self['version']=Label(_('Settings & Picons V.%s by GioppyGio')%version);self['A']=MenuListSelect([]);self[_A]=MenuListSelect([]);self[_A].selectionEnabled(1);self.Info();self.Menu();self.MenuA();self['actions']=ActionMap(['OkCancelActions','ShortcutActions','WizardActions','ColorActions','SetupActions','NumberActions','MenuActions','HelpActions','EPGSelectActions'],{'ok':self.OkSelect,'up':self.keyUp,'down':self.keyDown,'green':self.Uscita,'cancel':self.close_screen,'nextBouquet':self[_A].pageUp,'prevBouquet':self[_A].pageDown,'red':self.close_screen},-1)
	def close_screen(self):self.close()
	def Info(self):
		Type,AutoTimer,Personal,NumberSat,NameSat,Date,NumberDtt,DowDate,NameInfo=Load()
		if str(Date)=='0':newdate=''
		else:newdate=' - '+ConverDate(Date)
		if str(DowDate)=='0':newDowDate=_('Last Update: Never')
		else:newDowDate=_('Last Update: ')+DowDate
		self[_H].setText(NameInfo+newdate);self[_I].setText(newDowDate)
	def Uscita(self):
		if os.stat(_D).st_size==0:self.session.open(MessageBox,_('You have not selected any bouquet!'),MessageBox.TYPE_INFO)
		else:self.session.openWithCallback(self.personalizebouquet,MessageBox,_('Do you want to customize the bouquets?'),MessageBox.TYPE_YESNO)
	def personalizebouquet(self,result):
		C='/etc/enigma2/bouquets.tv';B='/etc/enigma2/';A='/etc/enigma2/SelectFolder'
		if result is _C:
			try:
				jw=open(_D);jjw=jw.readlines();jw.close()
				for x in jjw:
					try:jx=x.split(_E);newfile=jx[0];os.system('mkdir /etc/enigma2/SelectFolder');os.system('cp /etc/enigma2/'+newfile+' '+A)
					except:pass
				for filename in glob.glob(os.path.join(B,'*.bouquetmakerxtream*.tv')):shutil.copy(filename,A)
				for filename in glob.glob(os.path.join(B,'*.jmx*.tv')):shutil.copy(filename,A)
				for filename in glob.glob(os.path.join(B,'*.jedimakerxtream*.tv')):shutil.copy(filename,A)
				for filename in glob.glob(os.path.join(B,'*.iptvdiv.tv')):shutil.copy(filename,A)
				os.system('rm -r /etc/enigma2/*.tv');Writebouquets=open(C,'w');Writebouquets.write('#NAME User - bouquets (Tv)\n');Writebouquets.close()
				for x in jjw:
					try:
						jx=x.split(_E)
						with open(C,'a')as f:f.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "'+jx[0].strip()+'" ORDER BY bouquet\n')
					except:pass
				os.system('cp /etc/enigma2/SelectFolder/* '+_G);eDVBDB.getInstance().reloadServicelist();eDVBDB.getInstance().reloadBouquets();os.system('rm -rf /etc/enigma2/*.del');os.system('rm -rf /etc/enigma2/SelectFolder');MyMessage=_('Personalized bouquets successfully');self.session.open(MessageBox,MyMessage,MessageBox.TYPE_INFO,timeout=5);self.close()
			except:pass
		else:self.close()
	def keyUp(self):self[_A].up()
	def keyDown(self):self[_A].down()
	def hauptListEntry(self,dir,name,value):
		res=[(dir,name,value)]
		if getDesktop(0).size().width()==1920:
			icon='/usr/lib/enigma2/python/Plugins/Extensions/GioppyGio/Panel/gg_on.png'
			if value==_B:icon='/usr/lib/enigma2/python/Plugins/Extensions/GioppyGio/Panel/gg_off.png'
		else:
			icon='/usr/lib/enigma2/python/Plugins/Extensions/GioppyGio/Panel/gg_onhd.png'
			if value==_B:icon='/usr/lib/enigma2/python/Plugins/Extensions/GioppyGio/Panel/gg_offhd.png'
		try:name=name.split('   ')[0]
		except:pass
		if getDesktop(0).size().width()==1920:res.append(MultiContentEntryText(pos=(73,8),size=(625,45),font=0,text=name,flags=RT_HALIGN_LEFT));res.append(MultiContentEntryPixmapAlphaTest(pos=(20,13),size=(30,30),png=LoadPixmap(cached=_C,desktop=getDesktop(0),path=icon)))
		else:res.append(MultiContentEntryText(pos=(43,3),size=(625,45),font=0,text=name,flags=RT_HALIGN_LEFT));res.append(MultiContentEntryPixmapAlphaTest(pos=(8,5),size=(30,30),png=LoadPixmap(cached=_C,desktop=getDesktop(0),path=icon)))
		res.append(MultiContentEntryText(pos=(0,0),size=(0,0),font=0,text=dir,flags=RT_HALIGN_LEFT));res.append(MultiContentEntryText(pos=(0,0),size=(0,0),font=0,text=value,flags=RT_HALIGN_LEFT));return res
	def hauptListEntryA(self,name):
		res=[name]
		try:name=name.split('   ')[0]
		except:pass
		if getDesktop(0).size().width()==1920:res.append(MultiContentEntryText(pos=(20,4),size=(339,36),font=0,text=name,flags=RT_HALIGN_LEFT))
		else:res.append(MultiContentEntryText(pos=(10,0),size=(233,26),font=0,text=name,flags=RT_HALIGN_LEFT))
		return res
	def MenuA(self):
		self.jB=[];lista=self.ListSelect.readSaveList()
		if lista:
			for(dir,name)in lista:self.jB.append(self.hauptListEntryA(name))
		self['A'].setList(self.jB)
		if not self.jB:self[_F].setText(_('Please select\nwhat you want\nto keep!'))
		else:self[_F].setText(' ')
		self[_A].selectionEnabled(1);self['A'].selectionEnabled(0)
	def Menu(self):
		self.jA=[]
		for(dir,name,value)in self.ListSelect.TvList():
			if name!='Digitale Terrestre'and name!='Favourites (TV)':self.jA.append(self.hauptListEntry(dir,name,value))
		self[_A].setList(self.jA)
	def OkSelect(self):
		NewName=self[_A].getCurrent()[0][1];NewDir=self[_A].getCurrent()[0][0];self.list=[]
		for(dir,name,value)in self.ListSelect.TvList():
			if dir==NewDir and name==NewName:
				if value=='0':self.list.append((dir,name,_B))
			elif value==_B:self.list.append((dir,name,_B))
		self.ListSelect.SaveList(self.list);self.Menu();self.MenuA()
