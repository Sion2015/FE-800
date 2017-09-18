from django.shortcuts import render

# Create your views here.
def management(request):
    context = {

    }

    return render(request, 'management/step_2.html', context)
