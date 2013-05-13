from django.db import models
from django.contrib.auth.models import User
from PIL import Image as PILImage
import os
from tasks import create_thumbs
from settings import MEDIA_ROOT


class Image(models.Model):
    user = models.ForeignKey(User)
    filename = models.CharField(max_length=200)
    image = models.FileField(upload_to='static/media')

    thumbs = (('THUMB', 100, 100), ('MIDDLE', 200, 200))

    def save(self, force_insert=False, force_update=False, using=None):
        super(Image, self).save()
        #create_thumbs(self)
        create_thumbs.delay(self)

    @property
    def get_thumb(self):
        return self.image.url + '.THUMB.jpg'

    def _create_thumbs(self):
        image = PILImage.open(self.image)
        ext = self.image.path[-4:]
        for name, width, height in self.thumbs:
            image.thumbnail((width, height))
            c = self.image.path
            image.save(self.image.path + '.' + name + ext)

    def _delete_thumbs(self):
        for thumb in self.thumbs:
            the_file = self.image.path + '.' + thumb[0] + self.image.path[-4:]
            if os.path.isfile(the_file):
                os.remove(the_file)

    def delete(self, using=None):
        self._delete_thumbs()
        self.image.delete(save=False)
        super(Image, self).delete()

    class Meta:
        db_table = 'image'
