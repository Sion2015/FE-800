from django.shortcuts import render



def questionnaire(request):


    context = {

    }

    return render(request, 'questionnaire/questionnaire.html', context)
