from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from product.models import CommentForm, Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from user.models import UserProfile


def index(request):
    return HttpResponse("Hello wolrd")


def addcomment(request, id):
   url = request.META.get('HTTP_REFERER')  # get last url
   # return HttpResponse(url)
   if request.method == 'POST':  # check post
      form = CommentForm(request.POST)
      if form.is_valid():
        data = Comment()  # create relation with model
        data.name = form.cleaned_data['name']
        data.email = form.cleaned_data['email']
        data.subject = form.cleaned_data['subject']
        data.rate = form.cleaned_data['rate']
        data.comment = form.cleaned_data['comment']
        data.ip = request.META.get('REMOTE_ADDR')
        data.product_id = id
        current_user = request.user
        data.user_id = current_user.id
        if len(data.name) < 3 or len(data.subject) < 5 or len(data.comment) < 5 or len(data.email) < 10:
            messages.error(request, "Please fill the form correctly")
        else:
            data.save()  # save data to table
            messages.success(
                request, "Your review has ben sent. Thank you for your interest")
            return HttpResponseRedirect(url)
   else:
        print("Hello wolrd")

   return HttpResponseRedirect(url)

