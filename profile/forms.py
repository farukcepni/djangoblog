from django import forms
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify
from models import Profile
from django.contrib.auth.models import User


class EditForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField()
    account_type = forms.ChoiceField(
        choices=((True, 'Active'), (False, 'Deactive')))

    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].initial = kwargs['instance'].user.first_name
        self.fields['last_name'].initial = kwargs['instance'].user.last_name
        self.fields['email'].initial = kwargs['instance'].user.email
        self.fields['account_type'].initial = kwargs['instance'].user.is_active

    def save(self, commit=True):
        old_email = self.instance.user.email
        super(EditForm, self).save(self)
        user = self.instance.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.is_active = self.cleaned_data['account_type'] == 'True' or False
        user.save()
        if old_email != self.cleaned_data['email']:
            self.instance.is_verified = False
            self.instance.send_activation_email()

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'birthdate',
                  'gender', 'email', 'account_type']


class SignupForm(forms.ModelForm):
    # TODO: set the Field.error_messages via function
    # like {'required': '%s field is required'}

    email = forms.EmailField(label=_('E-mail'),
                             help_text=_('E-mail field is required'),
                             error_messages={
                                 'required': 'Please, type your e-mail'})
    password = forms.CharField(widget=forms.PasswordInput,
                               min_length=6,
                               label=_('Password'),
                               help_text=_('Password must be at least 6 chars'))
    password_again = forms.CharField(widget=forms.PasswordInput,
                                     label=_('Password Again'),
                                     help_text=_('Password must be same \
                                     with the password'),
                                     required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password',
                  'password_again')

    def save(self, commit=True):
        data = self.cleaned_data
        user = User()
        user.email = data['email']
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.username = slugify(user.get_full_name())
        user.set_password(data['password'])
        user.save()
        profile = Profile()
        profile.user_id = user.id
        profile.is_verified = False
        profile.birthdate = None
        profile.save()
        return profile

    def _password_match(self):
        password = self.data.get('password')
        password_again = self.data.get('password_again')
        if password != '' and password_again != '' and \
           password == password_again:
            return True
        else:
            self._errors['password_again'] = self.error_class(
                [_('Password again and password fields must be same')]
            )
            return False

    def _email_exists(self):
        is_email_exists = Profile.is_email_exists(self.data.get('email'))
        if is_email_exists is True:
            self._errors['email'] = self.error_class(
                [_('This E-mail has already taken.')]
            )
            return True
        else:
            return False

    def is_valid(self):
        # override is_valid() method to check
        #   password == password_again
        form_valid = super(SignupForm, self).is_valid()
        password_match = self._password_match()
        if form_valid is True and \
                password_match is True and \
                self._email_exists() is False:
            return True
        else:
            return False


class LoginForm(forms.Form):
    email = forms.EmailField(label=_('E-mail'))
    password = forms.CharField(widget=forms.PasswordInput,
                               label=_('Password'))