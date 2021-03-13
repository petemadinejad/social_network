from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Relationship


# is used for creating profile automatically
@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):  # created is a boolean value
    if created:
        Profile.objects.create(user=instance)


# is used for adding friends automatically
@receiver(post_save, sender=Relationship)
def post_save_add_friends(sender, instance, created, **kwargs):
    sender_ = instance.sender
    receiver_ = instance.receiver
    if instance.status == 'accepted':
        sender_.friends.add(receiver_.user)
        receiver_.friends.add(sender_.user)
        sender_.save()
        receiver_.save()


@receiver(pre_delete, sender=Relationship)  # signal is pre_delete and receiver is Relationship
def pre_delete_remove_from_friends(sender, instance, **kwargs):
    """before the relationship get deleted,it is removed from friends"""
    # here sender is instance of Relationship
    sender = instance.sender
    receiver = instance.receiver
    sender.friends.remove(receiver.user)
    receiver.friends.remove(sender.user)
    sender.save()
    receiver.save()
