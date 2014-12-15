from django.shortcuts import render
from django.http import HttpResponse
from authomatic import Authomatic
from authomatic.adapters import DjangoAdapter
from django.utils import simplejson
from django.db import models
from models import Likes
from profiles.models import Profile
import json

from config import CONFIG

authomatic = Authomatic(CONFIG, 'a super secret random string')

def home(request):
    # Create links and OpenID form to the Login handler.
    return render(request, 'fb/edit.html')


def login(request, provider_name):
    # We we need the response object for the adapter.
    response = HttpResponse()
    
    # Start the login procedure.
    result = authomatic.login(DjangoAdapter(request, response), provider_name)
     
    # If there is no result, the login procedure is still pending.
    # Don't write anything to the response if there is no result!
    if result:
        # If there is result, the login procedure is over and we can write to response.
                
        if result.error:
            # Login procedure finished with an error.
            response.write('<h2>Erro: {0}</h2>'.format(result.error.message))
        
        elif result.user:
            # Hooray, we have the user!
            
            # OAuth 2.0 and OAuth 1.0a provide only limited user data on login,
            # We need to update the user to get more info.
            if not (result.user.name and result.user.id):
                result.user.update()
                url = 'https://graph.facebook.com/v2.2/{0}?fields=likes,id&locale=pt_BR'
                url = url.format(result.user.id)
                
                access_response = result.provider.access(url)
                if access_response.status == 200:
                    likes=access_response.data.get('likes').get('data')
                    profile=Profile.objects.get(user=request.user)
                    Likes.objects.filter(profile=profile).delete()
                    for l in likes:
                        category=l.get('category')
                        name=l.get('name')
                        like=Likes(profile=profile,category=category,name=name)
                        like.save()
                    response.write('<script type="text/javascript">window.close()</script>') 
     

    return response

    


