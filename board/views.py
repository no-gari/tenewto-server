from django.views.decorators.csrf import csrf_exempt
from .forms import ApplyForm, CheckArtForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Application, ApplyAvailable, Board


@csrf_exempt
def info(request):
    result = None
    if request.method == 'POST':
        form = CheckArtForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            art_exists = Application.objects.filter(name=name, phone=phone).exists()

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
            obj.art_name1 = form.cleaned_data['art_name1']
            obj.art_name2 = form.cleaned_data['art_name2']
            obj.art_name3 = form.cleaned_data['art_name3']
            obj.art_name4 = form.cleaned_data['art_name4']
            obj.art_name5 = form.cleaned_data['art_name5']
            obj.application = form.cleaned_data['application']
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


@csrf_exempt
def apply_init(request):
    if request.method == 'POST':
        consent1 = request.POST.get('privacy_agreement1')
        consent2 = request.POST.get('privacy_agreement2')

        if consent1 and consent2:
            # 필수 동의 체크 후 처리 (예: 데이터 저장, 기타 로직)

            # 처리 완료 후 리다이렉트
            return redirect('apply')
    else:
        return render(request, 'apply_init.html')


def board_list(request):
    boards = Board.objects.all().order_by('-datetime')
    return render(request, 'board_list.html', {'boards': boards})


def board_detail(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    return render(request, 'board_detail.html', {'board': board})