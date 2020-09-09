from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.generic import CreateView
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from app.forms import SignUpForm

class SignUpView(CreateView):
    def post(self, request, *args, **kwargs):

        all_data = request.POST
        form_data = all_data
        img_choice = all_data['user_img']
        del form_data['user_img']

        form = SignUpForm(data=form_data)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, email=email, password=password,icon=icon)
            img_choice = ImageChoice(user=user, image_choice=img_choice)
            img_choice.save()
            login(request, user)
            return redirect('/')
        return render(request, 'app/signup.html', {'form': form})

    def get(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        return render(request, 'app/signup.html', {'form': form})

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user
        return HttpResponseRedirect(self.get_success_url())
