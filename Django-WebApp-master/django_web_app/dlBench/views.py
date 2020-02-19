from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django import forms
from extra_views import CreateWithInlinesView, InlineFormSetFactory,UpdateWithInlinesView 
from django.forms.models import BaseInlineFormSet

from .models import Project,DataSet,DLModel,PerformanceMetrics

import operator
from django.urls import reverse_lazy
from django.contrib.staticfiles.views import serve

from django.db.models import Q


def home(request):
    context = {
        'projects': Project.objects.all()
    }
    return render(request, 'dlBench/home.html', context)

def search(request):
    template='dlBench/home.html'

    query=request.GET.get('q')
    project_filter=Project.objects.filter(Q(title__icontains=query) | Q(author__username__icontains=query) | Q(task__icontains=query) |
        Q(project_description__icontains=query)
        | Q(dataSetDetails__dataset_name__icontains=query) | Q(dataSetDetails__dataset_description__icontains=query)
        |Q(dlModelDetails__model_framework__icontains=query)| Q(dlModelDetails__model_description__icontains=query)
        |Q(performanceDetails__accuracy_or_utilization__icontains=query))

    from itertools import chain
    result_list = list(chain(project_filter))
    print(result_list)
    paginate_by=2
    if(len(result_list)>0):
        context={ 'projects':result_list,'isSearch':"true" }
    else:    
        context={ 'projects':result_list,"isEmpty":"true" }
    return render(request,template,context)
   

def getfile(request):
   return serve(request, 'File')


class PostListView(ListView):
    model = Project
    template_name = 'dlBench/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'projects'
    ordering = ['-date_posted']
    paginate_by = 2


class UserPostListView(ListView):
    model = Project
    template_name = 'dlBench/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'projects'
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Project.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Project
    template_name = 'dlBench/post_detail.html'

from django.http import HttpResponseRedirect


class RequiredFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        self.empty_permitted = False
        for form in self.forms:
            form.empty_permitted = False

    def clean(self):
      cleaned_data = super(RequiredFormSet, self).clean()
      print(cleaned_data)  

class DataSetViewInline(InlineFormSetFactory):
    model = DataSet
    fields = ['dataset_name','dataset_url','dataset_file','dataset_description']    
    formset_class= RequiredFormSet
    factory_kwargs = {'extra': 1,'can_order': False, 'can_delete': False, 'max_num': 1,'formset': RequiredFormSet}

    def clean_value(self):
      cleaned_data = super(DataSetViewInline, self).clean()
      print(cleaned_data)  


class ModelViewInline(InlineFormSetFactory):
    model = DLModel
    fields = ['model_framework','model_url','model_file','model_description']   
    formset_class= RequiredFormSet 
    factory_kwargs = {'extra': 1,'can_order': False, 'can_delete': False,'max_num': 1,'formset': RequiredFormSet}

class PerformanceMetricsInline(InlineFormSetFactory):
  model=PerformanceMetrics
  fields=['accuracy_or_utilization','training_time','testing_time','metrics_description']
  formset_class= RequiredFormSet 
  factory_kwargs = {'extra': 1,'can_order': False, 'can_delete': False,'max_num': 1,'formset': RequiredFormSet}
 

class PostCreateView(LoginRequiredMixin,CreateWithInlinesView):
    model = Project
    inlines = [DataSetViewInline,ModelViewInline,PerformanceMetricsInline]
    fields = ['title','project_description','task','configurations_varied']
    template_name = 'dlBench/post_form.html'

    def form_valid(self, form):
      form.instance.author = self.request.user
      return super().form_valid(form)
    
  
class PostUpdateView(LoginRequiredMixin,UpdateWithInlinesView,UserPassesTestMixin):
    model = Project
    template_name = 'dlBench/post_form.html'
    inlines = [DataSetViewInline,ModelViewInline,PerformanceMetricsInline]
    fields = ['title','project_description','task','configurations_varied']


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
      

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    success_url = '/'
    template_name = 'dlBench/post_confirm_delete.html'

    def test_func(self):

        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'dlBench/about.html', {'title': 'About'})

