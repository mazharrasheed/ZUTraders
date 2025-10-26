

from django.shortcuts import render
from home.models import UnderConstruction
from decouple import config


class UnderConstructionMiddleWare():

    def __init__(self, get_response):
        self.get_respose=get_response

    def __call__(self,request):

        if request.user.is_superuser:
            print("under construction super user")
            key=config("MAINTENANCE_BYPASS_KEY")
            print("Key",key)
            return self.get_respose(request)
        #  imported from .env file to hide our secret key using decouple config
        uc_key=config("MAINTENANCE_BYPASS_KEY")

        if "u" in request.GET and request.GET["u"]==uc_key:
            request.session['bypass_maintenance']=True
            request.session.set_expiry(0)
            
        if request.session.get('bypass_maintenance',False):
            print("under construction session")
            return self.get_respose(request)
        try:
            uc=UnderConstruction.objects.first()
            if uc and uc.is_under_construction:
                data={
                    'uc_note':uc.uc_note,
                    'uc_duration':uc.uc_duration
                }
                print("under construction uc")
                return render(request,'under_construction.html',data)
            pass
        except:
            pass
        print("under construction")
        return self.get_respose(request)

