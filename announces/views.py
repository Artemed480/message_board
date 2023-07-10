from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import resolve, reverse

from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination

from .models import Announce, Reply
from .forms import AnnounceForm
from .filters import ReplyFilter
from .serializers import AnnounceSerializer



# Create your views here.
def list(request):
    return render(request, 'announces/list_announces.html')

@api_view(['GET'])
def list_announces(request):
    announces = Announce.objects.order_by('-pub_date')
    paginator = PageNumberPagination()
    paginator.page_size = 4
    results = paginator.paginate_queryset(announces, request)

    serializer = AnnounceSerializer(results, many=True)

    return paginator.get_paginated_response(serializer.data)



class AnnounceDetail(DetailView):
    model = Announce
    template_name = 'announces/announcedetail.html'
    context_object_name = 'announce'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.id = resolve(self.request.path_info).kwargs['pk']
        context['user'] = self.request.user
        context['replies'] = Reply.objects.filter(announce_id=self.id)
        return context


class AnnounceCreate(LoginRequiredMixin, CreateView):
    template_name = 'announces/createannounce.html'
    form_class = AnnounceForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        instance.save()
        return redirect("/announces/")

class PersonalPageView(LoginRequiredMixin, ListView):
    model = Announce
    template_name = 'announces/personal_page.html'
    context_object_name = 'announces'

    def get_queryset(self):
        queryset = Announce.objects.filter(author=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user.username
        context['undefined_replies'] = Reply.objects.filter(announce__author=self.request.user).filter(accept=False)
        return context


class PersonalRepliesView(LoginRequiredMixin, ListView):
    model = Reply
    template_name = 'announces/personal_replies.html'
    context_object_name='replies'
    ordering = ['-pub_date']

    def get_queryset(self):
        queryset = Reply.objects.filter(announce__author=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['undefined_replies'] = Reply.objects.filter(announce__author=self.request.user).filter(accept=False)
        context['filter'] = ReplyFilter(self.request.GET, queryset=self.get_queryset())
        return context

class AnnounceEdit(LoginRequiredMixin, UpdateView):
    template_name = 'announces/editannounce.html'
    form_class = AnnounceForm
    success_url = '/announces/account'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Announce.objects.get(pk=id)

class AnnounceDelete(LoginRequiredMixin, DeleteView):
    template_name = 'announces/deleteannounce.html'
    model = Announce
    success_url = '/announces/account'

class ReplyDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'announces/deletereply.html'
    model = Reply
    success_url = '/announces/account'

@login_required()
def reply_to_announce(request, pk):
    if request.method == "POST":
        user = request.user
        announce = Announce.objects.get(id=pk)
        content = request.POST['content']
        Reply.objects.create(announce=announce, content=content, replier=user)
        return HttpResponseRedirect('/announces/')
    else:
        print('error')
    return render(request, 'announces/announces.html')


@login_required()
def reply_accept(request, pk):
    if request.method == "GET":
        reply = Reply.objects.get(id=pk)
        reply.accept = True
        reply.save()
        return redirect(reverse("announces:personal_replies") + '?accept=false')
    else:
        messages.error(request, 'Что то пошло не так')
        return HttpResponseRedirect('/announces/account/replies')
    return render(request, 'announces/announces.html')

