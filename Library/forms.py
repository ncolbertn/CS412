from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Patron, Book, Loan



class PatronSignupForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True)
    library_card_number = forms.CharField(required=True)
    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        # Additional user field assignments
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            # Create associated Patron profile
            Patron.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                address=self.cleaned_data['address'],
                email=self.cleaned_data['email'],
                phone_number=self.cleaned_data['phone_number'],
                library_card_number=self.cleaned_data['library_card_number'],
                date_of_birth=self.cleaned_data['date_of_birth']
            )
        return user


class BookSearchForm(forms.Form):
    query = forms.CharField(label='Search for books', required=False)
    # Optionally add filters: author name, publication date, etc.


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title', 'isbn', 'publication_date', 'number_of_pages',
            'language', 'cover_image', 'description', 'author',
        ]


class BorrowForm(forms.Form):
    # If you need a form for confirmation or due date selection, include fields
    # If borrowing is always a fixed loan period, you may just need a button.
    confirm = forms.BooleanField(initial=True, required=True)


class PatronUpdateForm(forms.ModelForm):
    class Meta:
        model = Patron
        fields = ['first_name', 'last_name', 'address', 'email', 'phone_number']