import random

from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import mixins
from django.views import generic
from django.contrib import messages

from . import models, forms

def home(request):
    return render(request, 'home.html')


class SignUpView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = forms.UserCreationForm

    def get_success_url(self):
        return reverse("login")


class TrackerInline(mixins.LoginRequiredMixin):
    form_class = forms.TrackerForm
    model = models.Tracker
    template_name = "tracker_create_or_update.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))
        
        self.object = form.save()

        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        

        return redirect("tracker:list_trackers") 
    
    def formset_creatures_valid(self, formset):
        creatures = formset.save(commit=False)
        for creature in creatures:
            creature.tracker = self.object
            creature.save()


class TrackerCreateView(TrackerInline, generic.CreateView):

    def get_context_data(self, **kwargs):
        context = super(TrackerCreateView, self).get_context_data(**kwargs)
        context['named_formsets'] = self.get_named_formsets()
        return context
    
    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'creatures': forms.CreatureFormSet(prefix='creatures'),
            }
        else:
            return {
                'creatures': forms.CreatureFormSet(self.request.POST or None, self.request.FILES or None,
                                                   prefix='creatures'),
            }
        

class TrackerUpdateView(TrackerInline, generic.UpdateView):

    def get_context_data(self, **kwargs):
        context = super(TrackerUpdateView, self).get_context_data(**kwargs)
        context['named_formsets'] = self.get_named_formsets()
        return context
    
    def get_named_formsets(self):
        return {
            'creatures': forms.CreatureFormSet(self.request.POST or None, self.request.FILES or None,
                                                instance=self.object,
                                                prefix='creatures')
        }
    

class TrackerList(mixins.LoginRequiredMixin, generic.ListView):
    model = models.Tracker
    template_name = 'tracker_list.html'
    context_object_name = 'trackers'

    def get_queryset(self):
        return models.Tracker.objects.filter(user=self.request.user)


def delete_creature(request, pk):
    try:
        creature = models.Creature.objects.get(id=pk)
    except models.Creature.DoesNotExist:
        messages.success(
            request, 'Object does not exist'
        )
        return redirect('tracker:update_tracker', pk=creature.tracker.id)
    
    creature.delete()
    messages.success(
        request, 'Object deleted'
    )
    return redirect('tracker:update_tracker', pk=creature.tracker.id)


class RunView(mixins.LoginRequiredMixin, generic.DetailView):
    template_name = 'run.html'
    context_object_name = 'tracker'

    def get_context_data(self, **kwargs):
        context = super(RunView, self).get_context_data(**kwargs)
        tracker = models.Tracker.objects.get(pk=self.kwargs['pk'])
        initiative_tracker = {}
        for creature in tracker.creature_set.all():
            initiative_tracker.update({
                creature.name: int(creature.initiative) + random.randint(1, 20)
            })
        
        context.update({
                'tracker': {k: v for k, v in sorted(initiative_tracker.items(), key=lambda item: item[1])},
                'tracker_id': tracker.pk
            })
        return context
        

    def get_object(self):
        return models.Tracker.objects.get(pk=self.kwargs['pk'])