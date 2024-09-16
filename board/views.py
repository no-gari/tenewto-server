from django.views.decorators.csrf import csrf_exempt
from .forms import ApplyForm, CheckArtForm
from django.shortcuts import render
from .models import Application, ApplyAvailable


@csrf_exempt
def info(request):
    result = None
    if request.method == 'POST':
        form = CheckArtForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            # Check if an art entry exists for the given name and phone number
            art_exists = Application.objects.filter(name=name, phone=phone).exists()

            # Set the result message based on whether the art exists
            if art_exists:
                result = f"'{name}'님의 작품이 잘 제출되었습니다."
            else:
                result = f"'{name}'님의 작품이 존재하지 않습니다."
    else:
        form = CheckArtForm()

    return render(request, 'info.html', {'form': form, 'result': result})


@csrf_exempt
def apply(request):
    if request.method == 'POST':
        form = ApplyForm(request.POST, request.FILES)
        if form.is_valid():
            obj = Application()
            obj.name = form.cleaned_data['name']
            obj.phone = form.cleaned_data['phone']
            obj.birthday = form.cleaned_data['birthday']
            obj.email = form.cleaned_data['email']
            obj.art_name = form.cleaned_data['art_name']
            obj.when = form.cleaned_data['when']
            obj.where = form.cleaned_data['where']
            obj.explanation = form.cleaned_data['explanation']
            obj.fixed = form.cleaned_data['fixed']
            obj.image1 = form.cleaned_data.get('image1')
            obj.image2 = form.cleaned_data['image2']
            obj.image3 = form.cleaned_data['image3']
            obj.image4 = form.cleaned_data['image4']
            obj.image5 = form.cleaned_data['image5']
            obj.save()
            return render(request, 'success.html', {'form': form})
    else:
        form = ApplyForm()
        apply_available = ApplyAvailable.objects.first()
        available = apply_available.available if apply_available else False
        new_context = {
            'available': available
        }
        return render(request, 'apply.html', {'form': form, **new_context})
    return render(request, 'apply.html', {'form': form})
