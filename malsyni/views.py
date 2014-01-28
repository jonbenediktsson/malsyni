# coding: utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.decorators import user_passes_test
import re
from django.views.decorators.csrf import csrf_exempt
import urvinnsla
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, View, TemplateView
from malsyni.forms import Malsyniform
from malsyni.urvinnsla import Tolfraedimalsynis, Greining, Giskord, Angiskorda, Giskordaflokkun, Villur, Ordflokkatolfraedi

"""
Hondlar innskraningu og villur eftir notendanafni og lykilordi. Endurskrifad fra venjulegu login adferdinni til ad hafa oll view class based. Nafnahefd eftir best practice.

Breytur:
template_name -- html templateid sem sidan notar
form_class -- hvernig typa af formi thetta er
"""
class Login(FormView):
    template_name='login.html'
    form_class = AuthenticationForm

    """
    Skrair notenda inn ef lykilord og notendanafn eru rett.
    
    Breytur:
    redirect_to -- urlid a naestu sidu
    """
    def form_valid(self, form):
        redirect_to = '/accounts/loggedin'
        auth_login(self.request, form.get_user())
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
        return HttpResponseRedirect(redirect_to)

    """
    Gefur upp villu ur templateti ef notendanafn og lykilord er rangt.
    """
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    """
    Gefur notanda aukin rettindi ef hann er med thau.
    """
    @method_decorator(sensitive_post_parameters('password'))
    def dispatch(self, request, *args, **kwargs):
        request.session.set_test_cookie()
        return super(Login, self).dispatch(request, *args, **kwargs)

"""
Skrair notanda ut.
"""
class Logout(View):
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return render_to_response('logout.html')

"""
Visar notenda a retta sidu ef lykilord hans er rangt.

Breytur:
template_name -- html snid sidunnar
"""
class Invalid(TemplateView):
    template_name='invalid_login.html'
    def invalid_login(self, request):
        return render_to_response(template_name)

"""
Hjalparadferd med Graf klasanum, hann ma finna i myndraent.py
"""
def graf(request):
    grafid = request.POST.get('graf', '')
    return render_to_response('graf.html',{'grafid':grafid})

"""
Tekur a moti rett innskradum notenda, sendir malsynid a retta klasa og sendir notenda a nidurstodurnar. 

Breytur:
template_name -- html templatetid sem sidan notar
form_class -- hvada form sidan notar, skilgreint i forms.py
"""
class Loggedin(FormView):
    template_name= 'loggedin.html'
    form_class = Malsyniform
    #success_url = '/malsyni/nidurstodur/'

    """
    Skrifar yfir form_valid adferd FormView, til thess ad skila gognunum ur forminu. Vid POST saekir hun gognin ur forminu, sendir a retta klasa og skilar a nidurstodur. 

    Breytur:
    form -- hratt data ur forminu
    hreint -- gogn hreinsud fyrir oryggi
    malsyni -- malsyni barns
    aldur -- aldur barns
    kyn -- kyn barns
    """
    def form_valid(self,form):
        if self.request.method == 'POST':
            form = Malsyniform(self.request.POST)
            if form.is_valid():
                hreint = form.cleaned_data
                malsyni = hreint['malsyni']
                aldur = hreint['aldur']
                kyn = hreint['kyn']

                greining = Greining(malsyni)
                unnid = greining.unnid()

                angiskorda=Angiskorda(unnid)
                listi = angiskorda.angiskorda()
                giskord=Giskord(unnid)
                villulisti = giskord.giskord()
                ordflokkaurv = Ordflokkatolfraedi(listi)
                so, fn, no, ao, uh,fs, lo, st, nutid, thatid, sfn,snn, sthn, sbn, svn,ssn,sgn, fyrstapn,onnurpn,thridjapn=ordflokkaurv.tolfraedi()
                gisk = False
                if len(villulisti)>>0:
                    gisk = True

                villufj = Villur(malsyni)
                villur = villufj.villufjoldi()

                giskflokkun = Giskordaflokkun(villulisti)
                sagnir = giskflokkun.sagnir()
                nafnord = giskflokkun.nafnord()
                lysingar = giskflokkun.lysingar()
                atviks = giskflokkun.atviks()


                setningalisti = malsyni.split('\n')
                tolfr = Tolfraedimalsynis(setningalisti)
                mlsbarn = tolfr.mlsbarn()
                misbord = tolfr.misbord()
                bord = tolfr.bord()

                templates={'aldur': aldur, 'malsyni': malsyni, 'mlsbarn':mlsbarn, 'bord':bord, 'misbord':misbord, 'kyn': kyn, 'unnid': unnid, 'sagnir' : sagnir, 'lysingar': lysingar, 'nafnord': nafnord, 'atviks': atviks, 'villur' : villur, 'villulisti': villulisti,  'gisk':gisk, 'so':so, 'fn':fn, 'no':no, 'ao':ao, 'uh':uh, 'fs':fs, 'lo':lo, 'st':st, 'nutid':nutid, 'thatid':thatid, 'sfn':sfn,'snn':snn, 'sthn':sthn, 'sbn':sbn, 'svn':svn,'ssn':ssn,'sgn':sgn, 'fyrstapn':fyrstapn,'onnurpn':onnurpn,'thridjapn':thridjapn}
                return render_to_response('nidurstodur.html',templates)
    

"""
Ser um ad birta nidurstodur, kodi asamt html-i i templateti

Breytur:
template_name -- nafn html stilsnids
"""
class Nidurstodur(TemplateView):
    template_name='nidurstodur.html'
    def nidurstodur(request):
        return render_to_response(template_name)


"""
Ser um ad birta stjornbord rannsakanda, kodi asamt html-i i templateti

Breytur:
template_name -- nafn html stilsnids
c -- csrf requestid
"""
class Rannsakandastjb(TemplateView):
    template_name='stjornbord.html'

    @user_passes_test(lambda u: u.is_superuser)
    def stjornbord(request):
        c = {}
        c.update(csrf(request))
        return render_to_response(template_name, c)
