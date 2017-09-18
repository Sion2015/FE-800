from django.shortcuts import render
from django.utils.safestring import mark_safe


def home(request):
    text1 = "3 steps to build your financial plan"

    context = {
        'text1': mark_safe(text1),
    }



    return render(request, 'start/start.html', context)