from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Relationship
from .forms import ProfileModelForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    # instance shows us which profile we want to update
    confirm = False

    if request.method == 'POST':
        if form.is_valid:
            form.save()
            confirm = True  # for update

    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm,
    }

    return render(request, 'profiles/myprofile.html', context)


@login_required
def invited_received_view(request):
    """gets all the invitations for a particular profile"""
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invitation_received(profile)
    results = list(map(lambda x: x.sender, qs))
    if len(results) == 0:
        is_empty = True
    else:
        is_empty = False
    context = {
        'qs': results,
        'is_empty': is_empty,
    }
    return render(request, 'profiles/my_invites.html', context)


@login_required
def invite_profiles_list_view(request):
    """profiles list available to invite"""
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invite(user)
    context = {'qs': qs}
    return render(request, 'profiles/to_invite_list.html', context)


@login_required
def accept_invatation(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
    return redirect('profiles:my-invites-view')


@login_required
def reject_invatation(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        receiver = Profile.objects.get(user=request.user)
        sender = Profile.objects.get(pk=pk)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('profiles:my-invites-view')


@login_required
def profiles_list_view(request):
    """get all profiles by method view"""
    user = request.user
    qs = Profile.objects.get_all_profiles(user)
    context = {'qs': qs}
    return render(request, 'profiles/profile_list.html', context)


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profiles/detail.html'

    def get_object(self, slug=None):
        slug = self.kwargs.get('slug')
        profile = Profile.objects.get(slug=slug)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['posts'] = self.get_object().get_all_authors_posts()
        context['len_posts'] = True if len(self.get_object().get_all_authors_posts()) > 0 else False
        return context


class ProfileListView(LoginRequiredMixin, ListView):
    """get all profiles by list view"""
    model = Profile
    template_name = 'profiles/profile_list.html'
    context_object_name = 'qs'

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        """this function allows us to some additional context to the template"""

        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)  # it gets user the user
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        # relationships where we invited other users
        rel_s = Relationship.objects.filter(receiver=profile)
        # relationships where we are receiver of the invitation
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            # if we will be the only profile 'is_empty' will be equall to True
            context['is_empty'] = True
        return context


@login_required
def send_invitation(request):
    """here we are the sender of invitation and we should choose the receiver,and the receiver is
    our profile pk,based on the profile pk which we get from profiles list,we get the receiver"""

    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)  # primary key

        #  creating relationship
        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')
        return redirect(request.META.get('HTTP_REFERER'))  # in order to stay on the same page
    return redirect('profiles:my-profile-view')  # if access to this url directly


@login_required
def remove_from_friends(request):
    """here we dont know who is the sender and who is the receiver of the request,we have to delete
     the relationship after getting it we have to remove the person who we dont want to fried with from
      our friend list and also remove ourself from that person friend list"""

    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)  # sender is us
        receiver = Profile.objects.get(pk=pk)  # profile we want to remove from friends

        # there is two senario here whether first we requested and we want to remove that guz from
        # out friends list or first that guz requested us and now we want to remove him from our friends list
        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        )

        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))  # ??  # in order to stay on the same page
    return redirect('profiles:my-profile-view')  # if we are not dealing with post request
    # in order to get rid of user from friends list we use signals,'pre_delete signals function'
