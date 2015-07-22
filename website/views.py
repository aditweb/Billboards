from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from models import *
import json
from django.db.models import F
# Create your views here.


def check_if_already_upvoted(user, bid):
    userprofile = UserProfile.objects.filter(user=user).first()
    for board in userprofile.upvoted_boards.all():
        if bid == board.id:
            return True
    return False


def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/board/')
    return render(request, 'website/home.html')


def show_billboard(request, bid=False):
    if request.method == 'POST':
        if 'message' in request.POST:
            try:
                message = request.POST.get('message')
                user = request.user
                sign = request.user.first_name + ' ' + request.user.last_name
                board = Billboard.objects.create(user=user, message=message, sign=sign)
                return HttpResponse(json.dumps({'status': 'success', 'message': 'Board created successfully', 'board_id': board.id}))
            except Exception as e:
                return HttpResponse(json.dumps({'status': 'failure', 'message': '[Error] ' + e}))
        if 'upvote' in request.POST:
            if not check_if_already_upvoted(request.user, request.POST['bid']):
                userprofile = UserProfile.objects.filter(user=request.user).first()
                userprofile.upvoted_boards.add(Billboard.objects.get(id=request.POST['bid']))
                userprofile.save()
                Billboard.objects.filter(id=request.POST['bid']).update(upvotes=F('upvotes') + 1)
    more_boards = Billboard.objects.filter().select_related('user')
    authenticated = request.user.is_authenticated()
    upvoted = False
    if authenticated:
        if bid:
            upvoted = check_if_already_upvoted(request.user, bid)
        else:
            board = Billboard.objects.filter(user=request.user).first()
            upvoted = check_if_already_upvoted(request.user, board.id)
    if bid:
        board = Billboard.objects.filter(id=bid).first()
        return render(request, 'website/billboard.html', {'more_boards': more_boards, 'board': board, 'authenticated': authenticated, 'upvoted': upvoted})
    board = Billboard.objects.filter(user=request.user).first()
    return render(request, 'website/billboard.html', {'more_boards': more_boards, 'board': board, 'authenticated': authenticated, 'upvoted': upvoted})