from django.forms import forms
from django.utils.translation import ugettext as _


class ImageForm(forms.Form):
    ALLOWED_EXTS = ('jpg', 'png', 'bmp')
    ALLOWED_TYPES = ('image/jpeg', )
    image = forms.FileField(label=_('Select a file'), allow_empty_file=False)

    def is_valid_image(self):
        error_message = _('The uploaded file is not allowed')
        ext = self.cleaned_data['image'].name[-3:]
        file_type = self.cleaned_data['image'].content_type
        if ext in self.ALLOWED_EXTS and file_type in self.ALLOWED_TYPES:
            return True
        else:
            self._errors['type_error'] = self.error_class([error_message])
            return False
