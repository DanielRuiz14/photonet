from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
import webbrowser, flickrapi
from pymongo import MongoClient

# Create your views here.

def inicio(request):
    return render(request, 'inicio.html' )


def crear_publicacion(request):
    # Variables que tenemos en el html: descripcion e imagen
    #  ** Flickr
    api_key = '445296a00d73aa770871ba819090a5b0'
    api_secret = '5706f77136522983'
    user_id= '191718631@N03'


    otro_token ='559-931-719' #** Lo guardo porsiaca

    if request.method == 'POST':
        
        flickr = flickrapi.FlickrAPI(api_key, api_secret)


        # Más info: https://stuvel.eu/flickrapi-doc/3-auth.html
        ##############################################################################
        if not flickr.token_valid(perms='write'):

            # Get a request token
            flickr.get_request_token(oauth_callback='oob')

            # Open a browser at the authentication URL. Do this however
            # you want, as long as the user visits that URL.
            authorize_url = flickr.auth_url(perms='write')
            webbrowser.open_new_tab(authorize_url)

            # Get the verifier code from the user. Do this however you
            # want, as long as the user gives the application the code.
            verifier = str(input('Verifier code: '))

            # Trade the request token for an access token
            flickr.get_access_token(verifier)
        ################################################################################

        # Guardamos la imagen
        
        imagen = request.FILES['imagen']
        resp = flickr.upload(filename=str(imagen), fileobj=imagen.file, format='etree')

         # Sacamos la id de la respuesta del servidor REST
        for elem in resp:
            if(str(elem.tag)=='photoid'):
                photo_id = elem.text

        # Obtenemos la URL consultando el servidor REST 
        for photo in flickr.walk_user(user_id):
            # Estructura de la url por si alguien quiere utilizar algo 
            # https://live.staticflickr.com/{server-id}/{id}_{secret}_{size-suffix}.jpg
            if(photo.get('id') == photo_id):
                url = 'https://live.staticflickr.com/'+photo.get('server')+'/'+photo.get('id')+'_'+photo.get('secret')+'.jpg'
                break       

        # El objeto publicacion

        publicacion = {
            'descripcion' : request.POST['descripcion'], 
            'imagen' : url,
        }
        client = MongoClient('mongodb+srv://dosek:dosek@cluster0.up6fc.mongodb.net/examen?retryWrites=true&w=majority')

        
        print(request.POST['descripcion'])
    return redirect(reverse('inicio'))