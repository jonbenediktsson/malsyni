import numpy as np
import matplotlib.pyplot as plt
import django
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

"""
Tekur inn gildi fra koda og teiknar graf.

Breytur:
dbgildi -- medaltol gagnagrunns
stbgildi -- stadalfravik gagnagrunns
malsyni -- tolfraedi malsynis
stbmalsyni -- stadalfravik malsynis (alltaf 0)
sulur -- fjoldi sulna
ylabel -- titill y ass
xlabel -- titill x ass
titill -- titill grafs
xticks -- titlar sulna
"""
class Graf:
    def __init__(self, dbgildi, stbgildi, malsyni, stbmalsyni, sulur, ylabel, xlabel, titill, xticks):
        self.dbgildi = dbgildi
        self.stbgildi = stbgildi
        self.malsyni = malsyni
        self.stbmalsyni = stbmalsyni
        self.sulur = sulur
        self.ylabel = ylabel
        self.xlabel = xlabel
        self.titill = titill
        self.xticks = xticks

    def bord(self):

        n_groups1 = self.sulur
        dbgildi = self.dbgildi
        stddbgildi = self.stbgildi
        malsyni =self.malsyni
        stdmalsyni = self.stdmalsyni
 
        fig, ax = plt.subplots()   
        index = np.arange(n_groups1)
        bar_width = 0.35
        opacity = 0.4
        error_config = {'ecolor': '0.3'}
    
        rects1 = plt.bar(index, dbgildi, bar_width,
         alpha=opacity,
         color='b',
         yerr=stddbgildi,
         error_kw=error_config,
         label=u'Meðaltal')
    
        rects2 = plt.bar(index + bar_width, malsyni, bar_width,
     alpha=opacity,
     color='r',
     yerr=stdmalsyni,
     error_kw=error_config,
     label=u'Málsýni')
    
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.title(self.titill)
        plt.xticks(index + bar_width, (self.xticks))
        plt.legend()

        plt.tight_layout()
        response=django.http.HttpResponse(content_type='image/png')
        plt.savefig(response)
        return response
