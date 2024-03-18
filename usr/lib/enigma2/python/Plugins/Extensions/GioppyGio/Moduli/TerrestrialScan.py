from __future__ import print_function
_R='wait_1'
_Q='tuner_text'
_P='scanbg'
_O='status'
_N='australia'
_M=True
_L='progress_text'
_K='progress'
_J='action'
_I='uhf'
_H='nothing'
_G='DVB-T'
_F='uhf_vhf'
_E=False
_D='bandwidth'
_C='system'
_B='frequency'
_A=None
from.import _
from enigma import getDesktop
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Screens.MessageBox import MessageBox
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.ProgressBar import ProgressBar
from Components.Sources.Progress import Progress
from Components.Sources.FrontendStatus import FrontendStatus
from Components.NimManager import nimmanager
from enigma import eDVBFrontendParameters,eDVBFrontendParametersTerrestrial,eDVBResourceManager,eTimer,iFrontendInformation
import os,sys,datetime,time
try:py_version=sys.version_info.major
except:py_version=3
cpu=os.popen('uname -m').read().split()[0]
if cpu=='mips':
	if py_version==2:from.ReaderMipsP2 import dvbreader
	else:from.ReaderMips import dvbreader
elif cpu=='aarch64':from.ReaderAarch import dvbreader
elif py_version==2:from.ReaderArmP2 import dvbreader
else:from.ReaderArm import dvbreader
def insertValues(xml,values):return xml%tuple([int(-(A*getDesktop(0).size().height()//-720))for A in values])
def downloadBarTemplate():A=22;I=40;J=60;K=36;D=1280;L=720;B=30;C=4;M=7;N=433;O=466;P=433;E=929;F=3;G=25;H=24;Q=955;R=A;S=980;T=87;U=1080;V=87;W=1187;X=73;Y='\n\t<screen name="DownloadBar" position="0,0" size="%d,%d" flags="wfNoBorder" backgroundColor="#ff000000">\n\t\t<eLabel position="0,0" size="e,%d" backgroundColor="#100d37" zPosition="-1"/>\n\t\t<widget name="scanbg" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GioppyGio/Panel/scanfhd.jpg" position="0,0" alphatest="blend" size="1920,1080" transparent="1" zPosition="-2" />\n\t\t<widget name="action" position="%d,%d" size="%d,%d" font="gioppyregular;%d" transparent="1" foregroundColor="#ffffff"/>\n\t\t<widget name="status" position="%d,%d" size="%d,%d" font="gioppyregular;%d" halign="center" transparent="1" foregroundColor="#ffffff"/>\n\t\t<widget source="Frontend" conditional="Frontend" render="Pixmap" pixmap="icons/lock_on.png" position="%d,%d" size="%d,%d" alphatest="on" scale="1">\n\t\t\t<convert type="FrontendInfo">LOCK</convert>\n\t\t\t<convert type="ConditionalShowHide"/>\n\t\t</widget>\n\t\t<widget name="wait_1" position="0,center" zPosition="1" size="%d,%d" font="gioppyregular;%d" halign="center" valign="center" foregroundColor="#00ffc000" backgroundColor="#00000000" borderColor="#000000" borderWidth="2" transparent="1" />\n\t\t<widget source="Frontend" conditional="Frontend" render="Pixmap" pixmap="icons/lock_off.png" position="%d,%d" size="%d,%d" alphatest="on" scale="1">\n\t\t\t<convert type="FrontendInfo">LOCK</convert>\n\t\t\t<convert type="ConditionalShowHide">Invert</convert>\n\t\t</widget>\n\t\t<widget name="tuner_text" conditional="tuner_text" position="%d,%d" size="%d,%d" font="gioppyregular;%d" halign="center" transparent="1" foregroundColor="#ffffff"/>\n\t\t<widget source="Frontend" conditional="Frontend" render="Label" position="%d,%d" size="%d,%d" font="gioppyregular;%d" halign="left" transparent="1" foregroundColor="#ffffff">\n\t\t\t<convert type="FrontendInfo">SNRdB</convert>\n\t\t</widget>\n\t\t<widget source="progress_text" render="Label" position="%d,%d" size="%d,%d" font="gioppyregular;%d" halign="right" transparent="1" foregroundColor="#ffffff">\n\t\t\t<convert type="ProgressToText">InText</convert>\n\t\t</widget>\n\t\t<widget source="progress_text" render="Label" position="%d,%d" size="%d,%d" font="gioppyregular;%d" halign="left" transparent="1" foregroundColor="#ffffff">\n\t\t\t<convert type="ProgressToText">InPercent</convert>\n\t\t</widget>\n\t</screen>';Z=[D,L,K,M,C,N,B,A,O,C,P,B,A,E,F,G,H,D,J,I,E,F,G,H,Q,C,R,B,A,S,C,T,B,A,U,C,V,B,A,W,C,X,B,A];return insertValues(Y,Z)
downloadBar=downloadBarTemplate()
def setParams(frequency,system,bandwidth):A=eDVBFrontendParametersTerrestrial();A.frequency=frequency;A.bandwidth=bandwidth;A.code_rate_hp=eDVBFrontendParametersTerrestrial.FEC_Auto;A.code_rate_lp=eDVBFrontendParametersTerrestrial.FEC_Auto;A.inversion=eDVBFrontendParametersTerrestrial.Inversion_Unknown;A.system=system;A.modulation=eDVBFrontendParametersTerrestrial.Modulation_Auto;A.transmission_mode=eDVBFrontendParametersTerrestrial.TransmissionMode_Auto;A.guard_interval=eDVBFrontendParametersTerrestrial.GuardInterval_Auto;A.hierarchy=eDVBFrontendParametersTerrestrial.Hierarchy_Auto;return A
def setParamsFe(params):A=eDVBFrontendParameters();A.setDVBT(params);return A
def channel2freq(channel,bandwidth=8):
	B=bandwidth;A=channel
	if 4<A<13:return(177+B*(A-5))*1000000+500000
	elif 20<A<70:return(474+B*(A-21))*1000000
def getChannelNumber(frequency,descr):
	C=descr;A=(frequency+50000)/100000/1e1
	if C in(_I,_F):
		if 174<A<230:B=(A+1)%7;return str(int(A-174)//7+5)+(B<3 and'-'or B>4 and'+'or'')
		elif 470<=A<863:B=(A+2)%8;return str(int(A-470)//8+21)+(B<3.5 and'-'or B>4.5 and'+'or'')
	elif C==_N:
		if 174<A<202:return str(int(A-174)//7+6)
		elif 202<=A<209:return'9A'
		elif 209<=A<230:return str(int(A-209)//7+10)
		elif 526<A<820:return str(int(A-526)//7+28)
	return''
class TerrestrialScanGio(Screen):
	skin=downloadBar
	def __init__(A,session,args=0):
		P='uhf_short';O='skipT2';N='country';M='region';L='stabliseTime';K='restrict_to_networkid';J='networkid';I='feid';G=session;B=args;print('[TerrestrialScan][__init__] Starting...');print('[TerrestrialScan][__init__] args',B);A.session=G;Screen.__init__(A,G);Screen.setTitle(A,_('GioppyGio - Scanner DTT'));A['background']=Pixmap();A[_J]=Label(_('Starting scanner'));A[_O]=Label('');A[_K]=ProgressBar();A[_P]=Pixmap();A[_P].hide();A[_L]=Progress();A[_Q]=Label('');A[_R]=Label('');A.scan_bg='/usr/lib/enigma2/python/Plugins/Extensions/GioppyGio/Panel/scanfhd.jpg';A['actions']=ActionMap(['SetupActions'],{'cancel':A.keyCancel},-2);A.selectedNIM=-1;A.uhf_vhf=_I;A.networkid=0;A.restrict_to_networkid=_E;A.stabliseTime=2;A.region=_A;A.country=_A;A.skipT2=_E
		if B:
			if I in B:A.selectedNIM=B[I]
			if _F in B:A.uhf_vhf=B[_F]
			if J in B:A.networkid=B[J]
			if K in B:A.restrict_to_networkid=B[K]
			if L in B:A.stabliseTime=B[L]
			if M in B:A.region=B[M]
			if N in B:A.country=B[N]
			if O in B:A.skipT2=B[O]
		A.isT2tuner=_E;A.frontend=_A;A['Frontend']=FrontendStatus(frontend_source=lambda:A.frontend,update_interval=100);A.rawchannel=_A;A.session.postScanService=A.session.nav.getCurrentlyPlayingServiceOrGroup();A.index=0;A.frequency=0;A.system=eDVBFrontendParametersTerrestrial.System_DVB_T;A.lockTimeout=50;A.tsidOnidTimeout=100;A.snrTimeout=100;A.bandwidth=8;A.scanTransponders=[];H=(eDVBFrontendParametersTerrestrial.System_DVB_T,)if A.skipT2 else(eDVBFrontendParametersTerrestrial.System_DVB_T,eDVBFrontendParametersTerrestrial.System_DVB_T2)
		if A.uhf_vhf==_F:
			C=7
			for D in range(5,13):
				for F in H:A.scanTransponders.append({_B:channel2freq(D,C),_C:F,_D:C*1000000})
		if A.uhf_vhf in(_I,P,_F):
			C=8
			for D in range(21,50 if A.uhf_vhf==P else 70):
				for F in H:A.scanTransponders.append({_B:channel2freq(D,C),_C:F,_D:C*1000000})
		if A.uhf_vhf==_N:
			C=7;Q=177500000
			for D in list(range(0,8))+list(range(50,74)):R=Q+(D*C*1000000+(2000000 if D>8 else 0));A.scanTransponders.append({_B:R,_C:eDVBFrontendParametersTerrestrial.System_DVB_T,_D:C*1000000})
		if A.uhf_vhf=='xml':
			for E in nimmanager.getTranspondersTerrestrial(A.region):
				if E[10]<1:A.scanTransponders.append({_B:E[1],_C:eDVBFrontendParametersTerrestrial.System_DVB_T,_D:E[2]})
				if E[10]!=0:A.scanTransponders.append({_B:E[1],_C:eDVBFrontendParametersTerrestrial.System_DVB_T2,_D:E[2]})
		A.transponders_found=[];A.transponders_unique={};A.onClose.append(A.__onClose);A.onFirstExecBegin.append(A.firstExec)
	def showError(A,message):B=A.session.open(MessageBox,message,MessageBox.TYPE_ERROR);B.setTitle(_('TerrestrialScan'));A.close()
	def keyCancel(A):A.close()
	def firstExec(A):
		if len(A.scanTransponders)>0:A[_J].setText(_('Starting search...'));A[_O].setText(_('Scanning for active transponders'));A.progresscount=len(A.scanTransponders);A.progresscurrent=1;A[_L].range=A.progresscount;A[_L].value=A.progresscurrent;A[_K].setRange((0,A.progresscount));A[_K].setValue(A.progresscurrent);A.timer=eTimer();A.timer.callback.append(A.search);A.timer.start(100,1)
		else:A.showError(_('No frequencies to search'))
	def search(A):
		A[_Q].setText('')
		if A.index<len(A.scanTransponders):
			A.system=A.scanTransponders[A.index][_C];A.bandwidth=A.scanTransponders[A.index][_D];A.frequency=A.scanTransponders[A.index][_B];B=getChannelNumber(A.frequency,A.uhf_vhf=='xml'and(_N if A.country=='AUS'else _I)or A.uhf_vhf);A.channelNumberText=_('(ch %s)')%B if B else'';print('[TerrestrialScan][Search] Scan frequency %d %s'%(A.frequency,A.channelNumberText));print('[TerrestrialScan][Search] Scan system %d'%A.system);print('[TerrestrialScan][Search] Scan bandwidth %d'%A.bandwidth);A.progresscurrent=A.index;A[_L].value=A.progresscurrent;A[_K].setValue(A.progresscurrent);A[_J].setText(_('Tuning %s MHz %s')%(str(A.frequency//1000000),A.channelNumberText));A[_O].setText((len(A.transponders_unique)==1 and _('Found %d unique transponder')or _('Found %d unique transponders'))%len(A.transponders_unique));A.index+=1
			if A.frequency in A.transponders_found or A.system==eDVBFrontendParametersTerrestrial.System_DVB_T2 and A.isT2tuner==_E:print('[TerrestrialScan][Search] Skipping T2 search of %s MHz %s'%(str(A.frequency//1000000),A.channelNumberText));A.search();return
			A.searchtimer=eTimer();A.searchtimer.callback.append(A.getFrontend);A.searchtimer.start(100,1)
		else:
			if len(A.transponders_unique)>0:C=[A.selectedNIM,A.transponders_unique]
			else:C=_A
			A.close(C)
	def config_mode(B,nim):
		A=nim
		try:return A.config_mode
		except AttributeError:return A.isCompatible(_G)and A.config_mode_dvbt or _H
	def getFrontend(A):
		N='No terrestrial tuner found';M='[TerrestrialScan][getFrontend] No terrestrial tuner found';G='DVB-S';F='DVB-T2';print('[TerrestrialScan][getFrontend] searching for available tuner');C=[]
		if A.selectedNIM<0:
			for B in nimmanager.nim_slots:
				if A.config_mode(B)not in(_H,)and(B.isCompatible(F)or B.isCompatible(G)and B.canBeCompatible(F)):C.append(B.slot);A.isT2tuner=_M
			if len(C)==0:
				print('[TerrestrialScan][getFrontend] No T2 tuner found')
				for B in nimmanager.nim_slots:
					if A.config_mode(B)not in(_H,)and(B.isCompatible(_G)or B.isCompatible(G)and B.canBeCompatible(_G)):C.append(B.slot)
			if len(C)==0:print(M);A.showError(_(N));return
		else:
			B=nimmanager.nim_slots[A.selectedNIM]
			if A.config_mode(B)not in(_H,)and(B.isCompatible(F)or B.isCompatible(G)and B.canBeCompatible(F)):C.append(B.slot);A.isT2tuner=_M
			if len(C)==0:
				print('[TerrestrialScan][getFrontend] User selected tuner is not T2 compatible')
				if A.config_mode(B)not in(_H,)and(B.isCompatible(_G)or B.isCompatible(G)and B.canBeCompatible(_G)):C.append(B.slot)
			if len(C)==0:print('[TerrestrialScan][getFrontend] User selected tuner not configured');A.showError(_('Selected tuner is not cofigured'));return
		if len(C)==0:print(M);A.showError(_(N));return
		H=eDVBResourceManager.getInstance()
		if not H:print('[TerrestrialScan][getFrontend] Cannot retrieve Resource Manager instance');A.showError(_('Cannot retrieve Resource Manager instance'));return
		if A.selectedNIM<0:print('[TerrestrialScan][getFrontend] Choosing NIM')
		if A.session.pipshown:A.session.pipshown=_E;del A.session.pip;print('[TerrestrialScan][getFrontend] Stopping PIP.')
		I=_A;J=A.session and A.session.nav.getCurrentService();K=J and J.frontendInfo();L=K and K.getAll(_M)
		if L is not _A:I=L.get('tuner_number',_A)
		del K;del J;E=-1
		if A.rawchannel:del A.rawchannel
		A.frontend=_A;A.rawchannel=_A;C.reverse()
		for D in C:
			if E==-1:E=D
			A.rawchannel=H.allocateRawChannel(D)
			if A.rawchannel:print('[TerrestrialScan][getFrontend] Nim found on slot id %d'%D);E=D;break
		if E==-1:print('[TerrestrialScan][getFrontend] No valid NIM found');A.showError(_('No valid NIM found for terrestrial'));return
		if not A.rawchannel:
			if I in C:
				D=I;print("[TerrestrialScan][getFrontend] Nim found on slot id %d but it's busy. Stopping active service"%D);A.session.postScanService=A.session.nav.getCurrentlyPlayingServiceReference();A.session.nav.stopService();A.rawchannel=H.allocateRawChannel(D)
				if A.rawchannel:A[_R].setText(_('Scanning is in progress... Please wait'));A[_P].show();print('[TerrestrialScan][getFrontend] The active service was stopped, and the NIM is now free to use.');E=D
			if not A.rawchannel:
				if A.session.nav.RecordTimer.isRecording():print('[TerrestrialScan][getFrontend] Cannot free NIM because a recording is in progress');A.showError(_('Cannot free NIM because a recording is in progress'));return
				else:print('[TerrestrialScan][getFrontend] Cannot get the NIM');A.showError(_('Cannot get the NIM'));return
		print('[TerrestrialScan][getFrontend] Will wait up to %i seconds for tuner lock.'%(A.lockTimeout//10));A.selectedNIM=E;A[_Q].setText(chr(ord('A')+E));A.frontend=A.rawchannel.getFrontend()
		if not A.frontend:print('[TerrestrialScan][getFrontend] Cannot get frontend');A.showError(_('Cannot get frontend'));return
		A.rawchannel.requestTsidOnid();A.tsid=_A;A.onid=_A;A.demuxer_id=A.rawchannel.reserveDemux()
		if A.demuxer_id<0:print('[TerrestrialScan][getFrontend] Cannot allocate the demuxer');A.showError(_('Cannot allocate the demuxer'));return
		A.frontend.tune(setParamsFe(setParams(A.frequency,A.system,A.bandwidth)));A.lockcounter=0;A.locktimer=eTimer();A.locktimer.callback.append(A.checkTunerLock);A.locktimer.start(100,1)
	def checkTunerLock(A):
		B='tuner_state';A.dict={};A.frontend.getFrontendStatus(A.dict)
		if A.dict[B]=='TUNING':
			if A.lockcounter<1:print('[TerrestrialScan][checkTunerLock] TUNING')
		elif A.dict[B]=='LOCKED':print('[TerrestrialScan][checkTunerLock] LOCKED');A[_J].setText(_('Reading %s MHz %s')%(str(A.frequency//1000000),A.channelNumberText));A.tsidOnidtimer=eTimer();A.tsidOnidtimer.callback.append(A.tsidOnidWait);A.tsidOnidtimer.start(100,1);return
		elif A.dict[B]in('LOSTLOCK','FAILED'):print('[TerrestrialScan][checkTunerLock] TUNING FAILED');A.search();return
		A.lockcounter+=1
		if A.lockcounter>A.lockTimeout:print('[TerrestrialScan][checkTunerLock] Timeout for tuner lock');A.search();return
		A.locktimer.start(100,1)
	def tsidOnidWait(A):
		A.getCurrentTsidOnid()
		if A.tsid is not _A and A.onid is not _A:print('[TerrestrialScan][tsidOnidWait] tsid & onid found',A.tsid,A.onid);A.signalQualityCounter=0;A.signalQualitytimer=eTimer();A.signalQualitytimer.callback.append(A.signalQualityWait);A.signalQualitytimer.start(100,1);return
		print('[TerrestrialScan][tsidOnidWaitABM] tsid & onid wait failed');A.search()
	def getCurrentTsidOnid(A,from_retune=_E):
		E='header';G=0;H='/dev/dvb/adapter%d/demux%d'%(G,A.demuxer_id);I=time.time();J=17;C=66;K=255;L=5;A.tsid=_A;A.onid=_A;D=dvbreader.open(H,J,C,K,A.selectedNIM)
		if D<0:print('[TerrestrialScan][getCurrentTsidOnid] Cannot open the demuxer');return
		F=datetime.datetime.now();F+=datetime.timedelta(0,L)
		while _M:
			if datetime.datetime.now()>F:print('[TerrestrialScan][getCurrentTsidOnid] Timed out');break
			B=dvbreader.read_sdt(D,C,0)
			if B is _A:time.sleep(.1);continue
			if B[E]['table_id']==C:A.tsid=B[E]['transport_stream_id'];A.onid=B[E]['original_network_id'];break
		print('[TerrestrialScan][getCurrentTsidOnid] Read time %.1f seconds.'%(time.time()-I));dvbreader.close(D)
	def signalQualityWait(A):
		E='signalQuality';B=A.frontend.readFrontendData(iFrontendInformation.signalQuality)
		if B>0:
			time.sleep(A.stabliseTime);B=A.frontend.readFrontendData(iFrontendInformation.signalQuality)
			if B>0:
				D={_B:A.frequency,'tsid':A.tsid,'onid':A.onid,_C:A.system,_D:A.bandwidth,E:B};A.transponders_found.append(A.frequency);C='%x:%x'%(A.tsid,A.onid)
				if(C not in A.transponders_unique or A.transponders_unique[C][E]<B)and(not A.restrict_to_networkid or A.networkid==A.onid):A.transponders_unique[C]=D
				print('[TerrestrialScan][signalQualityWait] transponder details',D);A.search();return
		A.signalQualityCounter+=1
		if A.signalQualityCounter>A.snrTimeout:print('[TerrestrialScan][signalQualityWait] Failed to collect SNR');A.search();return
		A.signalQualitytimer.start(100,1)
	def __onClose(A):
		if A.frontend:A.frontend=_A;del A.rawchannel
