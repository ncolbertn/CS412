from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import timedelta
from .forms import PatronSignupForm, BookSearchForm, BookForm, BorrowForm, PatronUpdateForm
from django.db.models import Q

class PatronListView(ListView):
    ''' Gets all Patron models and lists them '''
    model = Patron
    template_name = 'Library/patron_list.html'
    context_object_name = 'patrons'

class PatronDetailView(DetailView):
    ''' Generic Detail view for the Patron model '''
    model = Patron
    template_name = 'Library/patron_detail.html'
    context_object_name = 'patron'


class LibrarianListView(ListView):
    ''' Generic List View for the Librarian model '''
    model = Librarian
    template_name = 'Library/librarian_list.html'
    context_object_name = 'librarians'

class LibrarianDetailView(DetailView):
    ''' Generic Detail View for the Librarian Model '''
    model = Librarian
    template_name = 'Library/librarian_detail.html'
    context_object_name = 'librarian'


class AuthorListView(ListView):
    ''' Generic List View for the Author model '''
    model = Author
    template_name = 'Library/author_list.html'
    context_object_name = 'authors'

class AuthorDetailView(DetailView):
    ''' Generic detail view for the Author model '''
    model = Author
    template_name = 'Library/author_detail.html'
    context_object_name = 'author'


class BookListView(ListView):
    ''' Generic list view for the Book model '''
    model = Book
    template_name = 'Library/book_list.html'
    context_object_name = 'books'

class BookDetailView(DetailView):
    ''' Generic detail view for the Book model '''
    model = Book
    template_name = 'Library/book_detail.html'
    context_object_name = 'book'


class LoanListView(ListView):
    ''' Lists all loans related to user. If the user is a librarian,
        they will see all Loan objects for all users'''
    model = Loan
    template_name = 'Library/loan_list.html'
    context_object_name = 'loans'

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_staff:
            # Librarian: can see all loans
            return queryset
        else:
            # Regular patron: see only your own loans
            return queryset.filter(patron__user=user)

class LoanDetailView(DetailView):
    ''' Show loan info '''
    model = Loan
    template_name = 'Library/loan_detail.html'
    context_object_name = 'loan'



def signup_view(request):
    ''' Function view for registering a new 
        Patron and User object. '''
    if request.method == 'POST':
        form = PatronSignupForm(request.POST)
        if form.is_valid():
            user = form.save()  # This creates the User and Patron as per the form's save method
            login(request, user)
            return redirect('index')
    else:
        form = PatronSignupForm()
    return render(request, 'Library/signup.html', {'form': form})


def book_search_view(request):
    ''' Function to parse search results '''
    form = BookSearchForm(request.GET or None)
    books = []

    if form.is_valid():
        query = form.cleaned_data.get('query', '').strip()
        if query:
            # filter by book title or author name
            books = Book.objects.filter(
                Q(title__icontains=query) |
                Q(author__first_name__icontains=query) |
                Q(author__last_name__icontains=query)
            )
        else:
            # If no query is provided, show all books
            books = Book.objects.all()
    else:
        # If form is not valid or GET with no data, show all books
        books = Book.objects.all()

    return render(request, 'Library/book_search.html', {'form': form, 'books': books})


@login_required
def borrow_book_view(request, pk):
    # Ensure the user is a patron
    patron = get_object_or_404(Patron, user=request.user)
    book = get_object_or_404(Book, pk=pk)

    # Check if the book is currently available/not in a loan object
    on_loan = Loan.objects.filter(book=book, return_date__isnull=True).exists()
    if on_loan:
        # The book is not available
        return render(request, 'Library/borrow_unavailable.html', {'book': book})

    if request.method == 'POST':
        form = BorrowForm(request.POST)
        if form.is_valid():
            # Create a new loan
            loan_date = timezone.now().date()
            due_date = loan_date + timedelta(days=14)  # loan period of two weeks, maybe longer?
            Loan.objects.create(book=book, patron=patron, loan_date=loan_date, due_date=due_date)
            return redirect('loan-list')
    else:
        form = BorrowForm()

    return render(request, 'Library/borrow_book.html', {'form': form, 'book': book})


# Librarian actions: require user to be staff
def is_librarian(user):
    return user.is_staff

@user_passes_test(is_librarian)
def librarian_dashboard(request):
    ''' The librarian dashboard facilitates back-end functions '''
    return render(request, 'Library/librarian_dashboard.html')


class BookCreateView(CreateView):
    ''' Creates a new book object '''
    model = Book
    form_class = BookForm
    template_name = 'Library/book_form.html'
    success_url = reverse_lazy('book-list')

    def form_valid(self, form):
        existing_author = form.cleaned_data.get('existing_author')
        new_author_first_name = form.cleaned_data.get('new_author_first_name')
        new_author_last_name = form.cleaned_data.get('new_author_last_name')
        new_author_biography = form.cleaned_data.get('new_author_biography')
        new_author_date_of_birth = form.cleaned_data.get('new_author_date_of_birth')
        new_author_date_of_death = form.cleaned_data.get('new_author_date_of_death')

        # If no existing author chosen, create a new one
        if not existing_author:
            new_author = Author.objects.create(
                first_name=new_author_first_name,
                last_name=new_author_last_name,
                biography=new_author_biography or "",
                date_of_birth=new_author_date_of_birth,
                date_of_death=new_author_date_of_death
            )
            form.instance.author = new_author
        else:
            form.instance.author = existing_author

        return super().form_valid(form)


class BookDeleteView(DeleteView):
    ''' deletes a Book object '''
    model = Book
    template_name = 'Library/book_confirm_delete.html'
    success_url = reverse_lazy('book-list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:   # Only librarians can delete books!
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)


@login_required
def return_loan_view(request, pk):
    ''' view to return loan, can be accessed by either librarian or patron of the loan '''
    loan = get_object_or_404(Loan, pk=pk)
    # Permission check: either staff or the patron who borrowed the book
    if not (request.user.is_staff or loan.patron.user == request.user):
        raise PermissionDenied("You do not have permission to return this loan.")

    # Delete the Loan record to "return" the book
    loan.delete()

    # Redirect back to the loan list after returning
    return redirect('loan-list')

class PatronUpdateView(UpdateView):
    '''Update patron info'''
    model = Patron
    form_class = PatronUpdateForm
    template_name = 'Library/patron_update.html'
    context_object_name = 'patron'
    success_url = reverse_lazy('patron-list')

    def dispatch(self, request, *args, **kwargs):
        patron = self.get_object()

        # Permission checks:
        if not (request.user.is_staff or request.user == patron.user):
            return redirect('index')

        return super().dispatch(request, *args, **kwargs)