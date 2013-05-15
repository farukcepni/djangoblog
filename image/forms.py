from django import forms
from django.utils.translation import ugettext as _
import os
from models import Image


class ImageForm(forms.Form):
    image = forms.FileField(label=_('Select an Image File'),
                            allow_empty_file=False)

    def clean_image(self):
        """
        Check size, ext and type of the uploaded image
        """
        image = self.cleaned_data.get('image')
        ext = os.path.splitext(os.path.basename(image.name))[1][1:]
        if image._size > Image.MAX_SIZE:
            raise forms.ValidationError(_('Max file size: %d MB' %
                                          (Image.MAX_SIZE / 1024**2)))
        if ext not in Image.ALLOWED_EXTS or\
                image.content_type not in Image.ALLOWED_TYPES:
            raise forms.ValidationError(_('The uploaded image is not allowed'))
        return image
