from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from models import *
import json
from django.db.models import F
from PIL import Image, ImageDraw, ImageFont,ImageOps
import StringIO
from django.core.files.base import File,ContentFile
import base64
from django.core.files.uploadedfile import InMemoryUploadedFile
# Create your views here.
import os
from django.core.context_processors import csrf

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def check_if_already_upvoted(user, bid):
    userprofile = UserProfile.objects.filter(user=user).first()
    bid = int(bid)
    for board in userprofile.upvoted_boards.all():
        if bid == board.id:
            return True
    return False


def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/board/')
    return render(request, 'website/home.html')


def show_billboard(request, bid=False):
    if request.user.is_authenticated():
        if request.method == 'POST':
            if 'message' in request.POST:
                try:
                    message = request.POST.get('message')
                    message = '"' + message + '"'
                    user = request.user
                    sign = request.user.first_name + ' ' + request.user.last_name
                    board = Billboard.objects.create(user=user, message=message, sign=sign)
                    ## Normal Image
                    image = generate_image(message, sign)
                    tempfile_io =StringIO.StringIO()
                    image.save(tempfile_io, format='PNG')
                    image_file = InMemoryUploadedFile(tempfile_io, None, 'test_new.png','image/png',tempfile_io.len, None)
                    board.image.save('test_new.png', image_file)
                    board.save()
                    ## Thumbnail Image
                    tempfile_io =StringIO.StringIO()
                    thumbnail_image = thumbnail(board.image.url)
                    thumbnail_image.save(tempfile_io, format='PNG')
                    thumbnail_image_file = InMemoryUploadedFile(tempfile_io, None, 'thumb_new.png','image/png',tempfile_io.len, None)
                    board.thumbnail_image.save('thumb_new.png', thumbnail_image_file)
                    board.save()

                    return HttpResponse(json.dumps({'status': 'success', 'message': 'Board created successfully', 'board_id': board.id, 'created':'true'}))
                except Exception as e:
                    return HttpResponse(json.dumps({'status': 'failure', 'message': '[Error] ' + str(e)}))
            if 'upvote' in request.POST:
                if not check_if_already_upvoted(request.user, request.POST['bid']):
                    userprofile = UserProfile.objects.filter(user=request.user).first()
                    userprofile.upvoted_boards.add(Billboard.objects.get(id=request.POST['bid']))
                    userprofile.save()
                    Billboard.objects.filter(id=request.POST['bid']).update(upvotes=F('upvotes') + 1)
                    return HttpResponse(json.dumps({'status': 'success', 'upvote': '+1', 'board_id':request.POST['bid']}))
                else:
                    userprofile = UserProfile.objects.filter(user=request.user).first()
                    userprofile.upvoted_boards.remove(Billboard.objects.get(id=request.POST['bid']))
                    userprofile.save()
                    Billboard.objects.filter(id=request.POST['bid']).update(upvotes=F('upvotes') - 1)
                    return HttpResponse(json.dumps({'status': 'success', 'upvote': '-1', 'board_id':request.POST['bid']}))
                return HttpResponse(json.dumps({'status': 'failed', 'message': 'Upvote Not Updated'}))
        more_boards = Billboard.objects.filter().select_related('user').exclude(user=request.user)[:3]
        authenticated = request.user.is_authenticated()
        user = UserProfile.objects.filter(user= request.user).first()

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
            return render(request, 'website/billboard.html', {'more_boards': more_boards, 'board': board, 'authenticated': authenticated, 'upvoted': upvoted, 'user': user})
        board = Billboard.objects.filter(user=request.user).first()
        return render(request, 'website/billboard.html', {'more_boards': more_boards, 'board': board, 'authenticated': authenticated, 'upvoted': upvoted, 'user': user})
    else:
        return HttpResponseRedirect('/')



#message = '"You know why? Because I am Batman and you are meghaaa! Pranav ja so ja be kab tak jagega!!"'
#name = '-Parth Choudhary'


def generate_image(message, name):
    base = Image.open('/home/kartikey/Desktop/billboard/static/img/template.png').convert('RGBA')

    txt = Image.new('RGBA', base.size, (255,255,255,0))

    # get a font
    fnt = ImageFont.truetype('/home/kartikey/Desktop/Roboto-Medium.ttf', 38)
    nfnt = ImageFont.truetype('/home/kartikey/Desktop/Roboto-Medium.ttf', 28)
    # get a drawing context
    d = ImageDraw.Draw(txt)
    if d.multiline_textsize(message, font=fnt)[0] > 1059:
        print len(message)
        nm = message.split()
        nm.insert(len(nm)/2, '\n')
        space = " "
        message = space.join(nm)
    d.multiline_text((240, 130), message, font=fnt, fill=(255, 255, 255, 255), align='left')
    d.text((255, 250), name, font=nfnt, fill=(255, 255, 255, 255))
    out = Image.alpha_composite(base, txt)
    return out


def explore_more(request):
    if request.user.is_authenticated():
            if request.method == 'POST':
                if 'upvote' in request.POST:
                    if not check_if_already_upvoted(request.user, request.POST['bid']):
                        userprofile = UserProfile.objects.filter(user=request.user).first()
                        userprofile.upvoted_boards.add(Billboard.objects.get(id=request.POST['bid']))
                        userprofile.save()
                        Billboard.objects.filter(id=request.POST['bid']).update(upvotes=F('upvotes') + 1)
                        return HttpResponse(json.dumps({'status': 'success', 'upvote': '+1', 'board_id':request.POST['bid']}))
                    else:
                        userprofile = UserProfile.objects.filter(user=request.user).first()
                        userprofile.upvoted_boards.remove(Billboard.objects.get(id=request.POST['bid']))
                        userprofile.save()
                        Billboard.objects.filter(id=request.POST['bid']).update(upvotes=F('upvotes') - 1)
                        return HttpResponse(json.dumps({'status': 'success', 'upvote': '-1', 'board_id':request.POST['bid']}))
                    return HttpResponse(json.dumps({'status': 'failed', 'message': 'Upvote Not Updated'}))
            boards = Billboard.objects.filter().select_related('user').exclude(user=request.user)
            return render(request, 'website/explore.html', {'boards': boards})
    else:
        return HttpResponseRedirect('/')

def thumbnail(image_list):
    print image_list, 'm in'
    size = (400, 400)
    image = Image.open(BASE_DIR + image_list)
    image.thumbnail(size, Image.ANTIALIAS)
    background = Image.new('RGBA', size, (255, 255, 255, 0))
    background.paste(
        image,
        ((size[0] - image.size[0]) / 2, (size[1] - image.size[1]) / 2))
    return background
