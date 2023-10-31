from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect,HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'data_app/index.html')