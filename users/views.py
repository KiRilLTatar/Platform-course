from django.shortcuts import render, redirect
from users.models import User
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.contrib.auth import logout
from users.models import Progress
from courses.models import Couse
from django.contrib.auth.decorators import login_required


# Create your views here.
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        is_teacher = request.POST.get('is_teacher') == 'true'

        errors = []

        if not username or not email or not password or not password2:
            errors.append('Пожалуйста, заполните все поля.')

        if password != password2:
            errors.append('Пароли не совпадают.')

        if User.objects.filter(username=username).exists():
            errors.append('Имя пользователя уже занято.')

        if errors:
            return JsonResponse({'success': False, 'errors': errors})

        user = User(username=username, email=email, is_teacher=is_teacher)
        user.set_password(password)
        user.save()
        login(request, user)

        return JsonResponse({'success': True, 'redirect_url': '/'})

    return JsonResponse({'success': False, 'errors': ['Неверный метод запроса']})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({"success": True, "redirect_url": "/"})  # URL для перенаправления после успешного входа
        else:
            return JsonResponse({"success": False, "error": "Неверный логин или пароль"})

    return JsonResponse({"success": False, "error": "Неверный запрос"})

def logout_view(request):
    logout(request)
    return redirect('home')

def check_username(request):
    username = request.GET.get('username', '')
    exists = User.objects.filter(username=username).exists()
    return JsonResponse({'exists': exists})

@login_required
def profile_info(request):
    return render(request, 'users/info.html')

@login_required
def profile_course(request):
    progresses = Progress.objects.filter(user=request.user)

    course_ids = [p.course_id for p in progresses]

    courses = Couse.objects.filter(id__in=course_ids)
    course_map = {c.id: c for c in courses}

    data = []
    for progress in progresses:
        course = course_map.get(progress.course_id)
        if course:
            data.append({
                'course': course,
                'progress': progress,
            })
    return render(request, 'users/course.html', {'course_data': data})

@login_required
def profile_later_course(request):
    return render(request, 'users/later.html')

@login_required
def profile_statistic(request):
    return render(request, 'users/statistic.html')