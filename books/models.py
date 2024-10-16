from django.db import models
from django.contrib.auth.models import User
from .constants import ACCOUNT_TYPE, GENDER_TYPE
# django amaderke built in user niye kaj korar facility dey


class UserBankAccount(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE)
    account_no = models.IntegerField(unique=True) # account no duijon user er kokhono same hobe na
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_TYPE)
    initial_deposite_date = models.DateField(auto_now_add=True)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2) # ekjon user 12 digit obdi taka rakhte parbe, dui doshomik ghor obdi rakhte parben 1000.50
    def __str__(self):
        return str(self.account_no)
    
class UserAddress(models.Model):
    user = models.OneToOneField(User, related_name='address', on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length= 100,null=True,blank=True)
    postal_code = models.IntegerField(null=True,blank=True)
    country = models.CharField(max_length=100)
    def __str__(self):
        return str(self.user.email)

class BookCategory(models.Model):
    category_name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=100,unique=True,null=True,blank=True)
    
    def __str__(self):
        return self.category_name
    
class BookModel(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    borrow_price = models.IntegerField()
    book_model = models.ForeignKey(BookCategory,related_name='books',on_delete=models.CASCADE)
    img = models.ImageField(upload_to='uploads/',null=True,blank=True)
    borrowed_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    
    def __str__(self):
        return self.title
    
class BorrowedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrowed_books')
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE, related_name='borrowed_books')
    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"
    
class Comment(models.Model):
    bookModel = models.ForeignKey(BookModel,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=250)
    email = models.EmailField()
    body = models.TextField()
    created_one = models.DateTimeField(auto_now_add=True)
    

    