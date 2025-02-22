from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
    

def detail(request, question_id):
    return HttpResponse("You're looking at question ")


def results(request, question_id):
    response = "You're looking at the results of question"
    return HttpResponse(response)


def vote(request, question_id):
    return HttpResponse("You're voting on question" )