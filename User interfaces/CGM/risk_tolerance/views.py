from django.shortcuts import render
from django.utils.safestring import mark_safe


def risk_tolerance(request):
    q1 = int(request.POST['element_3'])
    q2 = int(request.POST['element_4'])
    q3 = int(request.POST['element_8'])
    q4 = int(request.POST['element_9'])
    q5 = int(request.POST['element_10'])
    q6 = int(request.POST['element_11'])
    q7 = int(request.POST['element_12'])
    score = 42 - (q1+q2+q3+q4+q5+q6+q7)

    if score <= 10:
        result = "Very Conservative"
        level = "1"
    elif score <= 17:
        result = "Conservative"
        level = "2"
    elif score <=24:
        result = "Moderate"
        level = "3"
    elif score <=31:
        result = "Aggressive"
        level = "4"
    else:
        result = "Very Aggressive"
        level = "5"

    display = False


    context = {
        'q1': 6-q1,
        'q2': 6-q2,
        'q3': 6-q3,
        'q4': 6-q4,
        'q5': 6-q5,
        'q6': 6-q6,
        'q7': 6-q7,
        'score': score,
        'result': result,
        'level': mark_safe(level),
        "display": display
    }

    return render(request, 'risk_tolerance/risk_tolerance.html', context)