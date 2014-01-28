# coding: utf-8
import urllib
import re

"""
Skilar lista af ordum sem giskad var a.

Breytur:
unnid -- greinda malsynid
villulisti -- fylki orda sem giskad var a
"""
class Giskord:
    def __init__(self, unnid):
        self.unnid = unnid

    def giskord(self):
        n=0
        listi =[]
        villulisti =[]
        error=0
        for item in self.unnid:
            for word in item.split():
                listi.append(word)
                if word =="*":
                    try:
                        villulisti.append(listi[n-1])
                        villulisti.append(listi[n-2])
                        listi.remove(listi[n])
                        listi.remove(listi[n-1])
                        listi.remove(listi[n-2])
                    except:
                        error=error+1
                n=n+1
        return villulisti

"""
Skilar lista af ordum sem ekki var giskad a.

Breytur:
unnid -- greinda malsynid
listi -- fylki orda sem ekki var giskad a
"""
class Angiskorda:
    def __init__(self, unnid):
        self.unnid = unnid

    def angiskorda(self):
        error=0
        n=0
        listi =[]

        for item in self.unnid:
            for word in item.split():
                listi.append(word)
                if word =="*":
                    try:
                        listi.remove(listi[n])
                        listi.remove(listi[n-1])
                        listi.remove(listi[n-2])
                    except:
                        error=error+1
                n=n+1
        return listi

"""
Skilar tolfraedi synisins

Breytur:
so -- fjoldi sagnorda
fn  -- fjoldi fornafna
no  -- fjoldi nafnorda
ao  -- fjoldi atviksorda
uh -- fjoldi upphropanna
fs  -- fjoldi forsetninga
lo  -- fjoldi lysingarorda
st -- fjoldi samtenginga
nutid  -- fjoldi sagna i nutid
thatid -- fjoldi sagna i thatid
sfn,snn, sthn, sbn,svn,ssn,sgn -- flokkar sagna
fyrstapn -- fjoldi sagna i 1. personu
onnurpn -- fjoldi sagna i 2. personu
thridjapn -- fjoldi sagna i 3. personu
"""
class Ordflokkatolfraedi:
    def __init__(self, listi):
        self.listi = listi

    def tolfraedi(self):
        so=0
        fn=0
        no=0
        ao=0
        uh=0
        fs=0
        lo=0
        st=0
        nutidin=0
        thatidin=0
        sf=0
        sn=0
        sth=0
        sb=0
        sv=0
        ss=0
        sg=0
        fyrstap=0
        onnurp=0
        thridjap=0
        for i in range(1,len(self.listi), 2):
            if self.listi[i].startswith("s"):
                so=so+1
                if self.listi[i].startswith("sf"):
                    sf=sf+1
                if self.listi[i].startswith("sn"):
                    sn=sn+1
                if self.listi[i].startswith("sþ"):
                    sth=sth+1
                if self.listi[i].startswith("sb"):
                    sb=sb+1
                if self.listi[i].startswith("sv"):
                    sv=sv+1
                if self.listi[i].startswith("ss"):
                    ss=ss+1
                if self.listi[i].startswith("sg"):
                    sg=sg+1
                if "1" in self.listi[i]:
                    fyrstap=fyrstap+1
                if "2" in self.listi[i]:
                    onnurp=onnurp+1
                if "3" in self.listi[i]:
                    thridjap=thridjap+1
                if self.listi[i].endswith("n"):
                    nutidin=nutidin+1
                else:
                    thatidin=thatidin+1
            elif self.listi[i].startswith("n"):
                no=no+1
            elif self.listi[i].startswith("l"):
                lo=lo+1
            elif self.listi[i].startswith("f"):
                fn=fn+1
            elif self.listi[i].startswith("c"):
                st=st+1
            elif self.listi[i].startswith("aa"):
                ao=ao+1
            elif self.listi[i].startswith("au"):
                uh=uh+1
            else:
                fs=fs+1
    
        if (fyrstap+onnurp+thridjap)==0:
            samtalspersona=1.0
        else:
            samtalspersona=float(fyrstap+onnurp+thridjap)
    
        fyrstapn=fyrstap/samtalspersona
        onnurpn=onnurp/samtalspersona
        thridjapn=thridjap/samtalspersona
    
        if (sf+sn+sth+sb+sv+ss+sg)==0:
            samtalshaettir=1.0
        else:
            samtalshaettir=float(sf+sn+sth+sb+sv+ss+sg)
    
        sfn=sf/samtalshaettir
        snn= sn/samtalshaettir
        sthn= sth/samtalshaettir
        sbn= sb/samtalshaettir
        svn= sv/samtalshaettir
        ssn= ss/samtalshaettir
        sgn= sg/samtalshaettir
    
        if (nutidin+thatidin)==0:
            samtalstidir=1.0
        else:
            samtalstidir=float(nutidin+thatidin)
        nutid=nutidin/samtalstidir
        thatid=thatidin/samtalstidir
        return (so, fn, no, ao, uh,fs, lo, st, nutid, thatid,   sfn,snn, sthn, sbn, svn,ssn,sgn, fyrstapn,onnurpn,thridjapn)


"""
Reiknar tolfraedi sem ekki tengist ordflokkum.
"""
class Tolfraedimalsynis:
    def __init__(self, setningalisti):
        self.setningalisti = setningalisti

    """
    Reiknar medallengd segda barns

    Breytur:
    blinur -- fjoldi segda barns
    bord -- fjoldi orda barns
    mlsbarn -- medallengd segda barns
    """
    def mlsbarn(self):
        blinur = 0
        bord = 0
        for item in self.setningalisti:
            item =re.sub(r'\[[^)]*\]', '', item)
            if item.find("B") == 0:
                blinur= blinur+1
                bord = bord + len(item.split()) -1
        if blinur>>0:
            bord=float(bord)
            mlsbarn = float(bord/blinur)
        else:
            mlsbarn = 0  
        return mlsbarn

    """
    Reiknar fjolda mismunandi orda

    Breytur:
    ordaset -- oll mismunandi ord barns
    misbord -- fjoldi mismunandi orda
    """
    def misbord(self):
        ordaset = set([])
        for item in self.setningalisti:
            item =re.sub(r'\[[^)]*\]', '', item)
            if item.find("B") == 0:
                ordaset = ordaset | set(item.split())
        misbord= len(ordaset) -1
        return misbord

    """
    Reiknar fjolda orda barns

    Breytur:
    bord -- fjoldi mismunandi orda
    """
    def bord(self):
        bord = 0
        for item in self.setningalisti:
            item =re.sub(r'\[[^)]*\]', '', item)
            if item.find("B") == 0:
                bord = bord + len(item.split()) -1
        return bord

"""
Skilar malsyni unnid fra IceNLP

Breytur:
malsyni -- malsynid
unnid -- fylki setninga sem hefur verid greint
"""
class Greining:
    def __init__(self, malsyni):
        self.malsyni = malsyni

    """
    Sendir og tekur vid fra IceNLP
    """
    def unnid(self):
        splittadur = self.malsyni.split('\n')
        url = "http://nlp.cs.ru.is/IceNLPWebService/?mode=icenlp&tagging=true&markunknown=true&query="
        unnid = []
        for item in splittadur:
            uniitem = unicode(item.replace("B ","").replace("V ", ""))
            utf8item = uniitem.encode('utf-8')
            results = urllib.urlopen(url+utf8item)
            unnid.append(results.read())
        return unnid

"""
Flokkar ordin sem giskad var a
"""
class Giskordaflokkun:
    def __init__(self, villulisti):
        self.villulisti = villulisti

    """
    Flokkar sagnord

    Breytur:
    sagnir -- fylki sagnorda
    """
    def sagnir(self):
        i=0
        sagnir=[]
        for i in range(0,len(self.villulisti), 2):
            if self.villulisti[i].startswith("s"):
                sagnir.append('%s' % (self.villulisti[i+1]))
        return sagnir

    """
    Flokkar nafnord

    Breytur:
    nafnord -- fylki nafnorda
    """
    def nafnord(self):
        i=0
        nafnord=[]
        for i in xrange(0,len(self.villulisti), 2):
            if self.villulisti[i].startswith("n"):
                nafnord.append('%s' % (self.villulisti[i+1]))
        return nafnord

    """
    Flokkar lysingarord

    Breytur:
    lysingar -- fylki lysingarorda
    """
    def lysingar(self):
        i=0
        lysingar=[]
        for i in xrange(0,len(self.villulisti), 2):
            if self.villulisti[i].startswith("l"):
                lysingar.append('%s' % (self.villulisti[i+1]))
        return lysingar

    """
    Flokkar atviksord

    Breytur:
    atviks -- fylki atviksorda
    """
    def atviks(self):
        i=0
        atviks=[]
        for i in xrange(0,len(self.villulisti), 2):
            if self.villulisti[i].startswith("a"):
                atviks.append('%s' % (self.villulisti[i+1]))
        return atviks

"""
Telur fjolda villna i malsyni

Breytur:
malsyni -- malsynid
villufjoldi -- fjoldi villna
"""
class Villur:
    def __init__(self, malsyni):
        self.malsyni = malsyni

    def villufjoldi(self):
        villurnar=[]
        for sentence in re.findall('([A-Z][^\.!?]*[\.!?])', self.malsyni):
            if u"„" in sentence:
                villurnar.append(sentence)
        villufjoldi = len(villurnar)
        return villufjoldi
