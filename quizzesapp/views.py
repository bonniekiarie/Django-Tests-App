from itertools import count
from django.shortcuts import redirect, render
from .models import Test, Question, Choice, Scores
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .forms import TestForm

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password= raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
        return render(request, 'registration/signup.html', {'form':form})

def home_view(request):   
    if request.method == "POST":
        test = list(request.POST.items())[1][1]
        scores = Scores.objects.filter(student = request.user)
        print(scores)
        scores_list = []
        score_list = []
        for iscore in scores:
            tests = Test.objects.all()[iscore.test]
            score_list = [tests.subject, float(iscore.score)]
            scores_list.append(score_list)
        # request.session['scores_list'] = scores_list
        test_subject = Test.objects.all()[int(test)]
        request.session['test_subject'] = int(test)
        questions = Question.objects.all().filter(test=test_subject)
        request.session['number_of_questions'] = len(questions)
        test_subject = test_subject.subject
        questions_list = []
        for question in questions:
            question_list = []
            question_list.append(question.question)
            choices = Choice.objects.filter(question = question)
            for choice in choices:
                question_list.append(choice.choice)
            questions_list.append(question_list)
        return render(request, 'test_view.html', {'previous_tests':scores_list, 'test_subject':test_subject, 'questions':questions_list})
    else:
        test_form = TestForm()
        tests = Test.objects.all()
        count = 0
        choices = []
        for test in tests:
            choice = [str(count), test.subject]
            choices.append(choice)
            count += 1
        return render(request, 'home_view.html', {'tests':choices})
    
@login_required(redirect_field_name = 'accounts/login')
def score_view(request):
    if request.method == "POST":
        test = list(request.POST.items())[1:]
        test_subject = request.session['test_subject']
        test_subject = Test.objects.all()[test_subject]
        questions = Question.objects.all().filter(test=test_subject)
        test_score = 0
        number_of_questions = request.session['number_of_questions']
        count = 0
        correct_questions = []
        for question, answer in test:
            current_question = Question.objects.filter(test= test_subject)[int(question)]
            choice = Choice.objects.filter(question=current_question)[int(answer)]
            if choice.is_correct:
                test_score += 1
                correct_questions.append(count)
            count += 1
        total_score = (test_score / number_of_questions) * float(test_subject.maximum_score)
        total_score = round(total_score, 2)
        score = Scores.objects.create(student = request.user, test = request.session['test_subject'], score = total_score)
        score.save()
        questions_list = []
        count = 0
        # for question in questions:
        #     question_list = []
        #     question_list.append(question.question)
        #     choices = Choice.objects.filter(question = question, is_correct = True)
        #     for choice in choices:
        #         question_list.append(choice.choice)
        #     if count not in correct_questions:
        #         questions_list.append(question_list)
        #     count += 1
        # scores_list = request.session['scores_list']
        
        return render(request, 'score.html', {'score':total_score, 'questions':questions_list})
