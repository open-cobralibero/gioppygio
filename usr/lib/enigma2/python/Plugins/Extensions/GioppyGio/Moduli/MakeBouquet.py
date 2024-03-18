# -*- coding: utf-8 -*-
from __future__ import print_function
_g='%x:%x:%x'
_f='content'
_e='last_section_number'
_d='table_id'
_c='/dev/dvb/adapter%d/demux%d'
_b='bandwidth'
_a='scanbg'
_Z='wait_1'
_Y='TerrestrialScan'
_X='radio'
_W='service_id'
_V='tuner_text'
_U='status'
_T='signalQuality'
_S='section_number'
_R='version_number'
_Q='system'
_P='channel_list_id'
_O='progress_text'
_N='progress'
_M='action'
_L='tv'
_K='service_type'
_J=False
_I='onid'
_H='tsid'
_G='chmod -R 755 '
_F='original_network_id'
_E='transport_stream_id'
_D=True
_C=None
_B='header'
_A='frequency'
from.import _
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Screens.MessageBox import MessageBox
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.ProgressBar import ProgressBar
from Components.Sources.Progress import Progress
from Components.Sources.FrontendStatus import FrontendStatus
from Components.config import config
from enigma import eDVBResourceManager,eTimer,eDVBDB,eDVBFrontendParametersTerrestrial
import os,sys,datetime,time
from.TerrestrialScan import setParams,setParamsFe,downloadBar
dvbreaderarm='/usr/lib/enigma2/python/Plugins/Extensions/GioppyGio/Moduli/ReaderArm/dvbreader.so'
dvbreaderarmaa='/usr/lib/enigma2/python/Plugins/Extensions/GioppyGio/Moduli/ReaderArmAA/dvbreader.so'
dvbreaderarmpy2='/usr/lib/enigma2/python/Plugins/Extensions/GioppyGio/Moduli/ReaderArmP2/dvbreader.so'
dvbreadermips='/usr/lib/enigma2/python/Plugins/Extensions/GioppyGio/Moduli/ReaderMips/dvbreader.so'
dvbreadermipsp2='/usr/lib/enigma2/python/Plugins/Extensions/GioppyGio/Moduli/ReaderMipsP2/dvbreader.so'
dvbreaderaarch='/usr/lib/enigma2/python/Plugins/Extensions/GioppyGio/Moduli/ReaderAarch/dvbreader.so'
os.system(_G+dvbreaderarm)
os.system(_G+dvbreaderarmaa)
os.system(_G+dvbreaderarmpy2)
os.system(_G+dvbreadermips)
os.system(_G+dvbreadermipsp2)
os.system(_G+dvbreaderaarch)
try:py_version=sys.version_info.major
except:py_version=3
cpu=os.popen('uname -m').read().split()[0]
if cpu=='mips':
	if py_version==2:from.ReaderMipsP2 import dvbreader
	else:from.ReaderMips import dvbreader
elif cpu=='aarch64':from.ReaderAarch import dvbreader
elif py_version==2:from.ReaderArmP2 import dvbreader
else:from.ReaderArm import dvbreader
class MakeBouquet(Screen):
	skin=downloadBar
	def __init__(A,session,args=0):
		L='lcndescriptor';K='makexmlfile';J='makebouquet';I='FTA_only';H='transponders_unique';G='feid';D=session;B=args;print('[MakeBouquet][__init__] Starting...');print('[MakeBouquet][__init__] args',B);A.session=D;Screen.__init__(A,D);Screen.setTitle(A,_('MakeBouquet'));A.skinName=[_Y];A.path='/etc/enigma2';A.services_dict={};A.tmp_services_dict={};A.namespace_dict={};A.logical_channel_number_dict={};A.ignore_visible_service_flag=_J;A.VIDEO_ALLOWED_TYPES=[1,4,5,17,22,24,25,27,135];A.AUDIO_ALLOWED_TYPES=[2,10];E=[];C=[]
		with open('/usr/lib/enigma2/python/Plugins/Extensions/GioppyGio/Moduli/Settings/Select','r')as M:
			for F in M.readlines():
				if'DTTerrestrial'in F:
					N=F.split();E.append(N[0])
					for O in E:P=O.replace('tv---—','');C.append(P)
		if C==[]:A.BOUQUET_PREFIX='userbouquet.TerrestrialScan.'
		else:A.BOUQUET_PREFIX=C[0]
		A.bouquetsIndexFilename='bouquets.tv';A.bouquetFilename=A.BOUQUET_PREFIX+_L;A.bouquetName=_('—  DTTerrestrial LCN');A.namespace_complete_terrestrial=not(config.usage.subnetwork_terrestrial.value if hasattr(config.usage,'subnetwork_terrestrial')else _D);A.terrestrialXmlFilename='terrestrial.xml';A.frontend=_C;A.rawchannel=_C;A.scan_bg='/usr/lib/enigma2/python/Plugins/Extensions/GioppyGio/Panel/scanfhd.jpg';A['background']=Pixmap();A[_M]=Label(_('Starting scanner'));A[_U]=Label('');A[_N]=ProgressBar();A[_O]=Progress();A[_V]=Label('');A[_Z]=Label('');A[_a]=Pixmap();A['Frontend']=FrontendStatus(frontend_source=lambda:A.frontend,update_interval=100);A['actions']=ActionMap(['SetupActions'],{'cancel':A.keyCancel},-2);A.selectedNIM=-1;A.transponders_unique={};A.FTA_only=_J;A.makebouquet=_D;A.makexmlfile=_J;A.lcndescriptor=131;A.channel_list_id=0
		if B:
			if G in B:A.selectedNIM=B[G]
			if H in B:A.transponders_unique=B[H]
			if I in B:A.FTA_only=B[I]
			if J in B:A.makebouquet=B[J]
			if K in B:A.makexmlfile=B[K]
			if L in B:A.lcndescriptor=B[L]
			if _P in B:A.channel_list_id=B[_P]
		A.tsidOnidKeys=list(A.transponders_unique.keys());A.index=0;A.lockTimeout=50;A.onClose.append(A.__onClose);A.onFirstExecBegin.append(A.firstExec)
	def firstExec(A):
		if len(A.transponders_unique)>0:A[_Z].setText(_('Logical Channel Number (LCN) in progress'));A[_a].show();A[_M].setText(_('Making bouquet...'));A[_U].setText(_('Reading streams'));A.progresscount=len(A.transponders_unique);A.progresscurrent=1;A[_O].range=A.progresscount;A[_O].value=A.progresscurrent;A[_N].setRange((0,A.progresscount));A[_N].setValue(A.progresscurrent);A.timer=eTimer();A.timer.callback.append(A.readStreams);A.timer.start(100,1)
		else:A.showError(_('No transponders to read'))
	def readStreams(A):
		A[_V].setText('')
		if A.index<len(A.transponders_unique):A.transponder=A.transponders_unique[A.tsidOnidKeys[A.index]];A.progresscurrent=A.index;A[_O].value=A.progresscurrent;A[_N].setValue(A.progresscurrent);A[_M].setText(_('Tuning %s MHz')%str(A.transponder[_A]//1000000));A[_U].setText(_('TSID: %d, ONID: %d')%(A.transponder[_H],A.transponder[_I]));A.index+=1;A.searchtimer=eTimer();A.searchtimer.callback.append(A.getFrontend);A.searchtimer.start(100,1)
		else:
			if len(A.transponders_unique)>0:
				A.corelate_data();A.solveDuplicates()
				if config.plugins.TerrestrialScan.uhf_vhf.value!='xml'and A.makexmlfile:A.createTerrestrialXml()
				if A.makebouquet and len(A.services_dict)>0:A.createBouquet()
				B=[A.selectedNIM,A.transponders_unique]
			else:B=_C
			A.close(B)
	def getFrontend(A):
		B=eDVBResourceManager.getInstance()
		if not B:print('[MakeBouquet][getFrontend] Cannot retrieve Resource Manager instance');A.showError(_('Cannot retrieve Resource Manager instance'));return
		if A.rawchannel:del A.rawchannel
		A.frontend=_C;A.rawchannel=_C;A.rawchannel=B.allocateRawChannel(A.selectedNIM)
		if not A.rawchannel:print('[MakeBouquet][getFrontend] Cannot get the NIM');A.showError(_('Cannot get the NIM'));return
		print('[MakeBouquet][getFrontend] Will wait up to %i seconds for tuner lock.'%(A.lockTimeout//10));A[_V].setText(chr(ord('A')+A.selectedNIM));A.frontend=A.rawchannel.getFrontend()
		if not A.frontend:print('[MakeBouquet][getFrontend] Cannot get frontend');A.showError(_('Cannot get frontend'));return
		A.demuxer_id=A.rawchannel.reserveDemux()
		if A.demuxer_id<0:print('[MakeBouquet][getFrontend] Cannot allocate the demuxer');A.showError(_('Cannot allocate the demuxer'));return
		A.frontend.tune(setParamsFe(setParams(A.transponder[_A],A.transponder[_Q],A.transponder[_b])));A.lockcounter=0;A.locktimer=eTimer();A.locktimer.callback.append(A.checkTunerLock);A.locktimer.start(100,1)
	def checkTunerLock(A):
		B='tuner_state';A.dict={};A.frontend.getFrontendStatus(A.dict)
		if A.dict[B]=='TUNING':
			if A.lockcounter<1:print('[MakeBouquet][checkTunerLock] TUNING')
		elif A.dict[B]=='LOCKED':print('[MakeBouquet][checkTunerLock] TUNER LOCKED');A[_M].setText(_('Reading SI tables on %s MHz')%str(A.transponder[_A]//1000000));A.readTransponderCounter=0;A.readTranspondertimer=eTimer();A.readTranspondertimer.callback.append(A.readTransponder);A.readTranspondertimer.start(100,1);return
		elif A.dict[B]in('LOSTLOCK','FAILED'):print('[MakeBouquet][checkTunerLock] TUNING FAILED');A.readStreams();return
		A.lockcounter+=1
		if A.lockcounter>A.lockTimeout:print('[MakeBouquet][checkTunerLock] Timeout for tuner lock');A.readStreams();return
		A.locktimer.start(100,1)
	def readTransponder(A):A.readSDT();A.readNIT();A.readStreams()
	def readSDT(A):
		L=0;M=_c%(L,A.demuxer_id);A.tsid=_C;A.onid=_C;N=17;F=66;O=255;P=5;I=-1;E=[];J=0;D=[];G=_J;H=dvbreader.open(M,N,F,O,A.selectedNIM)
		if H<0:print('[MakeBouquet][readSDT] Cannot open the demuxer');return
		K=datetime.datetime.now();K+=datetime.timedelta(0,P)
		while _D:
			if datetime.datetime.now()>K:print('[Satfinder][getCurrentTsidOnid] Timed out');break
			B=dvbreader.read_sdt(H,F,0)
			if B is _C:time.sleep(.1);continue
			if B[_B][_d]==F and not G:
				if B[_B][_R]!=I:I=B[_B][_R];E=[];J=B[_B][_e]+1;D=[]
				if B[_B][_S]not in E:
					E.append(B[_B][_S]);D+=B[_f]
					if A.tsid is _C or A.onid is _C:A.tsid=A.transponder[_H]=B[_B][_E];A.onid=A.transponder[_I]=B[_B][_F]
					if len(E)==J:G=_D
			if G:break
		dvbreader.close(H)
		if not D:print('[MakeBouquet][readSDT] no services found on transponder');return
		for Q in range(len(D)):
			C=D[Q]
			if A.FTA_only and C['free_ca']!=0:continue
			if C[_K]not in A.VIDEO_ALLOWED_TYPES and C[_K]not in A.AUDIO_ALLOWED_TYPES:continue
			R=_g%(C[_E],C[_F],C[_W]);C[_T]=A.transponder[_T];A.tmp_services_dict[R]=C
	def readNIT(A):
		S='visible_service_flag';F='descriptor_tag';T=0;U=_c%(T,A.demuxer_id);V=16;G=64;I=0
		if I==0:M=255
		else:M=G^I^255
		W=20;N=-1;H=[];O=0;E=[];J=_J;K=dvbreader.open(U,V,G,M,A.selectedNIM)
		if K<0:print('[MakeBouquet][readNIT] Cannot open the demuxer');return
		P=datetime.datetime.now();P+=datetime.timedelta(0,W)
		while _D:
			if datetime.datetime.now()>P:print('[MakeBouquet][readNIT] Timed out reading NIT');break
			B=dvbreader.read_nit(K,G,I)
			if B is _C:time.sleep(.1);continue
			if B[_B][_d]==G and not J:
				if B[_B][_R]!=N:N=B[_B][_R];H=[];O=B[_B][_e]+1;E=[]
				if B[_B][_S]not in H:
					H.append(B[_B][_S]);E+=B[_f]
					if len(H)==O:J=_D
			if J:break
		dvbreader.close(K)
		if not E:print('[MakeBouquet][readNIT] current transponder not found');return
		C=[B for B in E if F in B and B[F]in(90,127)and B[_F]==A.transponder[_I]and B[_E]==A.transponder[_H]];print('[MakeBouquet][readNIT] transponders',C)
		if C:
			if C[0][F]==90:A.transponder[_Q]=eDVBFrontendParametersTerrestrial.System_DVB_T
			else:A.transponder[_Q]=eDVBFrontendParametersTerrestrial.System_DVB_T2
			if _A in C[0]and abs(C[0][_A]*10-A.transponder[_A])<1000000 and A.transponder[_A]!=C[0][_A]*10:print('[MakeBouquet][readNIT] updating transponder frequency from %.03f MHz to %.03f MHz'%(A.transponder[_A]//1000000,C[0][_A]//100000));A.transponder[_A]=C[0][_A]*10
		L=[B for B in E if F in B and B[F]==A.lcndescriptor and(A.lcndescriptor==131 or A.lcndescriptor==135 and(_P in B and B[_P]==A.channel_list_id or A.channel_list_id==0))and B[_F]==A.transponder[_I]];print('[MakeBouquet][readNIT] LCNs',L)
		if L:
			for D in L:
				Q=_g%(D[_E],D[_F],D[_W])
				if not A.ignore_visible_service_flag and S in D and D[S]==0:continue
				if Q not in A.logical_channel_number_dict or D[_E]==A.transponder[_H]:A.logical_channel_number_dict[Q]=D
		R=4008574976
		if A.namespace_complete_terrestrial:R|=A.transponder[_A]//1000000&65535
		X='%x:%x'%(A.transponder[_H],A.transponder[_I]);A.namespace_dict[X]=R
	def createBouquet(A):
		for B in(_L,_X):
			D=[B for B in A.services_dict.values()if B[_K]in A.AUDIO_ALLOWED_TYPES]
			if B==_X and(not D or not config.plugins.TerrestrialScan.makeradiobouquet.value):break
			A.tv_radio=B;C=A.readBouquetIndex()
			if'"'+A.bouquetFilename[:-2]+B+'"'not in C:A.writeBouquetIndex(C)
			A.writeBouquet()
		eDVBDB.getInstance().reloadBouquets()
	def corelate_data(A):
		C='logical_channel_number';D=A.iterateServicesBySNR(A.tmp_services_dict);A.duplicates=[]
		for B in D:
			if B in A.logical_channel_number_dict:
				A.tmp_services_dict[B][C]=A.logical_channel_number_dict[B][C]
				if A.logical_channel_number_dict[B][C]not in A.services_dict:A.services_dict[A.logical_channel_number_dict[B][C]]=A.tmp_services_dict[B]
				else:A.duplicates.append(A.tmp_services_dict[B])
	def solveDuplicates(A):
		if config.plugins.TerrestrialScan.uhf_vhf.value=='australia':
			B=[B for B in range(350,400)if B not in A.services_dict]
			for C in A.duplicates:
				if not B:break
				A.services_dict[B.pop(0)]=C
	def iterateServicesBySNR(B,servicesDict):A=[(A,B[_T])for(A,B)in servicesDict.items()];return[A[0]for A in sorted(A,key=lambda listItem:listItem[1],reverse=_D)]
	def readBouquetIndex(A):
		try:B=open(A.path+'/%s%s'%(A.bouquetsIndexFilename[:-2],A.tv_radio),'r')
		except Exception as D:return''
		C=B.read();B.close();return C
	def writeBouquetIndex(A,bouquetIndexContent):
		D=bouquetIndexContent;B=[];B.append('#NAME Bouquets (%s)\n'%('TV'if A.tv_radio==_L else'Radio'));B.append('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "%s%s" ORDER BY bouquet\n'%(A.bouquetFilename[:-2],A.tv_radio))
		if D:
			C=D.split('\n',1)
			if C[0][:6]!='#NAME ':B.append('%s\n'%C[0])
			if len(C)>1:B.append('%s'%C[1])
		E=open(A.path+'/'+A.bouquetsIndexFilename[:-2]+A.tv_radio,'w');E.write(''.join(B));E.close();del B
	def writeBouquet(A):
		E=not config.plugins.TerrestrialScan.makeradiobouquet.value and A.VIDEO_ALLOWED_TYPES+A.AUDIO_ALLOWED_TYPES or A.tv_radio==_L and A.VIDEO_ALLOWED_TYPES or A.tv_radio==_X and A.AUDIO_ALLOWED_TYPES;B=[];B.append('#NAME %s\n'%A.bouquetName);F=range(1,1001)
		for C in F:
			if C in A.services_dict and A.services_dict[C][_K]in E:B.append(A.bouquetServiceLine(A.services_dict[C]))
			else:B.append('#SERVICE 1:832:d:0:0:0:0:0:0:0:\n');B.append('#DESCRIPTION  \n')
		D=open(A.path+'/'+A.bouquetFilename[:-2]+A.tv_radio,'w');D.write(''.join(B));D.close();del B
	def bouquetServiceLine(B,service):A=service;return'#SERVICE 1:0:%x:%x:%x:%x:%x:0:0:0:\n'%(A[_K],A[_W],A[_E],A[_F],B.getNamespace(A))
	def getNamespace(A,service):B=service;C='%x:%x'%(B[_E],B[_F]);return A.namespace_dict[C]if C in A.namespace_dict else 4008574976
	def createTerrestrialXml(C):
		A=['<?xml version="1.0" encoding="UTF-8"?>\n'];A.append('<!-- File created on %s with the TerrestrialScan plugin -->\n'%time.strftime('%A, %d of %B %Y, %H:%M:%S'));A.append('<locations>\n');A.append('\t<terrestrial name="My local region (Europe DVB-T/T2)" flags="5">\n')
		for E in C.iterateUniqueTranspondersByFrequency():B=C.transponders_unique[E];A.append('\t\t<transponder centre_frequency="%d" system="%d" bandwidth="%d" constellation="3"/><!-- onid="%d" tsid="%d" signal_quality="%d" -->\n'%(B[_A],B[_Q],B[_b]==7 and 1 or 0,B[_I],B[_H],B[_T]))
		A.append('\t</terrestrial>\n');A.append('</locations>');D=open(C.path+'/'+C.terrestrialXmlFilename,'w');D.write(''.join(A));D.close();del A
	def iterateUniqueTranspondersByFrequency(A):B=[(A[0],A[1][_A])for A in A.transponders_unique.items()];return[A[0]for A in sorted(B,key=lambda listItem:listItem[1])]
	def showError(A,message):B=A.session.open(MessageBox,message,MessageBox.TYPE_ERROR);B.setTitle(_(_Y));A.close()
	def keyCancel(A):A.close()
	def __onClose(A):
		if A.frontend:A.frontend=_C;del A.rawchannel
