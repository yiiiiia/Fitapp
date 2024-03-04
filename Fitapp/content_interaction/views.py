from django.shortcuts import render, redirect
from .forms import ArticleForm, CommentForm
from .models import Article, Comment

def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            new_article = form.save(commit=False)
            new_article.author = request.user
            new_article.save()
            return redirect('article_detail', pk=new_article.pk)
    else:
        form = ArticleForm()
    return render(request, 'content_interaction/add_article.html', {'form': form})
