# -*- coding: utf-8 -*-
import os
import shutil
from PIL import Image, ImageDraw, ImageFont
from uuid import uuid4

from django.contrib import messages
from django.shortcuts import render, redirect, render_to_response
from django.views import View
from django.views.generic import TemplateView
from django.http import JsonResponse
from .forms import FileFieldForm


def do_watermark(directory, file, text):
    color = (255, 255, 255, 75)
    font = 'static/font/roboto/Roboto-Bold.ttf'
    filename = 'media/{0}/{1}'.format(directory, str(file))
    im = Image.open(file).convert('RGBA')
    im_watermark = Image.new('RGBA', im.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(im_watermark)
    width, height = im.size
    font = ImageFont.truetype(font, int(height / 20))
    x = width / 6.5
    y = height / 6.2
    draw.text((x, y), text, color, font)
    x = width / 2.5
    y = height / 2
    draw.text((x, y), text, color, font)
    x = width / 1.5
    y = height / 1.2
    draw.text((x, y), text, color, font)
    result_img = Image.alpha_composite(im, im_watermark)
    result_img.convert('RGB').save(filename, 'JPEG')


class HomeView(View):
    def get(self, request, *args, **kwargs):
        # if request.session.get('uuid'):
        #     shutil.rmtree('media/{0}'.format(request.session['uuid']), ignore_errors=True)
        form = FileFieldForm(self.request.POST or None)
        context = {
            'form': form,
        }
        return render(request, 'home.html', context=context)

    def post(self, request, *args, **kwargs):
        form = FileFieldForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            text = form.cleaned_data['text_field']
            files = request.FILES.getlist('file_field')
            if len(files) > 50:
                messages.error(request, 'Вы выбрали больше 50 фото!')
                return redirect('home_view_url', permanent=True)
            directory = str(uuid4())
            os.mkdir('media/{0}'.format(directory))

            for file in files:
                do_watermark(directory, file, text)
            shutil.make_archive(root_dir='media/{0}'.format(directory),
                                format='zip',
                                base_name='media/{0}'.format(directory))
            shutil.move('media/{0}.zip'.format(directory), 'media/{0}/images.zip'.format(directory))
            request.session['uuid'] = directory
            return redirect('link_view_url', permanent=True)


class LinkView(TemplateView):
    template_name = "link.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['uuid'] = self.request.session.get('uuid')
        return context


class GetLinkView(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            context = {
                'directory': request.session.get('uuid'),
            }
            return JsonResponse(context)

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            print(request.POST)
            status = request.POST.get('status')
            print(status)
            if status == 'true':
                shutil.rmtree('media/{0}'.format(request.session['uuid']), ignore_errors=True)
                del request.session['uuid']
                print('DEL')
                return JsonResponse({'data': True})
            else:
                return redirect('home_view_url', permanent=True)

