#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Please don't remove this disclaimer
# Code by Madhouse
_D='/Settings/Temp'
_C='mkdir '
_B='/Settings/Date'
_A='0'
import os,sys,xml.etree.cElementTree
from.Setting import*
try:from io import BytesIO as By_tesIO
except ImportError:from cStringIO import StringIO as By_tesIO
version='12.1'
UrlGitXml='https://raw.githubusercontent.com/GioppyGio/list-xml/main/new_set.xml'
Header={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
def OnclearMem():os.system('sync');os.system('echo 3 > /proc/sys/vm/drop_caches')
Directory=os.path.dirname(sys.modules[__name__].__file__)
if not os.path.exists(Directory+'/Settings'):os.system(_C+Directory+'/GioppyGio')
if not os.path.exists(Directory+_D):os.system(_C+Directory+_D)
def ConverDate(Date):
	if not Date:return
	day=Date[:2];month=Date[-6:][:2];year=Date[-4:];return day+'-'+month+'-'+year
def Downloadxml():
	try:import requests;link=requests.get(UrlGitXml,headers=Header,verify=False,timeout=(3,2));return link.content
	except requests.exceptions.HTTPError as errh:print('Http Error:',errh)
	except requests.exceptions.ConnectionError as errc:print('Error Connecting:',errc)
	except requests.exceptions.Timeout as errt:print('Timeout Error:',errt)
	except requests.exceptions.RequestException as err:print('OOps: Something Else',err)
def DownloadSetting():
	I='Date';H='Link';G='Name';F='Number';E='Marker';D='type';C='rule';B='name';A='ruleset';ListSettings=[]
	try:
		mdom=xml.etree.cElementTree.parse(By_tesIO(Downloadxml()))
		for x in mdom.getroot():
			if x.tag==A and x.get(B)=='Sat':rootsat=x
		for x in rootsat:
			if x.tag==C:
				if x.get(D)==E:NumberSat=str(x.get(F));NameSat=str(x.get(G));LinkSat=str(x.get(H));DateSat=str(x.get(I));ListSettings.append((NumberSat,NameSat,LinkSat,DateSat,_A,_A,_A,_A))
		for x in mdom.getroot():
			if x.tag==A and x.get(B)=='Satdual':rootsat=x
		for x in rootsat:
			if x.tag==C:
				if x.get(D)==E:NumberSat=str(x.get(F));NameSat=str(x.get(G));LinkSat=str(x.get(H));DateSat=str(x.get(I));ListSettings.append((NumberSat,NameSat,LinkSat,DateSat,_A,_A,_A,_A))
		for x in mdom.getroot():
			if x.tag==A and x.get(B)=='Sattrial':rootsat=x
		for x in rootsat:
			if x.tag==C:
				if x.get(D)==E:NumberSat=str(x.get(F));NameSat=str(x.get(G));LinkSat=str(x.get(H));DateSat=str(x.get(I));ListSettings.append((NumberSat,NameSat,LinkSat,DateSat,_A,_A,_A,_A))
		for x in mdom.getroot():
			if x.tag==A and x.get(B)=='Satquadri':rootsat=x
		for x in rootsat:
			if x.tag==C:
				if x.get(D)==E:NumberSat=str(x.get(F));NameSat=str(x.get(G));LinkSat=str(x.get(H));DateSat=str(x.get(I));ListSettings.append((NumberSat,NameSat,LinkSat,DateSat,_A,_A,_A,_A))
		for x in mdom.getroot():
			if x.tag==A and x.get(B)=='Satmotor':rootsat=x
		for x in rootsat:
			if x.tag==C:
				if x.get(D)==E:NumberSat=str(x.get(F));NameSat=str(x.get(G));LinkSat=str(x.get(H));DateSat=str(x.get(I));ListSettings.append((NumberSat,NameSat,LinkSat,DateSat,_A,_A,_A,_A))
		for x in mdom.getroot():
			if x.tag==A and x.get(B)=='dtt':rootsat=x
		for x in rootsat:
			if x.tag==C:
				if x.get(D)==E:NumberSat=str(x.get(F));NameSat=str(x.get(G));LinkSat=str(x.get(H));DateSat=str(x.get(I));ListSettings.append((NumberSat,NameSat,LinkSat,DateSat,_A,_A,_A,_A))
	except:pass
	return ListSettings
def Load():
	AutoTimer=_A;Type=_A;Personal=_A;NameSat=Date=NumberDtt=DowDate=NameInfo=_A;NumberSat='1'
	if os.path.exists(Directory+_B):
		xf=open(Directory+_B,'r');f=xf.readlines();xf.close()
		for line in f:
			try:
				LoadDate=line.strip();elements=LoadDate.split('=')
				if LoadDate.find('AutoTimer')!=-1:AutoTimer=elements[1][1:]
				elif LoadDate.find('Type')!=-1:Type=elements[1][1:]
				elif LoadDate.find('Personal')!=-1:Personal=elements[1][1:]
				elif LoadDate.find('NumberSat')!=-1:NumberSat=elements[1][1:]
				elif LoadDate.find('NameSat')!=-1:NameSat=elements[1][1:]
				elif LoadDate.find('jDateSat')!=-1:Date=elements[1][1:]
				elif LoadDate.find('NumberDtt')!=-1:NumberDtt=elements[1][1:]
				elif LoadDate.find('DowDate')!=-1:DowDate=elements[1][1:]
				elif LoadDate.find('NameInfo')!=-1:NameInfo=elements[1][1:]
			except:pass
	else:xf=open(Directory+_B,'w');xf.write('AutoTimer = 0\n');xf.write('Type = 0\n');xf.write('Personal = 0\n');xf.write('NumberSat = 1\n');xf.write('NameSat = Mono (13Â°E)\n');xf.write('jDateSat = 0\n');xf.write('NumberDtt = 0\n');xf.write('DowDate = 0\n');xf.write('NameInfo = 0\n');xf.close()
	return Type,AutoTimer,Personal,NumberSat,NameSat,Date,NumberDtt,DowDate,NameInfo
def WriteSave(Type,AutoTimer,Personal,NumberSat,NameSat,Date,NumberDtt,DowDate,NameInfo):xf=open(Directory+_B,'w');xf.write('AutoTimer = %s\n'%str(AutoTimer));xf.write('Type = %s\n'%str(Type));xf.write('Personal = %s\n'%str(Personal));xf.write('NumberSat = %s\n'%str(NumberSat));xf.write('NameSat = %s\n'%str(NameSat));xf.write('jDateSat = %s\n'%str(Date));xf.write('NumberDtt = %s\n'%str(NumberDtt));xf.write('DowDate = %s\n'%str(DowDate));xf.write('NameInfo = %s\n'%str(NameInfo));xf.close()
