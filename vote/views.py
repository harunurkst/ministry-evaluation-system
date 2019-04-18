from django.shortcuts import render, redirect
from .forms import MinistrySelectForm
from .models import Ministry, Question, VoteCast


def get_ministry(request):
    forms = MinistrySelectForm()
    if request.method == 'POST':
        ministry = request.POST['ministry']
        request.session['ministry'] = ministry
        return redirect('cast-vote')
    return render(request, 'get_ministry.html', {'forms': forms})


def cast_vote(request):
    if 'ministry' in request.session:
        ministry_id = request.session['ministry']
        min_obj = Ministry.objects.get(pk=ministry_id)
        questions = Question.objects.filter(ministry=min_obj)
        if request.method == 'POST':
            post_data = dict(request.POST)
            del post_data['csrfmiddlewaretoken']
            total_score = 0
            print(post_data.items())
            for key, value in post_data.items():
                total_score += int(value[0])
            vote = VoteCast.objects.create(
                voter=request.user,
                ministry_id=ministry_id,
                score = total_score
            )
            print(vote)
        return render(request, 'cast_vote.html', {'questions': questions})
    else:
        return redirect('get-ministry')