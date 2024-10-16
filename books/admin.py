from django.contrib import admin
from .models import UserBankAccount, UserAddress, BookCategory, BookModel, BorrowedBook
# Register your models here.

admin.site.register(UserBankAccount)
admin.site.register(UserAddress)
admin.site.register(BookCategory)
admin.site.register(BookModel)
admin.site.register(BorrowedBook)