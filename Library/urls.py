from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    PatronListView, PatronDetailView,
    LibrarianListView, LibrarianDetailView,
    AuthorListView, AuthorDetailView,
    BookListView, BookDetailView,
    LoanListView, LoanDetailView, signup_view,
    book_search_view, borrow_book_view,
    BookCreateView, BookDeleteView, librarian_dashboard, return_loan_view,
    PatronUpdateView,
)

urlpatterns = [
    path('', BookListView.as_view(), name='index'),
    path('patrons/', PatronListView.as_view(), name='patron-list'),
    path('patrons/<int:pk>/', PatronDetailView.as_view(), name='patron-detail'),
    path('librarians/', LibrarianListView.as_view(), name='librarian-list'),
    path('librarians/<int:pk>/', LibrarianDetailView.as_view(), name='librarian-detail'),
    path('authors/', AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('loans/', LoanListView.as_view(), name='loan-list'),
    path('loans/<int:pk>/', LoanDetailView.as_view(), name='loan-detail'),
    path('signup/', signup_view, name='signup'),
    path('search/', book_search_view, name='book-search'),
    path('borrow/<int:pk>/', borrow_book_view, name='borrow-book'),
    path('librarian/', librarian_dashboard, name='librarian-dashboard'),
    path('librarian/books/add/', BookCreateView.as_view(), name='book-add'),
    path('librarian/books/delete/<int:pk>/', BookDeleteView.as_view(), name='book-delete'),
    path('login/', auth_views.LoginView.as_view(template_name='Library/login.html', next_page='index'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('loans/<int:pk>/', LoanDetailView.as_view(), name='loan-detail'),
    path('loans/<int:pk>/return/', return_loan_view, name='return-loan'),
    path('patrons/<int:pk>/edit/', PatronUpdateView.as_view(), name='patron-edit'),
]
