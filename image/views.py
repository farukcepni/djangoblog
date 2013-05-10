from django.shortcuts import render, redirect
from image.forms import ImageForm
from image.models import Image
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    if request.POST:
        image_form = ImageForm(request.POST, request.FILES)
        if image_form.is_valid() and image_form.is_valid_image():
            image = Image()
            image.image = image_form.cleaned_data['image']
            image.filename = image_form.cleaned_data['image'].name
            image.user_id = request.user.id
            image.save()
    else:
        image_form = ImageForm()

    images = Image.objects.filter(user_id=request.user.id)
    return render(request, 'image/index.html', {'image_form': image_form,
                                                'images': images})

@login_required
def delete(request, image_id):
    try:
        image = Image.objects.get(id=image_id)
    except:
        pass
    else:
        image.delete()
    return redirect('image_index')