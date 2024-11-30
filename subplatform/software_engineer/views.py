from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . forms import ArticleForm
from django.http import HttpResponse

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
            return HttpResponse('Article created successfully')

    context = {'CreateArticleForm': form}
    return render(request, 'software_engineer/create-article.html', context)