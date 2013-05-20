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
        from django.conf import settings
        activation_url = settings.BASE_URL + \
            reverse('activate_the_profile') + '?email=' + \
            Signer().sign(self.user.email)
        mail_content = 'To Activate the your account visit the below link; '
        mail_content += activation_url
        self.user.email_user('Blog - User Account Activation',
                             mail_content,
                             'no-reply@blog.com')

    def send_email_to_change_mail(self, email):
        from django.conf import settings
        from django.core.mail import send_mail
        activation_url = settings.BASE_URL + \
            reverse('change_email') + '?email=' + \
            Signer().sign(self.user.email) + '&to=' + Signer().sign(email)
        mail_content = 'To change your e-mail visit the below link; '
        mail_content += activation_url
        send_mail('Blog - Change your email address', mail_content,
                  'no-reply@blog.com', [email])

    class Meta:
        db_table = 'profile'