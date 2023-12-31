from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

def auth_admin(func):
    def wrapper(request, *args, **kwargs):
        if 'admin' in request.session:
            return func(request, *args, **kwargs)
        else:
            return redirect('home_bake:customer_home')
            
    return wrapper


 
