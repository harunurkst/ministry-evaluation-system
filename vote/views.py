from datetime import datetime 
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Sum
from .forms import MinistrySelectForm, VoteReportForm
from .models import Ministry, Question, VoteCast, QuestionChoice, Area
from nid.models import NidInfo, PhoneList


def get_ministry(request):
    forms = MinistrySelectForm()
    if request.method == 'POST':
        ministry = request.POST['ministry']
        
        current_year = datetime.now().year
        voter_mobile = request.session["user"]
        print(voter_mobile)
        voter_obj = PhoneList.objects.get(mobile_number=voter_mobile)
        print(voter_obj.nid)
        if VoteCast.objects.filter(date__year=current_year, voter=voter_obj.nid, ministry_id=ministry).exists():
            return render(request, 'get_ministry.html', {'forms': forms, 'errMsg': 'You already voted this ministry'})

        request.session['ministry'] = ministry
        return redirect('cast-vote')
    return render(request, 'get_ministry.html', {'forms': forms})


def cast_vote(request):
    if 'ministry' in request.session:
        ministry_id = request.session['ministry']
        min_obj = Ministry.objects.get(pk=ministry_id)
        questions = Question.objects.filter(ministry=min_obj)
        choices = QuestionChoice.objects.all()
        if request.method == 'POST':
            post_data = dict(request.POST)
            del post_data['csrfmiddlewaretoken']
            total_score = 0
            print(post_data.items())
            for key, value in post_data.items():
                total_score += int(value[0])

            voter_mobile = request.session["user"]
            try:
                voter_obj = PhoneList.objects.get(mobile_number=voter_mobile)
                area_code = voter_obj.nid.nid_number[:2]
                area_obj = Area.objects.get(area_code=area_code)
                vote = VoteCast.objects.create(
                    voter=voter_obj.nid,
                    area=area_obj,
                    ministry_id=ministry_id,
                    score=total_score
                )
                return redirect('home')
            except Exception as e:
                context = {'questions': questions, 'choices': choices, 'errMsg': str(e)}
                return render(request, 'cast_vote.html', context)

        context = {'questions': questions, 'choices': choices}
        return render(request, 'cast_vote.html', context)
    else:
        return redirect('get-ministry')


def vote_report(request):
    forms = VoteReportForm()
    if request.method == 'POST':
        forms = VoteReportForm(request.POST)
        if forms.is_valid():
            ministry = forms.cleaned_data["ministry"]
            year = forms.cleaned_data["year"]
            area = forms.cleaned_data["area"]
            votes = VoteCast.objects.filter(date__year=year, ministry_id=ministry)
            if votes:
                if area:
                    votes = votes.filter(area=area)
                total_score = votes.aggregate(total_score=Sum('score'))['total_score']
                total_voter = votes.count()
                average = total_score / total_voter

                context = {'forms': forms, 'score':total_score, 'voter':total_voter, 'average':average}
            else:
                context = {'forms': forms, 'errMsg': 'No Vote report found'}
            return render(request, 'vote/vote_report.html', context)

    context = {'forms': forms}
    return render(request, 'vote/vote_report.html', context)
