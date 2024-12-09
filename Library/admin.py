from django.contrib import admin
from .models import *

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Patron)
admin.site.register(Librarian)
admin.site.register(Loan)

