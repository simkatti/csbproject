from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import signupForm, loginForm
from .models import Message
from django.utils.safestring import mark_safe
from django.db import connection

def indexPage(request):
    return render(request, 'index.html')

def loginPage(request):
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Wrong password!'})
    else:
        form = loginForm()
    return render(request, 'login.html', {'form': form})

def signupPage(request):
    if request.method == 'POST':
        form = signupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return render(request, 'signup.html', {'form': form, 'error':'could not create an account'})
    else:
        form = signupForm()
    return render(request, 'signup.html', {'form': form})

#SENSITIVE DATA EXPOSURE in homePage function. Right now it ables the browser to cache the messages
#CROSS SITE SCRIPTING vulnerability in homePage function. Content should not be wrapped in mark_safe function.
@login_required
#@never_cache
@csrf_exempt  #This should not be used
def homePage(request):
    messages = Message.objects.filter(reciever=request.user).order_by('-time')
    #insecure:
    msgs = [{'id': m.id, 'sender': m.sender.username, 'content': mark_safe(m.content), 'time': m.time} for m in messages]
    # secure:
    # msgs = [{'id': m.id, 'sender': m.sender.username, 'content': m.content, 'time': m.time} for m in messages]
    return render(request, 'home.html', {'msgs': msgs})

@login_required
def logoutView(request):
    logout(request)
    return redirect('index')

#BROKEN ACCESS CONTROL in deleteView function. Anyone can delete a message with proper message.id
@login_required
def deleteView(request):
    # if request.method == 'POST':
    #     user = request.user
    m = Message.objects.get(pk=request.POST.get('id'))
        # if user.id == m.reciever.id:
    m.delete()
    return redirect('home')

@login_required
def NewMessage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        content = request.POST.get('content', '').strip()

        if content:
            if User.objects.filter(username=username).exists():
                reciever = User.objects.get(username=username)
                Message.objects.create(sender=request.user, reciever=reciever, content=content)
                return redirect('home')
            else:
                return render(request, 'newmsg.html', {'error': 'User does not exist'})
        else:
            return render(request, 'newmsg.html', {'error': 'Can not send an empty message!'})

        
    return render(request, 'newmsg.html')

#SQL INJECTION in searchMessages function.
@login_required  
def searchMessages(request):
    if request.method == 'POST':
        query = request.POST.get('query', '')
        if query:
        #insecure:
            with connection.cursor() as cursor:
                user = request.user
                response = cursor.execute("SELECT m.id, m.content, m.time, u.username as sender, ur.username as receiver FROM messenger_message m "
                    "JOIN auth_user u ON m.sender_id = u.id "
                    "JOIN auth_user ur ON m.reciever_id = ur.id "
                    "WHERE reciever_id='" + str(user.id) + "' AND content LIKE '%" + query + "%'").fetchall()
                msgs = [{'id': row[0], 'content': row[1], 'time': row[2], 'sender': row[3], 'reciever': row[4]} for row in response]

        #secure:
            # messages_content = Message.objects.filter(reciever=request.user, content__contains=query)
            # messages_sender = Message.objects.filter(reciever=request.user, sender__username__contains=query)
            # messages = list(set(messages_content) | set(messages_sender))
            # msgs = [{'id': m.id, 'sender': m.sender.username, 'content': m.content, 'time': m.time} for m in messages]

            return render(request, 'home.html', {'msgs': msgs})
        else:
            return redirect('home')

        


        


#last flaw leaving DEBUG on in production

#figure out how to and what to push to git
# instructions to how to install etc
# reclone the repo and test if it works
# finish the essay
#submit


