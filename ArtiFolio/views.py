from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, get_object_or_404
from .models import Artwork, Challenge, ProgressPhoto, PrivateComment
from .forms import ArtworkFilterForm, PrivateCommentForm, ArtworkForm, ProgressPhotoFormSet, ChallengeForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.views.generic import TemplateView
from django.contrib import messages

# Create your views here.
class GlobalStatsView(LoginRequiredMixin, TemplateView):
    template_name = 'ArtiFolio/global_stats.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        general_stats = Artwork.objects.filter(user=user).aggregate(
            total_artworks=Count('id', distinct=True),
            total_photos=Count('progressphoto', distinct=True),
            total_comments=Count('privatecomment', distinct=True)
        )
        context['general_stats'] = general_stats
        return context
        
class ArtworkList(LoginRequiredMixin, ListView):
    model = Artwork
    template_name = 'ArtiFolio/artwork_list.html'
    context_object_name = 'artworks'
    paginate_by = 3
    
    def get_queryset(self):
        queryset = Artwork.objects.filter(user=self.request.user).annotate(num_photos=Count('progressphoto'))
        
        title = self.request.GET.get('title')
        technique = self.request.GET.get('technique')
        month = self.request.GET.get('start_month')
        year = self.request.GET.get('start_year')

        if title:
            queryset = queryset.filter(title__icontains=title)
        if technique:
            queryset = queryset.filter(technique=technique)
        if month:
            queryset = queryset.filter(start_date__month=month)
        if year:
            queryset = queryset.filter(start_date__year=year)
            
        return queryset.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = ArtworkFilterForm(self.request.GET)
        
        stats = Artwork.objects.filter(user=self.request.user).aggregate(total_artworks=Count('id'))
        context['stats'] = stats
        context['challenges'] = Challenge.objects.filter(user=self.request.user, is_completed=False).order_by('id')
        return context

class ArtworkDetail(LoginRequiredMixin, DetailView):
    model = Artwork
    template_name = 'ArtiFolio/artwork_detail.html'
    context_object_name = 'artwork'
    
    def get_queryset(self):
        return Artwork.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['progress_photos'] = ProgressPhoto.objects.filter(artwork=self.object).order_by('order')
        context['private_comments'] = PrivateComment.objects.filter(artwork=self.object).order_by('-created_at')
        context['comment_form'] = PrivateCommentForm()
        return context

class ArtworkCreate(LoginRequiredMixin, CreateView):
    model = Artwork
    success_message = "Your work '%(title)s' has been successfully uploaded!"
    template_name = 'ArtiFolio/artwork_create.html'
    form_class = ArtworkForm
    success_url = reverse_lazy('artwork_list')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['progressphoto_formset'] = ProgressPhotoFormSet(self.request.POST, self.request.FILES)
        else:
            context['progressphoto_formset'] = ProgressPhotoFormSet()
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['progressphoto_formset']
        form.instance.user = self.request.user
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class ArtworkUpdate(UpdateView):
    model = Artwork
    success_message = "The information about your work has been updated."
    template_name = 'ArtiFolio/artwork_update.html'
    form_class = ArtworkForm
    success_url = reverse_lazy('artwork_list')
    context_object_name = 'artwork'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['progressphoto_formset'] = ProgressPhotoFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['progressphoto_formset'] = ProgressPhotoFormSet(instance=self.object)
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['progressphoto_formset']
        
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class ArtworkDelete(DeleteView):
    model = Artwork
    template_name = 'ArtiFolio/artwork_delete.html'
    success_url = reverse_lazy('artwork_list')
    context_object_name = 'artwork'
    
    def form_valid(self, form):
        messages.success(self.request, "The work has been permanently removed.")
        return super().form_valid(form)
    
def add_private_comment(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk)
    if request.method == 'POST':
        form = PrivateCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.artwork = artwork
            comment.save()
            return redirect('artwork_detail', pk=artwork.pk)
    return redirect('artwork_detail', pk=artwork.pk)

def delete_private_comment(request, pk):
    comment = get_object_or_404(PrivateComment, pk=pk)
    artwork_id = comment.artwork.id
    
    if request.user == comment.user:
        comment.delete()
    return redirect('artwork_detail', pk=artwork_id)

class ChallengeCreate(LoginRequiredMixin, CreateView):
    model = Challenge
    template_name = 'ArtiFolio/challenge_create.html'
    form_class = ChallengeForm
    success_url = reverse_lazy('artwork_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
def challenge_complete(request, pk):
    if request.method == 'POST':
        challenge = get_object_or_404(Challenge, pk=pk, user=request.user)
        if 'complete' in request.POST:
            challenge.delete() 
            messages.success(request, 'Challenge completed! Great job.')
    return redirect('artwork_list')