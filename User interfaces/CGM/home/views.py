from django.shortcuts import render
from django.utils.safestring import mark_safe


def home(request):
    key_features_1 = "Our Switch Back strategy systematically finds embedded capital losses to lower investment taxes" \
                     " and increase after-tax returns."
    key_features_2 = "CGM has no hidden fees, no trade requirements to access advanced features, and requires very " \
                     "small opening deposit minimums. "
    key_features_3 = "With CGM, choosing the right portfolio is easy, no matter your level of experience. We'll " \
                     "recommend a customized allocation to you based on your risk profile."
    key_features_4 = "CGM maintains portfolios that closely tracks the investor's strategic asset allocation while " \
                     "generally preventing too frequently buy and sell which cause extra taxes and expenses."



    context = {
        "key_features_1": mark_safe(key_features_1),
        "key_features_2": mark_safe(key_features_2),
        "key_features_3": mark_safe(key_features_3),
        "key_features_4": mark_safe(key_features_4),



    }

    return render(request, 'home/home.html', context)