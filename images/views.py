from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from .forms import UploadFileForm
from .forms import ClassifyFileForm

import datetime
import pathlib
from images.models import Image
from images.models import Tag
import io
import base64

AIEnable = True
if AIEnable:
    from images import MLclassifer

    cl = MLclassifer.MLclassifer()
    cl.classifyPath("images/test.png")


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():

            im = Image()
            im.model_pic = form.cleaned_data['file']

            filename = '{0}{1}'.format(
                str(base64.b64encode(bytes(str(datetime.datetime.now().timestamp()), 'utf-8')))[2:-2],
                pathlib.Path(form.cleaned_data['file'].name).suffix)
            im.model_pic.name = filename

            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

            if x_forwarded_for:
                ipaddress = x_forwarded_for.split(',')[-1].strip()
            else:
                ipaddress = request.META.get('REMOTE_ADDR')

            im.owner = None
            im.upload_ip_address = ipaddress
            im.lease = datetime.datetime.now().replace(microsecond=0) + datetime.timedelta(
                seconds=int(form.cleaned_data['expiration'].split(".")[0]))

            im.name = filename
            if form.cleaned_data['your_name'] == "":
                im.custom_name = None
            else:
                im.custom_name = form.cleaned_data['your_name']

            im.save()

            for tag in request.POST.getlist('tagList'):
                tag = Tag(name=tag.split(":")[0], image=im)
                tag.save()

            return HttpResponseRedirect("/image/view/%s" % filename)
    else:
        form = UploadFileForm()
    return render(request, 'index.html', {'form': form})


def view_file(request, filename):
    fs = FileSystemStorage()
    im = Image.objects.get(name=filename)
    filename = fs.url(im.model_pic.name)
    tags = Tag.objects.filter(image=im)
    return render(request, 'uploaded.html', {
        'file_url': filename,
        'tags': tags,
        'title': im.custom_name
    })


def cleanup(request):
    start = datetime.datetime.fromtimestamp(0)
    end = datetime.datetime.now()
    l = Image.objects.filter(lease__range=[start, end]).all()
    st = "Removed:"
    for im in l:
        st += ('<br>' + im.model_pic.name)
    l.delete()
    return HttpResponse(st)


def classify(request):
    if request.is_ajax():
        form = ClassifyFileForm(request.POST, request.FILES)
        if form.is_valid():
            tags = ["one", "two"]
            if AIEnable:
                img = Image2.open(io.BytesIO(form.cleaned_data['file'].read()))
                x = cl.prepare_image(img)
                tags = cl.classify(x)
        else:
            tags = "Error"
    else:
        tags = "Error"
    return JsonResponse({'tags': tags})
