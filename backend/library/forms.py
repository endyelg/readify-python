from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

from .models import Book, Borrower, Borrowing, Fine, Reservation, Category, Author


class CustomUserCreationForm(UserCreationForm):
    """Extended user creation form for borrowers"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=15, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    library_id = forms.CharField(max_length=20, required=True, help_text="Your unique library ID")

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
        self.fields['password1'].help_text = 'Your password must contain at least 8 characters.'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def clean_library_id(self):
        library_id = self.cleaned_data.get('library_id')
        if Borrower.objects.filter(library_id=library_id).exists():
            raise ValidationError("A borrower with this library ID already exists.")
        return library_id

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Create borrower profile
            Borrower.objects.create(
                user=user,
                library_id=self.cleaned_data['library_id'],
                phone=self.cleaned_data.get('phone', ''),
                address=self.cleaned_data.get('address', ''),
                date_of_birth=self.cleaned_data.get('date_of_birth'),
            )
        return user


class BorrowerForm(forms.ModelForm):
    """Form for updating borrower information"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = Borrower
        fields = ['library_id', 'phone', 'address', 'date_of_birth', 'is_active', 'max_books_allowed']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, commit=True):
        borrower = super().save(commit=False)
        if commit:
            borrower.save()
            # Update user information
            user = borrower.user
            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.save()
        return borrower


class BookForm(forms.ModelForm):
    """Form for adding/editing books"""
    
    class Meta:
        model = Book
        fields = [
            'title', 'isbn', 'authors', 'category', 'publisher', 
            'publication_year', 'pages', 'description', 'cover_image',
            'total_copies', 'price'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'authors': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['authors'].queryset = Author.objects.all().order_by('last_name', 'first_name')
        self.fields['category'].queryset = Category.objects.all().order_by('name')

    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn')
        # Basic ISBN validation (should be 13 digits)
        if isbn and not isbn.isdigit():
            raise ValidationError("ISBN must contain only digits.")
        if isbn and len(isbn) != 13:
            raise ValidationError("ISBN must be exactly 13 digits.")
        return isbn

    def clean_publication_year(self):
        year = self.cleaned_data.get('publication_year')
        current_year = timezone.now().year
        if year and (year < 1000 or year > current_year):
            raise ValidationError(f"Publication year must be between 1000 and {current_year}.")
        return year


class BorrowingForm(forms.ModelForm):
    """Form for borrowing books"""
    
    class Meta:
        model = Borrowing
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional notes about this borrowing...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['notes'].required = False


class ReturnBookForm(forms.ModelForm):
    """Form for returning books"""
    
    class Meta:
        model = Borrowing
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional notes about the return...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['notes'].required = False


class FineForm(forms.ModelForm):
    """Form for managing fines"""
    
    class Meta:
        model = Fine
        fields = ['amount', 'status', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs['step'] = '0.01'


class ReservationForm(forms.ModelForm):
    """Form for reserving books"""
    
    class Meta:
        model = Reservation
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional notes about this reservation...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['notes'].required = False


class SearchForm(forms.Form):
    """Form for searching books"""
    search = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by title, ISBN, author, or publisher...',
            'class': 'form-control'
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    author = forms.ModelChoiceField(
        queryset=Author.objects.all(),
        required=False,
        empty_label="All Authors",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    status = forms.ChoiceField(
        choices=[('', 'All Status')] + Book.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all().order_by('name')
        self.fields['author'].queryset = Author.objects.all().order_by('last_name', 'first_name')


class CategoryForm(forms.ModelForm):
    """Form for adding/editing categories"""
    
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class AuthorForm(forms.ModelForm):
    """Form for adding/editing authors"""
    
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'bio', 'birth_date']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date and birth_date > timezone.now().date():
            raise ValidationError("Birth date cannot be in the future.")
        return birth_date


class ContactForm(forms.Form):
    """Contact form for library inquiries"""
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=200, required=True)
    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5}),
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['subject'].widget.attrs.update({'class': 'form-control'})
        self.fields['message'].widget.attrs.update({'class': 'form-control'})


class ReportForm(forms.Form):
    """Form for generating reports"""
    REPORT_CHOICES = [
        ('borrowings', 'Borrowing Report'),
        ('returns', 'Return Report'),
        ('overdue', 'Overdue Books Report'),
        ('fines', 'Fines Report'),
        ('popular', 'Popular Books Report'),
        ('borrowers', 'Borrower Activity Report'),
    ]

    report_type = forms.ChoiceField(
        choices=REPORT_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise ValidationError("Start date cannot be after end date.")

        return cleaned_data
