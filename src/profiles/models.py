from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

from .utils import get_random_code
from django.template.defaultfilters import slugify
from django.db.models import Q


class ProfileManager(models.Manager):
    def get_all_profiles_to_invite(self, sender):
        """gets all the profiles that are available for us to invite so cases of profiles where we are already
        in a relationship with were excluded.
        Here the sender is ourselves and the receiver is different user with whom we dont have a relationship status
        set to 'accepted' """

        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))
        # grabbed all the relationships where we are the sender or receiver

        accepted = set([])
        for rel in qs:
            if rel.status == 'accepted':
                # because are either receiver or sender using set prevents repetition in list
                accepted.add(rel.receiver)
                accepted.add(rel.sender)

        available = [profile for profile in profiles if profile not in accepted]  # all the available profile to invite
        print(available)
        return available

    def get_all_profiles(self, me):
        """gets all the profiles that are in the system excluding our own"""

        profiles = Profile.objects.all().exclude(user=me)
        return profiles


class Profile(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # every user will have his own profile/every time the user is deleted the profile is deleted as well
    bio = models.TextField(default='no bio ...', max_length=300)
    email = models.EmailField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    avatar = models.ImageField(default='avatar.png', upload_to='avatars/')  # profile picture
    # install pillow
    # create media_root
    # find avatar.png
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    slug = models.SlugField(unique=True, blank=True)
    # slug is base on first name and last name if they are provided otherwise slug is made out of the user
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    objects = ProfileManager()

    def __str__(self):
        return '{}-{}'.format(self.user.username, self.created.strftime(('%d-%m-%Y')))

    def get_absolute_url(self):
        return reverse("profiles:profile-detail-view", kwargs={"slug": self.slug})

    def get_friends(self):
        return self.friends.all()

    def get_friends_no(self):
        return self.friends.all().count()

    def get_posts_no(self):
        # instead of author_set.all() we wrote posts.all() because author verbose_name is posts
        return self.posts.all().count()

    def get_all_authors_posts(self):
        return self.posts.all()

    def get_likes_given_no(self):
        likes = self.like_set.all()
        total_liked = 0
        for item in likes:
            if item.value == 'Like':
                total_liked += 1
        return total_liked

    def get_likes_received_no(self):
        """this function counts all likes of a particular post"""
        posts = self.posts.all()  # gets all posts of a particular profile
        total_liked = 0
        for item in posts:
            total_liked += item.liked.all().count()
        return total_liked

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial_first_name = self.first_name
        self.__initial_last_name = self.last_name

    def save(self, *args, **kwargs):
        """this function is for making slug for users , Ones whose first and last name are similar
        and for ones who do not have first name and last name ,if a user does not have first and last name,
        his slug is made based on user. for making unique slug we used  get_random_code() function which is
        defined at utils.py"""
        ex = False
        to_slug = self.slug
        if self.first_name != self.__initial_first_name or self.last_name != self.__initial_last_name or self.slug == "":
            if self.first_name and self.last_name:
                to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
                ex = Profile.objects.filter(slug=to_slug).exists()
                while ex:
                    to_slug = slugify(to_slug + " " + str(get_random_code()))
                    ex = Profile.objects.filter(slug=to_slug).exists()
            else:
                to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)


STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)


class RelationshipManager(models.Manager):

    def invitation_received(self, receiver):
        """shows all the invitation we received from different users and the receiver is going to be our selves"""
        # we passed the profile as the receiver because the receiver is foreign key to  our profile
        # instead of writing  a view like Relationship.objects.invitation_receiver(myprofile) we wrote a model#??
        qs = Relationship.objects.filter(receiver=receiver, status='send')
        # status chosen from STATUS_ChOICES
        # if the receiver accepts the invitation it no longer exists
        return qs


class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    # who sends invitation
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    # who receives the invitation
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    # whether it is sent,accepted,ignored or deleted
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    objects = RelationshipManager()

    def __str__(self):
        return '{}-{}-{}'.format(self.sender, self.receiver, self.status)
