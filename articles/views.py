from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

import articles

from .models import Article, Comment



def index(request):
    articles_list = Article.objects.order_by('pub_date')
    return render (request, "list.html", {"articles_list": articles_list})


def detail(request, article_id):
    try:
        a = Article.objects.get(id = article_id)
    except:
        raise Http404("Статья не найдено")
    
    comment_list = a.comment_set.order_by('-id')[:10]
    
    return render(request, "detail.html", {'article': a, "comment_list": comment_list})

def leave_comment(request, article_id):
    
    try:
        a = Article.objects.get(id = article_id)
    except:
        raise Http404("Статья не найдено")
    
    a.comment_set.create(author_name = request.POST["name"], comment_text = request.POST["text"])
    return HttpResponseRedirect(reverse('detail', args=(a.id,)))