import hashlib

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from apps.account.forms import SignUpForm, LogInForm
from apps.account.models import User
from django.contrib.auth import authenticate, login
h = hashlib.sha256()


class SignUp(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'account/signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            validated_data = form.cleaned_data
            user_obj = User(email=validated_data['email'],
                            password=hashlib.sha256(str(validated_data['password']).encode('utf-8'))
                            .hexdigest(),
                            repeat_password=hashlib.sha256(str(validated_data['repeat_password']).encode('utf-8'))
                            .hexdigest())
            user_obj.save()
            return redirect('home')
        return render(request, 'account/signup.html', {'form': form})


class LogIn(View):
    def get(self, request):
        form = LogInForm()
        return render(request, 'account/login.html', {'form': form})

    def post(self, request):
        form = LogInForm(request.POST or None)
        if form.is_valid():
            email_valid = form.cleaned_data.get("email")
            password_valid = form.cleaned_data.get("password")
            user = authenticate(request, email=email_valid, password=password_valid)
            if user != None:
                return redirect("home")
            else:
                request.session['invalid_user'] = 1  # 1 == True
        return render(request, "account/login.html", {"form": form})


def autocomplete(request):
    if 'term' in request.GET:
        qs = User.objects.filter(email__icontains=request.GET.get('term'))
        titles = list()
        for person in qs:
            titles.append(person.email)
        return JsonResponse(titles, safe=False)
    return render(request, 'home.html')
