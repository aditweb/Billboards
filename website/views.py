from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from models import *
import json
from django.db.models import F
from PIL import Image, ImageDraw, ImageFont
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
                image = generate_image(message, sign)
                board = Billboard.objects.create(user=user, message=message, sign=sign, image=image)
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
            if board:
                upvoted = check_if_already_upvoted(request.user, board.id)
    if bid:
        board = Billboard.objects.filter(id=bid).first()
        return render(request, 'website/billboard.html', {'more_boards': more_boards, 'board': board, 'authenticated': authenticated, 'upvoted': upvoted})
    board = Billboard.objects.filter(user=request.user).first()
    return render(request, 'website/billboard.html', {'more_boards': more_boards, 'board': board, 'authenticated': authenticated, 'upvoted': upvoted})



#message = '"You know why? Because I am Batman and you are meghaaa! Pranav ja so ja be kab tak jagega!!"'
#name = '-Parth Choudhary'


def generate_image(message, name):
    base = Image.open('/home/parth/Downloads/Billboard template.png').convert('RGBA')

    txt = Image.new('RGBA', base.size, (255,255,255,0))

    # get a font
    fnt = ImageFont.truetype('/home/parth/Roboto-Medium.ttf', 38)
    nfnt = ImageFont.truetype('/home/parth/Roboto-Medium.ttf', 28)
    # get a drawing context
    d = ImageDraw.Draw(txt)

    if d.multiline_textsize(message, font=fnt)[0] > 1059:
        print len(message)
        nm = message.split()
        nm.insert(len(nm)/2, '\n')
        space = " "
        message = space.join(nm)

    d.multiline_text((170, 320), message, font=fnt, fill=(255, 255, 255, 255), align='center')
    d.text((990, 420), name, font=nfnt, fill=(255, 255, 255, 255))
    out = Image.alpha_composite(base, txt)

    return out