from django.shortcuts import render
from django.views.generic import FormView
from .forms import UserRegistrationForm
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.shortcuts import redirect
from django.views import View
from .models import BookCategory,BookModel,BorrowedBook
from .forms import BookCategoryForm,BookModelForm
from .import forms
from django.views.generic import DetailView
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from transactions.models import UserBankAccount, Transaction
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse

def send_book_email(user,book,balance,subject,template):
    message = render_to_string(template,{
        'user' : user,
         'borrowed_books': {
            'book': book,
        },
        'user_account': {
            'balance': balance,
        } 
    })

    send_email = EmailMultiAlternatives(subject,'',to=[user.email])
    send_email.attach_alternative(message,"text/html")
    send_email.send()
    
class UserRegistrationView(FormView):
    template_name = 'books/user_registration.html'
    form_class = UserRegistrationForm
    
    def form_valid(self,form):
        user = form.save()
        login(self.request, user)
        return redirect('homepage')
    

class UserLoginView(LoginView):
    template_name = 'books/user_login.html'
    def get_success_url(self):
        return reverse_lazy('homepage')

class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')
    
class HomeView(View):
    def get(self, request):
        return render(request, 'books/home.html')
    
def homePage(request,book_slug=None):
    data = BookModel.objects.all()
    if book_slug is not None:
        try:
            category = BookCategory.objects.get(slug = book_slug)
            data = BookModel.objects.filter(book_model=category)
        except BookCategory.DoesNotExist:
            messages.error(request,"The requested book category doesn't exist.")
    bookcategories = BookCategory.objects.all()
    return render(request,'books/home.html',{'data' : data,'bookcategories' : bookcategories})

def add_book(request):
    if request.method == "POST":
        form = BookModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('homepage') 
    else:
        form = BookModelForm()
    return render(request, 'books/add_book.html', {'form': form})

def add_book_category(request):
    if request.method == "POST":
        form = BookCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage') 
    else:
        form = BookCategoryForm()
    return render(request, 'books/add_book_category.html', {'form': form})

class DetailsPostView(DetailView):
    model = BookModel
    pk_url_kwarg = 'id'
    template_name = 'books/view_detail.html'

    def post(self, request, *args, **kwargs):
        book = self.get_object()
        try:
         user_account = get_object_or_404(UserBankAccount,user=request.user)
        except UserBankAccount.DoesNotExist:
            messages.error(request, "You do not have a bank account. Please create one to proceed.")
            return redirect('detail') 
        
        if user_account.balance >= book.borrow_price:
            user_account.balance -= book.borrow_price
            user_account.save()
            
            Transaction.objects.create(
                    account=user_account,
                    amount=book.borrow_price,
                    balance_after_transaction=user_account.balance,
                )
            
            BorrowedBook.objects.create(user=request.user, book=book)
            messages.success(request, f"You have successfully borrowed {book.title}")
            send_book_email(self.request.user, book, user_account.balance, "Borrow Book Message", "books/borrow_email.html")
            return redirect('profile', id=request.user.id)
        else:
             messages.error(request, "Sorry! You do not have enough balance to borrow this book.")
             return redirect(reverse('detail', kwargs={'id': book.id}))
        

class CommentsPostView(DetailsPostView):
    model = BookModel
    pk_url_kwarg = 'id'
    template_name = 'books/view_detail.html'
    
    def post(self,request,*args,**kwargs):
        bookModel = self.get_object()
        comment_form = forms.CommentForm(data=self.request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.bookModel= bookModel
            new_comment.save()
            messages.success(request, "Comment added successfully!") 
        return redirect('detail_post',id=bookModel.id)
    
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(**kwargs)
        bookModel = self.object
        comments = bookModel.comments.all()
        comment_form = forms.CommentForm()
        context['comments'] = comments
        context['comment_form'] = comment_form
        print(context)
        return context
    

def profile_view(request,id):
    user = get_object_or_404(User, id=id)
    borrowed_books = BorrowedBook.objects.filter(user=request.user)
    return render(request, 'books/profile.html', {'borrowed_books': borrowed_books})

def Return_Book(request,id):
    borrowed_books = BorrowedBook.objects.filter(user=request.user, book_id=id)
    user_account = get_object_or_404(UserBankAccount, user=request.user)
    
    borrowed_book = borrowed_books.first()  
    book = borrowed_book.book

    user_account.balance += book.borrow_price
    user_account.save()

    Transaction.objects.create(
        account=user_account,
        amount=book.borrow_price,
        balance_after_transaction=user_account.balance,
    )

    borrowed_book.delete()

    send_book_email(request.user, book, user_account.balance, "Return Book Message", "books/return_email.html")

    messages.success(request, f"You have successfully returned {book.title}. The price has been added to your balance.")
    return redirect('profile', id=request.user.id)




    
    
    