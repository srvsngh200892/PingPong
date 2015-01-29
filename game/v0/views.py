import json
from v0.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from v0.config import PLAYER_DETAILS
from v0.models import GameDetail, UserProfile





# from .models import task,PRIORITY_CHOICES,STATUS_CHOICES
# from todo.utils import get_list_from_set, get_data_dict

def auth_login(request):
    if request.method == 'GET':
        return render(request, 'v0/registration/login.html')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                user_profile = UserProfile.objects.get(user=request.user)
                if user_profile.role == 'refree':
                    return HttpResponseRedirect('/home')
                else:
                    return HttpResponseRedirect('/game')
                       
    return HttpResponseRedirect(request.path_info+'?auth_error=true')


def user_logout(request):
    if request.method == 'GET':
        logout(request)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseBadRequest()
    return HttpResponseBadRequest('Not Allowed')
 
@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
    'form': form
    })
 
    return render_to_response(
    'v0/registration/register.html',
    variables,
    )
def register_success(request):
    return render_to_response(
    'v0/registration/success.html',
)
    
@login_required
def home(request):
    user_profile = UserProfile.objects.get(user=request.user)
    current_user_role = user_profile.role
    if current_user_role == 'refree':
        user_obj = GameDetail.objects.all()

    return render(request,
    'v0/home.html',
    { 'user': request.user,'users':user_obj, 'current_user_role':current_user_role}
    )

def game(request):
    user_profile = UserProfile.objects.get(user=request.user)
    game_data = GameDetail.objects.filter(user=user_profile)
    game_data = game_data[len(game_data) - 1]
    if game_data.game_role == 'attacker':
        opponent_data =  GameDetail.objects.get(game_id = game_data.game_id, game_role='defender')
    else:
        opponent_data =  GameDetail.objects.get(game_id = game_data.game_id, game_role='attacker')
      
            
    return render(request,
        'v0/game.html',
        { 'current_user': request.user,'user':game_data, 'opponent_data': opponent_data, 'current_user_role':user_profile.role, 'array_len':PLAYER_DETAILS[request.user.username]}
        )


@login_required
def attacker_game(request, gm_id):
    user_profile = UserProfile.objects.get(user=request.user)
    game_data = GameDetail.objects.get(user=user_profile, game_id= gm_id)
    if request.method=='POST':
       if game_data.result<5: 
           dvalue =  request.POST['value']
           game_data.dvalue = dvalue
           game_data.status = "Joined"
           game_data.save()
           message = 'Your Played wait for result'
       else:
            message = 'Your are out of game now'
               
    data =  {'status': True, 'message': message}
    return HttpResponse(content=json.dumps(data),
                                content_type='application/json')

@login_required
def defender_game(request, gm_id):
    user_profile = UserProfile.objects.get(user=request.user)
    defender_game_data = GameDetail.objects.get(user=user_profile, game_id= gm_id)
    if request.method=='POST':
       array =  request.POST['darray']
       value_array = array.split(',')
       value_array = [int(i) for i in value_array]
       attacker_game_data = GameDetail.objects.get(game_id= gm_id, status='Joined', game_role='attacker')
       if attacker_game_data.dvalue in value_array and defender_game_data.result <5:
          point=int(defender_game_data.result)+1
          defender_game_data.result = point
          defender_game_data.game_role = 'attacker'
          attacker_game_data.game_role = 'defender'
          attacker_game_data.status = ''
          defender_game_data.save()
          attacker_game_data.save()
          message = 'You Got 1 point'
       elif attacker_game_data.result <5 :
          point=int(attacker_game_data.result)+1
          attacker_game_data.result = point
          attacker_game_data.save()
          message = 'Your Opponnent got 1 point'
       if defender_game_data.result == 5:
          defender_game_data.game_result = 'winner'
          defender_game_data.save()
          attacker_game_data.game_result = 'losser'
          attacker_game_data.save()
          message = 'You Won this rounf'

       elif attacker_game_data.result == 5:
           defender_game_data.game_result = 'losser'
           defender_game_data.save()
           attacker_game_data.game_result = 'winner'
           attacker_game_data.save()
           message = 'Your Opponnent Won  this round'
              
          
    data = {'status': True, 'message': message}
    return HttpResponse(content=json.dumps(data),
                                content_type='application/json')      
  		
