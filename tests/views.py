from django.shortcuts import render, redirect
from tests.models import Test, Question, AnswerOption
from tests.forms import TestForm, QuestionForm, AnswerOptionForm
from courses.models import Module
from django.contrib.auth.decorators import login_required   
from django.shortcuts import get_object_or_404


# Create your views here.
@login_required
def add_test(request, module_id):
    module = get_object_or_404(Module, id=module_id)

    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.module = module
            test.save()
            return redirect('courses:edit_course', course_id=module.course.id)
    else:
        form = TestForm()

    return render(request, 'tests/add_test.html', {
        'form': form,
        'module': module
    })

@login_required
def add_question(request, test_id):
    test = get_object_or_404(Test, id=test_id, module__course__author=request.user)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.test = test
            question.save()
            return redirect('tests:edit_test', test_id=test.id)
    else:
        form = QuestionForm()

    return render(request, 'tests/add_question.html', {
        'form': form,
        'test': test
    })

@login_required
def add_answer_option(request, question_id):
    question = get_object_or_404(Question, id=question_id, test__module__course__author=request.user)

    if request.method == 'POST':
        form = AnswerOptionForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.save()
            return redirect('tests:edit_test', test_id=question.test.id)
    else:
        form = AnswerOptionForm()

    return render(request, 'tests/add_answer_option.html', {
        'form': form,
        'question': question
    })

@login_required
def edit_question(request, question_id):
    question = get_object_or_404(Question, id=question_id, test__module__course__author=request.user)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('tests:edit_test', test_id=question.test.id)
    else:
        form = QuestionForm(instance=question)
    return render(request, 'tests/edit_question.html', {
        'form': form,
        'question': question
    })

@login_required
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id, test__module__course__author=request.user)
    test_id = question.test.id
    if request.method == 'POST':
        question.delete()
        return redirect('tests:edit_test', test_id=test_id)
    return render(request, 'courses/delete_confirm.html', {
        'object': question,
        'cancel_url': 'tests:edit_test',
        'cancel_args': [test_id],
    })


@login_required
def edit_answer_option(request, answer_id):
    answer = get_object_or_404(AnswerOption, id=answer_id, question__test__module__course__author=request.user)
    if request.method == 'POST':
        form = AnswerOptionForm(request.POST, instance=answer)
        if form.is_valid():
            form.save()
            return redirect('tests:edit_test', test_id=answer.question.test.id)
    else:
        form = AnswerOptionForm(instance=answer)
    return render(request, 'tests/edit_answer_option.html', {
        'form': form,
        'answer': answer
    })


@login_required
def delete_answer_option(request, answer_id):
    answer = get_object_or_404(AnswerOption, id=answer_id, question__test__module__course__author=request.user)
    test_id = answer.question.test.id
    if request.method == 'POST':
        answer.delete()
        return redirect('tests:edit_test', test_id=test_id)
    return render(request, 'courses/delete_confirm.html', {
        'object': answer,
        'cancel_url': 'tests:edit_test',
        'cancel_args': [test_id],
    })

@login_required
def edit_test(request, test_id):
    test = get_object_or_404(Test, id=test_id, module__course__author=request.user)
    return render(request, 'tests/edit_test.html', {'test': test})

@login_required
def delete_test(request, test_id):
    test = get_object_or_404(Test, id=test_id, module__course__author=request.user)
    course_id = test.module.course.id

    if request.method == 'POST':
        test.delete()
        return redirect('courses:edit_course', course_id=course_id)

    return render(request, 'courses/delete_confirm.html', {
        'object': test,
        'cancel_url': 'tests:edit_test',
        'cancel_args': [test.id],
    })
