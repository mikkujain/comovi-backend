from django.shortcuts import render

# Create your views here.

def error404(request, exception):
    return render(request, 'website/404.html', locals())


# def error500(request,):
#     return render(request, 'website/500.html', locals())


