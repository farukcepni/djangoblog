from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.core.signing import Signer


class Profile(models.Model):
    GENDER_CHOICES = (('M', _('Male')), ('F', _('Female')))

    user = models.OneToOneField(User)
    birthdate = models.DateField(blank=True, null=True,
                                 verbose_name=_('Birthdate'))
    gender = models.CharField(max_length=1,
                              choices=GENDER_CHOICES,
                              verbose_name=_('Gender'))
    is_verified = models.BooleanField(default=False,
                                      verbose_name=_('Verified'))


    @classmethod
    def is_email_exists(cls, email):
        email_count = User.objects.filter(email=email).count()
        return email_count > 0 or False

    def send_activation_email(self):
        activation_url = 'http://localhost:8000' + \
            reverse('activate_the_profile') + '?email=' + \
            Signer().sign(self.user.email)
        mail_content = 'To Activate the your account visit the below link; '
        mail_content += activation_url
        self.user.email_user('Blog - User Account Activation',
                             mail_content,
                             'no-reply@blog.com')

    class Meta:
        db_table = 'profile'