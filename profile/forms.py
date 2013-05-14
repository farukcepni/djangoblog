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

    def clean_email(self):
        if Profile.is_email_exists(self.cleaned_data['email']):
            raise forms.ValidationError(_('This email has been already taken'))
        return self.cleaned_data['email']

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        if 'password' in cleaned_data and 'password_again' in cleaned_data and\
                cleaned_data['password'] != cleaned_data['password_again']:
            self._errors['password_again'] = self.error_class([_(
                'Password again must be same with password')])
        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(label=_('E-mail'))
    password = forms.CharField(widget=forms.PasswordInput,
                               label=_('Password'))