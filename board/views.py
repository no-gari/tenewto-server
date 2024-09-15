from django.shortcuts import render
from .forms import ApplyForm

def home_view(request):
    return render(request, 'home.html')


def info(request):
    return render(request, 'info.html')


def apply(request):
    if request.method == 'POST':
        form = ApplyForm(request.POST, request.FILES)
        if form.is_valid():
            return render(request, 'success.html', {'form': form})
    else:
        form = ApplyForm()

    return render(request, 'apply.html', {'form': form})


def check(request):
    return render(request, 'check.html')


def community(request):
    return render(request, 'community.html')

