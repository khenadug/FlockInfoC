from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from data_modifier.models import *
from data_modifier.custom_sql import *
from data_modifier.section_type import SectionType
from django.http import Http404

def index(request):
    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}
    return render(request, 'data_modifier/index.html', context=context_dict)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('index'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'data_modifier/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('index'))

@login_required
def navigation(request, section_id=None):

    # Load species if no id is provided
    if not section_id:
        sections = get_species_sections()

    # Load children of current section
    else:
        sections = get_child_sections(section_id)


    context_dict = {}
    context_dict['sections'] = sections
    return render(request, 'data_modifier/navigation.html', context=context_dict)

@login_required
def section_edit(request, section_id=None):

    context_dict = {}
    context_dict['section'] = get_section(section_id)

    return render(request, 'data_modifier/section/edit.html', context=context_dict)