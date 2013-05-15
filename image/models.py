from django.db import models
from django.contrib.auth.models import User
from PIL import Image as PILImage
import os
from tasks import create_thumbs
from django.conf import settings


class Image(models.Model):
    MAX_SIZE = 4 * 1024 * 1024
    ALLOWED_EXTS = ('jpg', 'png')
    ALLOWED_TYPES = ('image/jpeg', 'image/png')
    THUMBS = (('THUMB', 100, 100), ('MIDDLE', 200, 200))

    user = models.ForeignKey(User)
    filename = models.CharField(max_length=200)
    image = models.FileField(upload_to='user_image')

    def save(self, force_insert=False, force_update=False, using=None):
        super(Image, self).save()
        create_thumbs.delay(self)

    @property
    def get_thumb(self):
        ext = os.path.splitext(self.image.path)[1]
        return settings.MEDIA_URL + self.image.url + '.THUMB' + ext

    def _create_thumbs(self):
        image = PILImage.open(self.image)
        ext = os.path.splitext(self.image.path)[1]
        for name, width, height in self.THUMBS:
            image.thumbnail((width, height))
            image.save(self.image.path + '.' + name + ext)

    def _delete_thumbs(self):
        for thumb in self.THUMBS:
            the_file = self.image.path + '.' + thumb[0] + \
                os.path.splitext(self.image.path)[1]
            if os.path.isfile(the_file):
                os.remove(the_file)

    def delete(self, using=None):
        self._delete_thumbs()
        self.image.delete(save=False)
        super(Image, self).delete()

    class Meta:
        db_table = 'image'
