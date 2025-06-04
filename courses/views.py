from django.shortcuts import render, redirect
from courses.models import Couse, Material, Module, Lesson
from users.models import Progress
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .forms import CourseForm, ModuleForm, LessonForm, MaterialForm


# Create your views here.
def course_list(request):
    courses = Couse.objects.all()
    material = Material.objects.all()
    return render(request, 'courses/list_course.html', {'courses': courses, 'material': material})

def course_detail(request, course_id):
    try:
        user = request.user
        courses = Couse.objects.get(id=course_id)
        material = Material.objects.all()
        modules = courses.modules.all()
        is_enrolled = Progress.objects.filter(user=user, course_id=course_id).exists()
    except Couse.DoesNotExist:
        return render(
                request, 
                'courses/detail_course.html', 
                {'error': 'Курс не найден!'},
                status=404
            )
    
    return render(request, 'courses/detail_course.html', {'courses': courses, 'modules': modules, 'material': material, 'is_enrolled': is_enrolled,})


@login_required
def add_course(request, course_id):
    course = get_object_or_404(Couse, id=course_id)
    
    if not Progress.objects.filter(user=request.user, course_id=course.id).exists():  
        Progress.objects.create(
            user=request.user,
            course_id=course.id,
            comleted_modules=[],
            last_accessed=timezone.now,
        ) 
        messages.success(request, f'Вы записались на курс "{course.title}"') 
    else:
        messages.warning(request, f'Вы уже записаны на курс "{course.title}"') 
    
    return redirect('courses:course_detail', course_id=course.id)   

@login_required
def remove_course(request, course_id):
    progress = get_object_or_404(Progress, user=request.user, course_id=course_id)
    progress.delete()
    messages.success(request, "Вы успешно покинули курс.")
    return redirect('courses:course_detail', course_id=course_id)


@login_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.author = request.user
            course.save()
            return redirect('courses:manage_course') 
    else:
        form = CourseForm()
    return render(request, 'courses/create_course.html', {'form': form})


@login_required
def manage_course(request):
    courses = Couse.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'courses/manage_course.html', {'courses': courses})

@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Couse, id=course_id, author=request.user)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('courses:edit_course', course_id=course.id)
    else:
        form = CourseForm(instance=course)

    return render(request, 'courses/edit_course.html', {
        'form': form,
        'course': course
    })

@login_required
def add_module(request, course_id):
    course = get_object_or_404(Couse, id=course_id, author=request.user)

    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            module = form.save(commit=False)
            module.course = course
            module.save()
            return redirect('courses:edit_course', course_id = course.id)
    else:
        form = ModuleForm()

    return render(request, 'courses/add_module.html', {
        'form':form,
        'course': course
    })

@login_required
def add_lesson(request, module_id):
    module = get_object_or_404(Module, id=module_id)

    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.module = module
            lesson.save()
            return redirect('courses:edit_course', course_id = module.course.id)
    else:
        form = LessonForm()

    return render(request, 'courses/add_lesson.html', {
        'form': form,
        'module': module
    })

@login_required
def edit_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course__author=request.user)
    materials = lesson.materials.all()

    if request.method == 'POST':
        lesson_form = LessonForm(request.POST, instance=lesson)
        material_form = MaterialForm(request.POST, request.FILES)
        if 'save_lesson' in request.POST and lesson_form.is_valid():
            lesson_form.save()
            return redirect('courses:edit_lesson', lesson_id=lesson.id)
        elif 'add_material' in request.POST and material_form.is_valid():
            material = material_form.save(commit=False)
            material.lesson = lesson
            material.save()
            return redirect('courses:edit_lesson', lesson_id=lesson.id)
    else:
        lesson_form = LessonForm(instance=lesson)
        material_form = MaterialForm()

    return render(request, 'courses/edit_lesson.html', {
        'lesson': lesson,
        'lesson_form': lesson_form,
        'material_form': material_form,
        'materials': materials,
    })

@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Couse, id=course_id, author=request.user)
    if request.method == 'POST':
        course.delete()
        return redirect('courses:manage_course')
    return render(request, 'courses/delete_course.html', {'course': course})

@login_required
def delete_module(request, module_id):
    module = get_object_or_404(Module, id=module_id, course__author=request.user)
    course_id = module.course.id
    if request.method == 'POST':
        module.delete()
        return redirect('courses:edit_course', course_id=course_id)
    return render(request, 'courses/delete_confirm.html', {
        'object': module,
        'cancel_url': 'courses:edit_course',
        'cancel_args': [course_id],
    })

@login_required
def delete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course__author=request.user)
    course_id = lesson.module.course.id
    if request.method == 'POST':
        lesson.delete()
        return redirect('courses:edit_course', course_id=course_id)
    return render(request, 'courses/delete_confirm.html', {
        'object': lesson,
        'cancel_url': 'courses:edit_course',
        'cancel_args': [course_id],
    })

@login_required
def delete_material(request, material_id):
    material = get_object_or_404(Material, id=material_id, lesson__module__course__author=request.user)
    lesson_id = material.lesson.id
    if request.method == 'POST':
        material.delete()
        return redirect('courses:edit_lesson', lesson_id=lesson_id)
    return render(request, 'courses/delete_confirm.html', {
        'object': material,
        'cancel_url': 'courses:edit_lesson',
        'cancel_args': [lesson_id],
    })

@login_required
def course_detail_progress(request, course_id):
    course = get_object_or_404(Couse, id=course_id)
    modules = course.modules.prefetch_related('lessons')

    progress, _ = Progress.objects.get_or_create(user=request.user, course_id=course.id)
    completed_modules = set(progress.comleted_modules)

    return render(request, 'courses/course_progress.html', {
                      'course': course,
                      'modules': modules,
                      'progress': progress,
                      'completed_modules': completed_modules,
                  })

@login_required
def lesson_detail_progress(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    course = lesson.module.course

    progress, _ = Progress.objects.get_or_create(user=request.user, course_id=course.id)
    modules = course.modules.prefetch_related('lessons')


    all_lessons = Lesson.objects.filter(module__course=course).order_by('module__order', 'order')
    completed_lesson_ids = [
        l.id for m in course.modules.all() if m.id in progress.comleted_modules
        for l in m.lessons.all()
    ]

    allowed_ids = [l.id for l in all_lessons[:len(completed_lesson_ids) + 1]]
    if lesson.id not in allowed_ids:
        messages.warning(request, "Сначала пройдите предыдущие уроки.")
        return redirect('courses:course_progress', course_id=course.id)

    total_modules = course.modules.count()
    progress.update_progress(lesson.module.id, total_modules)

    return render(request, 'courses/lesson_detail.html', {
        'lesson': lesson,
        'modules': modules,
        'completed_lesson_ids': completed_lesson_ids,
        'allowed_ids': allowed_ids,
    })

