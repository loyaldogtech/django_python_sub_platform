from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . forms import ArticleForm, UpdateUserForm
from django.http import HttpResponse
from . models import Article

@login_required(login_url='my_login')
def software_engineer_dashboard(request):

    return render(request, 'software_engineer/software_engineer-dashboard.html')

@login_required(login_url='my_login')
def create_article(request):

    form = ArticleForm()

    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('my-articles')

    context = {'CreateArticleForm': form}
    return render(request, 'software_engineer/create-article.html', context)

@login_required(login_url='my_login')
def my_articles(request):
    
    current_user = request.user.id
    article = Article.objects.filter(user=current_user).order_by('-date_posted')
    context = {'AllArticles': article}
    return render(request, 'software_engineer/my-articles.html', context)

@login_required(login_url='my_login')
def update_article(request, pk):

    try:

        article = Article.objects.get(id=pk, user=request.user)

    except:
        return redirect('my-articles')
    
    form = ArticleForm(instance=article)

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('my-articles')

    context = {'UpdateArticleForm': form}
    return render(request, 'software_engineer/update-article.html', context)

@login_required(login_url='my_login')
def delete_article(request, pk):
        
    try:
        article = Article.objects.get(id=pk, user=request.user)
    except:
        return redirect('my-articles')
    
    if request.method == 'POST':
        article.delete()
        return redirect('my-articles')
    return render(request, 'software_engineer/delete-article.html')

@login_required(login_url='my_login')
def account_management(request):

    form = UpdateUserForm(instance=request.user)

    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('software_engineer-dashboard')

    context = {'UpdateUserForm': form}
    return render(request, 'software_engineer/account-management.html', context)

        
