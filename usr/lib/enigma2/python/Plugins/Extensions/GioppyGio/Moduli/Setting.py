#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Please don't remove this disclaimer
# Code by Madhouse
_M='services'
_L='transponders'
_K='rm -rf /etc/enigma2/*.del'
_J='rm -fr '
_I='/Settings/Temp/TrasponderListOldLamedb'
_H='/Settings/Temp/TerrestrialChannelListArchive'
_G='/Settings/Temp/ServiceListOldLamedb'
_F='/etc/enigma2/'
_E=':'
_D='w'
_C='r'
_B=True
_A=False
install_epg='cd /usr/lib/enigma2/python/Plugins/Extensions/GioppyGio/Panel && chmod 777 installepg.sh && ./installepg.sh'
from.import _
from enigma import eTimer,eDVBDB
from random import choice
import re,glob,shutil,os,ssl,time,sys,zipfile
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.Console import Console
from Screens.Standby import TryQuitMainloop
from.Config import*
import socket
try:from urllib.request import urlopen,Request;from urllib.error import HTTPError,URLError
except ImportError:from urllib2 import urlopen,Request,HTTPError,URLError
Directory=os.path.dirname(sys.modules[__name__].__file__)
MinStart=int(choice(range(59)))
def TimerControl():now=time.localtime(time.time());Ora=str(now[3]).zfill(2)+_E+str(now[4]).zfill(2)+_E+str(now[5]).zfill(2);Date=str(now[2]).zfill(2)+'-'+str(now[1]).zfill(2)+'-'+str(now[0]);return'%s ora: %s'%(Date,Ora)
def StartSavingTerrestrialChannels(lamedb,type):
	B='/etc/enigma2/*.tv';A='eeee0000'
	def ForceSearchBouquetTerrestrial():
		for file in sorted(glob.glob(B)):
			f=open(file,_C).read();x=f.strip().lower()
			if x.find(A)!=-1:
				if x.find('82000')==-1 and x.find('c0000')==-1:return file;break
	def ResearchBouquetTerrestrial(search,search1):
		for file in sorted(glob.glob(B)):
			f=open(file,_C).read();x=f.strip().lower();x1=f.strip()
			if x1.find('#NAME')!=-1:
				if x.lower().find(search.lower())!=-1 or x.lower().find(search1.lower())!=-1:
					if x.find(A)!=-1:return file;break
	def SaveTrasponderService(lamedb):
		TrasponderListOldLamedb=open(Directory+_I,_D);ServiceListOldLamedb=open(Directory+_G,_D);Trasponder=_A;inTransponder=_A;inService=_A
		try:
			LamedbFile=open(lamedb,_C)
			while 1:
				line=LamedbFile.readline()
				if not line:break
				if not(inTransponder or inService):
					if line.find(_L)==0:inTransponder=_B
					if line.find(_M)==0:inService=_B
				if line.find('end')==0:inTransponder=_A;inService=_A
				line=line.lower()
				if line.find(A)!=-1:
					Trasponder=_B
					if inTransponder:TrasponderListOldLamedb.write(line);line=LamedbFile.readline();TrasponderListOldLamedb.write(line);line=LamedbFile.readline();TrasponderListOldLamedb.write(line)
					if inService:tmp=line.split(_E);ServiceListOldLamedb.write(tmp[0]+_E+tmp[1]+_E+tmp[2]+_E+tmp[3]+_E+tmp[4]+':0\n');line=LamedbFile.readline();ServiceListOldLamedb.write(line);line=LamedbFile.readline();ServiceListOldLamedb.write(line)
			TrasponderListOldLamedb.close();ServiceListOldLamedb.close()
			if not Trasponder:os.system(_J+Directory+_I);os.system(_J+Directory+_G)
		except:pass
		return Trasponder
	def CreateBouquetForce():
		WritingBouquetTemporary=open(Directory+_H,_D);WritingBouquetTemporary.write('#NAME terrestre\n');ReadingTempServicelist=open(Directory+_G).readlines()
		for jx in ReadingTempServicelist:
			if jx.find('eeee')!=-1:String=jx.split(_E);WritingBouquetTemporary.write('#SERVICE 1:0:%s:%s:%s:%s:%s:0:0:0:\n'%(hex(int(String[4]))[2:],String[0],String[2],String[3],String[1]))
		WritingBouquetTemporary.close()
	def SaveBouquetTerrestrial(istype):
		if istype:
			try:shutil.copyfile(Directory+'/Settings/Temp/enigma2dtt/dtt.tv',Directory+_H);return _B
			except:pass
		NameDirectory=ResearchBouquetTerrestrial('terr','dtt')
		if not NameDirectory:NameDirectory=ForceSearchBouquetTerrestrial()
		try:shutil.copyfile(NameDirectory,Directory+_H);return _B
		except:pass
	Service=SaveTrasponderService(lamedb)
	if Service:
		if not SaveBouquetTerrestrial(type):CreateBouquetForce()
		return _B
def TransferBouquetTerrestrialFinal():
	def RestoreTerrestrial():
		for file in os.listdir(_F):
			if re.search('^userbouquet.*.tv',file):
				f=open(_F+file,_C);x=f.read()
				if re.search('#NAME —  Digitale Terrestre Italia',x,flags=re.IGNORECASE):return _F+file
	try:
		TerrestrialChannelListArchive=open(Directory+_H,_C).readlines();DirectoryUserBouquetTerrestrial=RestoreTerrestrial()
		if DirectoryUserBouquetTerrestrial:
			TrasfBouq=open(DirectoryUserBouquetTerrestrial,_D)
			for Line in TerrestrialChannelListArchive:
				if Line.lower().find('#name')!=-1:TrasfBouq.write('#NAME —  Digitale Terrestre Italia\n')
				else:TrasfBouq.write(Line)
			TrasfBouq.close();return _B
	except:return _A
def StartProcess(jLinkSat,jLinkDtt,Type,Personal):
	U='/Settings/Temp/*';T='/Settings/Temp/enigma2/lamedb /etc/enigma2';S='/Settings/enigma2/* /etc/enigma2';R='#NAME User - bouquets (Tv)\n';Q='/usr/lib/enigma2/python/Plugins/Extensions/GioppyGio/Moduli/Settings/SelectBack';P='/Settings/Temp/enigma2dtt/lamedb';O='userbouquet.favourites_gio.tv';N='userbouquet.favourites.tv';M='/Settings/Temp/enigma2/lamedb2/lamedb';L='/Settings/enigma2';K='a';J='/usr/lib/enigma2/python/Plugins/Extensions/GioppyGio/Moduli/Settings/Select';I='/Settings/Temp/enigma2/lamedb';H='rm -rf ';G='cp ';F='---';E='/etc/enigma2/lamedb';D='/etc/enigma2/bouquets.tv';C='mkdir ';B='/Settings/SelectFolder';A='cp -rf '
	def LamedbRestore():
		C='end\n';B='/Settings/Temp/ServiceListNewLamedb';A='/Settings/Temp/TrasponderListNewLamedb'
		try:
			TrasponderListNewLamedb=open(Directory+A,_D);ServiceListNewLamedb=open(Directory+B,_D);inTransponder=_A;inService=_A;infile=open(E,_C)
			while 1:
				line=infile.readline()
				if not line:break
				if not(inTransponder or inService):
					if line.find(_L)==0:inTransponder=_B
					if line.find(_M)==0:inService=_B
				if line.find('end')==0:inTransponder=_A;inService=_A
				if inTransponder:TrasponderListNewLamedb.write(line)
				if inService:ServiceListNewLamedb.write(line)
			TrasponderListNewLamedb.close();ServiceListNewLamedb.close();WritingLamedbFinal=open(E,_D);WritingLamedbFinal.write('eDVB services /4/\n');TrasponderListNewLamedb=open(Directory+A,_C).readlines()
			for x in TrasponderListNewLamedb:WritingLamedbFinal.write(x)
			try:
				TrasponderListOldLamedb=open(Directory+_I,_C).readlines()
				for x in TrasponderListOldLamedb:WritingLamedbFinal.write(x)
			except:pass
			WritingLamedbFinal.write(C);ServiceListNewLamedb=open(Directory+B,_C).readlines()
			for x in ServiceListNewLamedb:WritingLamedbFinal.write(x)
			try:
				ServiceListOldLamedb=open(Directory+_G,_C).readlines()
				for x in ServiceListOldLamedb:WritingLamedbFinal.write(x)
			except:pass
			WritingLamedbFinal.write(C);WritingLamedbFinal.close();return _B
		except:return _A
	def DownloadSettingAggDtt(jLinkDtt):
		F='/Settings/Temp/enigma2dtt';E='/Settings/Temp/settingdtt/userbouquet.favourites.tv';D='/Settings/Temp/settingdtt';B='/Settings/Temp/settingdtt/bouquets.tv';A='/Settings/Temp/listaE2dtt.zip'
		try:
			import requests;url_zip=requests.get(jLinkDtt,verify=_A)
			with open(Directory+A,'wb')as f:f.write(url_zip.content)
			if os.path.exists(Directory+A):
				os.system(C+Directory+D);image_zip=zipfile.ZipFile(Directory+A);image_zip.extractall(Directory+D)
				if os.path.exists(Directory+E):old_favorites=Directory+E;new_favorites=Directory+'/Settings/Temp/settingdtt/userbouquet.favourites_gio.tv';os.rename(old_favorites,new_favorites)
				if os.path.exists(Directory+B):f=open(Directory+B,_C);filedata=f.read();f.close();newdata=filedata.replace(N,O);f=open(Directory+B,_D);f.write(newdata);f.close()
				os.system(C+Directory+F);dir_name=Directory+'/Settings/Temp/settingdtt/';destination=Directory+F
				for filename in glob.glob(os.path.join(dir_name,'*')):shutil.copy(filename,destination)
				if os.path.exists(Directory+P):return _B
			return _A
		except:return
	def DownloadSettingAgg(jLinkSat,jLinkDtt):
		E='/Settings/Temp/setting/userbouquet.favourites.tv';D='/Settings/Temp/setting/bouquets.tv';B='/Settings/Temp/setting';A='/Settings/Temp/listaE2.zip';conferma=_B
		if jLinkDtt and str(jLinkDtt)!='0':
			if DownloadSettingAggDtt(jLinkDtt):conferma=_B
			else:conferma=_A
		try:
			import requests;url_zip=requests.get(jLinkSat,verify=_A)
			with open(Directory+A,'wb')as f:f.write(url_zip.content)
			if os.path.exists(Directory+A):
				os.system(C+Directory+B);image_zip=zipfile.ZipFile(Directory+A);image_zip.extractall(Directory+B)
				if os.path.exists(Directory+E):old_favorites=Directory+E;new_favorites=Directory+'/Settings/Temp/setting/userbouquet.favourites_gio.tv';os.rename(old_favorites,new_favorites)
				if os.path.exists(Directory+D):f=open(Directory+D,_C);filedata=f.read();f.close();newdata=filedata.replace(N,O);f=open(Directory+D,_D);f.write(newdata);f.close()
				os.system(C+Directory+'/Settings/Temp/enigma2');dir_name=Directory+B;destination=Directory+'/Settings/Temp/enigma2/'
				for filename in glob.glob(os.path.join(dir_name,'*')):shutil.copy(filename,destination)
				if os.path.exists(Directory+I)and conferma:return _B
			return _A
		except:return
	def SaveList(list):
		jw=open(Q,_D)
		for(dir,name)in list:jw.write(dir+F+name)
		jw.close()
	def SavePersonalSetting():
		try:
			os.system(C+Directory+B);jw=open(J,_C);jjw=jw.readlines();jw.close();list=[]
			for x in jjw:
				try:jx=x.split(F);newfile=jx[0];os.system('cp /etc/enigma2/'+newfile+' '+Directory+B);os.system(G+Directory+'/Settings/Temp/enigma2/*'+' '+Directory+B);list.append((newfile,jx[1]))
				except:pass
			for filename in glob.glob(os.path.join(_F,'*.bouquetmakerxtream*.tv')):shutil.copy(filename,Directory+B)
			for filename in glob.glob(os.path.join(_F,'*.jmx*.tv')):shutil.copy(filename,Directory+B)
			for filename in glob.glob(os.path.join(_F,'*.jedimakerxtream*.tv')):shutil.copy(filename,Directory+B)
			for filename in glob.glob(os.path.join(_F,'*.iptvdiv.tv')):shutil.copy(filename,Directory+B)
			if os.path.exists('userbouquet.TerrestrialScan.tv'):os.system('cp /etc/enigma2/userbouquet.TerrestrialScan.tv'+' '+Directory+B)
			SaveList(list)
		except:return
		return _B
	def TransferPersonalSetting():
		try:
			jw=open(Q,_C);jjw=jw.readlines();jw.close()
			for x in jjw:
				try:jx=x.split(F);newfile=jx[0];os.system(G+Directory+'/Settings/SelectFolder/*.tv'+' /etc/enigma2')
				except:pass
		except:pass
		return _B
	def CreateUserbouquetPersonalSetting():
		B='" ORDER BY bouquet\n';A='#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "'
		try:jw=open(J,_C);jjw=jw.readlines();jw.close()
		except:pass
		jRewriteBouquet=open(D,_C);RewriteBouquet=jRewriteBouquet.readlines();jRewriteBouquet.close();WriteBouquet=open(D,_D)
		if int(Personal)==1:
			Writebouquets=open(D,_D);Writebouquets.write(R);Writebouquets.close()
			for x in jjw:
				try:
					jx=x.split(F)
					with open(D,K)as f:f.write(A+jx[0].strip()+B)
				except:pass
			with open(D,K)as f:f.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.favourites.tv" ORDER BY bouquet\n')
		else:
			Counter=0
			for xx in RewriteBouquet:
				if Counter==1:
					for x in jjw:
						if x[0].strip()!='':
							try:jx=x.split(F);WriteBouquet.write(A+jx[0].strip()+B)
							except:pass
					WriteBouquet.write(xx)
				else:WriteBouquet.write(xx)
				Counter=Counter+1
		WriteBouquet.close()
	def TransferNewSetting():
		K='/Settings/Temp/enigma2/satellites.xml /etc/tuxbox/';J='/Settings/Temp/enigma2/whitelist /etc/enigma2/';I='/etc/enigma2/whitelist';H='/Settings/Temp/enigma2/blacklist /etc/enigma2/';G='/etc/enigma2/blacklist';F='/Settings/Temp/enigma2/*.radio /etc/enigma2/';E='/etc/enigma2/userbouquet.favourites.tv';C='rm -rf /etc/enigma2/*.tv';B='rm -rf /etc/enigma2/*.radio'
		try:
			if int(Personal)==1:
				os.system(B);os.system(_K);os.system(C);WriteBouquet=open(D,_D);WriteBouquet.write(R);WriteBouquet.close()
				if not os.path.exists(E):WriteFavorites=open(E,_D);WriteFavorites.write('#NAME @GioppyGio Favorites\n');WriteFavorites.close()
				os.system(A+Directory+F)
				if not os.path.exists(G):os.system(A+Directory+H)
				if not os.path.exists(I):os.system(A+Directory+J)
				os.system(A+Directory+K)
			else:
				os.system('rm -rf /etc/enigma2/lamedb');os.system(B);os.system(C);os.system(_K);os.system(A+Directory+'/Settings/Temp/enigma2/*.tv /etc/enigma2/');os.system(A+Directory+F);os.system(A+Directory+'/Settings/Temp/enigma2/lamedb /etc/enigma2/')
				if not os.path.exists(G):os.system(A+Directory+H)
				if not os.path.exists(I):os.system(A+Directory+J)
				os.system(A+Directory+K)
		except:return
		return _B
	Status=_B
	if int(Type)==1:SavingProcessTerrestrialChannels=StartSavingTerrestrialChannels(E,_A);os.system('cp -r /etc/enigma2/ '+Directory+L)
	if not DownloadSettingAgg(jLinkSat,jLinkDtt):os.system(G+Directory+S);os.system(H+Directory+L);Status=_A
	else:
		if int(Type)==0:SavingProcessTerrestrialChannels=StartSavingTerrestrialChannels(Directory+P,_B)
		personalsetting=_A
		if int(Personal)==1:personalsetting=SavePersonalSetting()
		if TransferNewSetting():
			if personalsetting:
				if TransferPersonalSetting():
					CreateUserbouquetPersonalSetting()
					with open(J,_C)as f:
						if'userbouquet.TerrestrialScan.tv---—'in f.read():
							os.system(C+Directory+'/Settings/Temp/enigma2/lamedb2');file_diff=open(Directory+M,_D);oldlines=set(open(Directory+I,_C))
							for line in open(E,_C):
								if line not in oldlines:file_diff.write(line)
							FileNews=open(Directory+I,K);FileNewsDb=open(Directory+M,_C);FileNewsDb2=FileNewsDb.read();FileNewsDb.close();f1=open(E,_C);f2=open(Directory+M,_C);f1_data=f1.readlines();f2_data=f2.readlines();CheckFiles=_A
							for line1 in f1_data:
								for line2 in f2_data:
									if line2 in line1:CheckFiles=_B
							if CheckFiles==_A:FileNews.write(FileNewsDb2);FileNews.close();os.system(A+Directory+T)
						else:os.system(A+Directory+T)
					os.system(_J+Directory+B);os.system('mv /usr/lib/enigma2/python/Plugins/Extensions/GioppyGio/Moduli/Settings/SelectBack /usr/lib/enigma2/python/Plugins/Extensions/GioppyGio/Moduli/Settings/Select');os.system(H+Directory+L)
		else:os.system(G+Directory+S);os.system(H+Directory+U);Status=_A
		if SavingProcessTerrestrialChannels and Status:TransferBouquetTerrestrialFinal()
	os.system(H+Directory+U);return Status
class GioppyGioSettings:
	def __init__(self,session=None):self.session=session;self.iTimer1=eTimer();self.iTimer2=eTimer();self.iTimer3=eTimer();self.iTimer1.callback.append(self.startTimerSetting);self.iTimer2.callback.append(self.startTimerSetting);self.iTimer3.callback.append(self.startTimerSetting)
	def gotSession(self,session):
		self.session=session;Type,AutoTimer,Personal,NumberSat,NameSat,Date,NumberDtt,DowDate,NameInfo=Load()
		if int(AutoTimer)==1:self.TimerSetting()
	def StopTimer(self):
		try:self.iTimer1.stop()
		except:pass
		try:self.iTimer2.stop()
		except:pass
		try:self.iTimer3.stop()
		except:pass
	def TimerSetting(self):
		try:self.StopTimer()
		except:pass
		now=time.time();ttime=time.localtime(now);start_time4=ttime[0],ttime[1],ttime[2],6,MinStart,0,ttime[6],ttime[7],ttime[8];start_time5=ttime[0],ttime[1],ttime[2],12,MinStart,0,ttime[6],ttime[7],ttime[8];start_time6=ttime[0],ttime[1],ttime[2],22,MinStart,0,ttime[6],ttime[7],ttime[8];start_time1=time.mktime(start_time4);start_time2=time.mktime(start_time5);start_time3=time.mktime(start_time6)
		if start_time1<now+60:start_time1+=86400
		if start_time2<now+60:start_time2+=86400
		if start_time3<now+60:start_time3+=86400
		delta1=int(start_time1-now);delta2=int(start_time2-now);delta3=int(start_time3-now);self.iTimer1.start(1000*delta1,_B);self.iTimer2.start(1000*delta2,_B);self.iTimer3.start(1000*delta3,_B)
	def startTimerSetting(self,Auto=_A):
		B='https://gioppygio.it/';A='https://picons.gioppygio.it';Type,AutoTimer,Personal,NumberSat,NameSat,Date,NumberDtt,DowDate,NameInfo=Load()
		def OnDsl():
			try:req=Request('http://gioppygio.it',None,{'User-agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'});context=ssl._create_unverified_context();response=urlopen(req,timeout=5,context=context);return _B
			except URLError as Error:
				if isinstance(Error.reason,socket.timeout):print('URL ERROR: ',Error)
				return _A
			except HTTPError as Error:
				if isinstance(Error.reason,socket.timeout):print('HTTPError: ',Error)
				return _A
			except socket.timeout as Error:print('socket.timeout: ',Error);return _A
			except Exception:return _A
		if OnDsl():
			for(jNumberSat,jNameSat,jLinkSat,jDateSat,jNumberDtt,jNameDtt,jLinkDtt,jDateDtt)in DownloadSetting():
				jDate=jDateSat
				if jDateDtt:
					if int(jDateDtt)>int(jDateSat):jDate=jDateDtt
				if jNumberSat==NumberSat and NumberDtt==jNumberDtt and jNameSat==NameSat:
					if jLinkSat.startswith(A)or jLinkDtt.startswith(B)or jLinkSat.startswith(B)or jLinkDtt.startswith(A):
						if jDate>Date or Auto:
							if StartProcess(jLinkSat,jLinkDtt,Type,Personal):now=time.time();jt=time.localtime(now);DowDate=str(jt[2]).zfill(2)+'-'+str(jt[1]).zfill(2)+'-'+str(jt[0])+'   '+str(jt[3]).zfill(2)+_E+str(jt[4]).zfill(2)+_E+str(jt[5]).zfill(2);WriteSave(Type,AutoTimer,Personal,jNumberSat,jNameSat,jDateSat,jNumberDtt,DowDate,NameInfo);OnclearMem();eDVBDB.getInstance().reloadServicelist();eDVBDB.getInstance().reloadBouquets();os.system(_K);MyMessage=NameInfo+' '+ConverDate(jDate)+_('\ninstalled!\n\nDo you want to download the Epg?\nThe download takes place in the background.');self.session.openWithCallback(self.downloadepg,MessageBox,MyMessage,MessageBox.TYPE_YESNO,default=_A,timeout=15)
							else:MyMessage=_('Sorry, cannot download !');self.session.open(MessageBox,MyMessage,MessageBox.TYPE_ERROR,timeout=5)
						break
					else:MyMessage=_('YOU ARE NOT ALLOWED TO\n\nDownload the GioppyGio plugin only from official sources!');self.session.open(MessageBox,MyMessage,MessageBox.TYPE_INFO)
		else:MyMessage=_('Sorry.\nno internet connection !');self.session.open(MessageBox,MyMessage,MessageBox.TYPE_ERROR,timeout=5)
		self.TimerSetting()
	def downloadepg(self,answer):
		if answer is _B:
			if os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/EPGImport/plugin.pyo')or os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/EPGImport/plugin.py')or os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/EPGImport/plugin.pyc'):
				if not os.path.exists('/etc/enigma2/epgimport.conf'):os.system('cp /usr/lib/enigma2/python/Plugins/Extensions/GioppyGio/Panel/epgimport.conf /etc/enigma2/')
				from Plugins.Extensions.EPGImport.plugin import AutoStartTimer,autoStartTimer,channelFilter,config,epgimport
				if autoStartTimer is not None and not epgimport.isImportRunning():autoStartTimer.runImport()
			else:self.session.openWithCallback(self.installepg,MessageBox,_('Epg Importer not found! Do you want to install it?'),MessageBox.TYPE_YESNO,default=_A,timeout=15)
		else:0
	def installepg(self,answer):
		if answer is _B:self.session.openWithCallback(self.instepg,Console,_('Install Epg Import'),[install_epg],closeOnSuccess=_B)
		else:0
	def instepg(self,string=''):MyMessage=_('Do you want to restart the GUI\nto apply the changes?');self.session.openWithCallback(self.downloadepginst,MessageBox,MyMessage,MessageBox.TYPE_YESNO,default=_A,timeout=15)
	def downloadepginst(self,answer):
		if answer is _B:self.session.open(TryQuitMainloop,3)
		else:0
