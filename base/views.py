from pickle import TRUE
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import SignUpForm,SharingForm, UpdateForm, SuperUpdateForm

# Imports for Reordering Feature
from django.views import View
from django.shortcuts import redirect
from django.db import transaction
from django.db.models import Q
from .models import Share, Sharing, Task
#from .forms import PositionForm
from rules.contrib.views import LoginRequiredMixin, PermissionRequiredMixin, objectgetter, permission_required

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')
    
class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = SignUpForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'base/task_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__contains=search_input)

        context['search_input'] = search_input

        return context
    
class ShareList(LoginRequiredMixin, ListView):
    model = Sharing
    context_object_name = 'shares'
    template_name = 'base/sharing_list.html'
    def get_context_data(self, **kwargs):
        context = super(ShareList,self).get_context_data(**kwargs)
        context['shares'] = context['shares'].filter(user=self.request.user)

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['shares'] = context['shares'].filter(
                title__contains=search_input)

        context['search_input'] = search_input

        return context

class TaskLists(LoginRequiredMixin, ListView):
    model = Sharing
    context_object_name = 'taskss'
    template_name = 'base/sharetask_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['taskss'] = Task.objects.filter(sharing__target=self.request.user)
        context['count'] = context['taskss'].filter(complete=False).count()


        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['taskss'] = context['taskss'].filter(
                title__contains=search_input)

        context['search_input'] = search_input

        return context
    
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'
    
class ShareDetail(LoginRequiredMixin, DetailView):
    model = Sharing
    context_object_name = 'shared'
    template_name = 'base/sharing_detail.html'

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description','view_only', 'complete']
    success_url = reverse_lazy('tasks')
    template_name = 'base/task_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class ShareCreate(LoginRequiredMixin, CreateView):
    model = Sharing
    template_name = 'base/sharing_form.html'
    form_class = SharingForm
    success_url = reverse_lazy('shares')
    
    def get_form_kwargs(self):
        kwargs = super(ShareCreate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ShareCreate, self).form_valid(form)
    
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = UpdateForm
    template_name = 'base/task_form_update.html'
    success_url = reverse_lazy('tasks')
    
class SuperTaskUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Task
    template_name = 'base/task_form.html'
    form_class = SuperUpdateForm
    success_url = reverse_lazy('tasks')
    permission_required = "base.change_task"
    
class OwnerTaskUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Task
    template_name = 'base/task_form.html'
    fields = ('title','description','view_only','complete')
    success_url = reverse_lazy('tasks')
    permission_required = ["base.change_task","base.delete_task"]
    
class ShareUpdate(LoginRequiredMixin, UpdateView):
    model = Share
    fields = ['target','target2']
    success_url = reverse_lazy('tasks')
    
class SharingUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Sharing
    form_class = SharingForm
    success_url = reverse_lazy('shares')
    permission_required = "base.change_sharing"
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class TaskDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Task
    template_name = 'base/task_confirm_delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    permission_required = "base.delete_task"
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)

class ShareDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Sharing
    template_name = 'base/sharing_confirm_delete.html'
    context_object_name = 'share'
    success_url = reverse_lazy('shares')
    permission_required = "base.delete_sharing"
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)
    
"""class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('tasks'))"""
