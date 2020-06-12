from django.http import HttpResponse


def grading_queue(request):
    return HttpResponse("This is de Grading Queue")


def dedup_queue(request):
    return HttpResponse("This is the De-duplication Queue")