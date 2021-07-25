import os
from django.http import HttpResponse
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from . import db_handle

@login_required
def index(request):
	return redirect("/show_items/")

def signup(request):
	if request.user.is_authenticated:
			return redirect("/")
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			# This will go to login_view function
			return redirect("/login/?message=signup_success")
		else:
			# print(form.errors)
			# Extract error code from sign-up form :https://stackoverflow.com/a/41711850/9217577
			error_names,error_descriptions=next(iter(form.errors.items())) 
			print(''.join(error_descriptions)) #I don't know how this works.
			error_descriptions=''.join(error_descriptions)
			# ToDo remove helptext in form
			form = RegisterForm()
			return render(request, "signup.html", {"form":form,'message':error_descriptions})
	else:
		form = RegisterForm()
		return render(request, "signup.html", {"form":form})


# Do not change the name from login_view to login.Because default login() function causes problems .
def login_view(request):
	if request.user.is_authenticated:
			return redirect("/")
	elif request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request,user)
				return redirect("/")
			else:
				return render(request,"login.html",{'message':"Your account was inactive."})
		else:
			print("Someone tried to login and failed.")
			print("They used username: {} and password: {}".format(username,password))
			return render(request,"login.html",{'message':"Wrong username or password"})
	else:
		message = request.GET.get('message', None)
		if message!=None and message=="signup_success":
			return render(request, 'login.html',{'message':'Account created successfully!..Login to continue!'})
		else:
			return render(request, 'login.html')

# Do not change the name from logout_view to logout.Because default logout() function causes problems 
def logout_view(request):
	if request.user.is_authenticated:
		logout(request)
		return render(request,'logout_status.html',{'message':"Logged out successfully"})
	else:
		return render(request,'logout_status.html')

@login_required
def add_item(request):
	if request.method == "POST":
		db_handle.add_item(request.user.id,request.POST.get('item_title'),request.POST.get('item_description'),request.POST.get('item_tag'),request.POST.get('date_to_buy'))
		return redirect("/show_items/?added=true")
	else:
		return render(request,"add_item.html",{})

@login_required
def show_items(request):
	date_to_buy = request.GET.get('date_to_buy', None)
	deleted = request.GET.get('deleted', None)
	updated = request.GET.get('updated', None)
	added = request.GET.get('added', None)
	items = db_handle.show_items(request.user.id,date_to_buy)
	return render(request,"index.html",{"items":items,"deleted":deleted,"updated":updated,"date_to_buy":date_to_buy,"added":added})

@login_required
def update_item(request,item_id=None):
	if not item_id:
		return HttpResponse("No ID was given")
	if request.method == "GET":
		item_details = db_handle.get_item_details(request.user.id,item_id)
		return render(request,"update.html",{"item_details":item_details})
	else:
		db_handle.update_item(request.user.id,item_id,request.POST.get("item_title"),request.POST.get("item_description"),request.POST.get("item_tag"),request.POST.get("date_to_buy"))
		return redirect("/show_items/?updated=true")

@login_required
def delete_item(request,item_id=None):
	if not item_id:
		return HttpResponse("No ID was given")
	db_handle.delete_item(request.user.id,item_id)
	return redirect("/show_items/?deleted=true")

