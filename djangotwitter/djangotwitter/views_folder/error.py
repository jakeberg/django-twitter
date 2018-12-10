from django.shortcuts import render


def error_view(request):

    html = "error.html"

    return render(request, html)
