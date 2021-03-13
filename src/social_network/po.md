1.profiles

    -Profile
    (Django signals is used and each user has his own profile)

    -Relationship
     (helps manage relation: 1. Sender (who send the invitaion)  2.Receiver(who receives the invitation  
      3. what is the status of this relation ( it is sent or waiting for acceptence or it is already accepted 
      or it is rejected,also status of a friends which was removed from friends list and also we are removed 
      his friends list)
    **for making profile automatically we used signals(signals in Django allow us to send information to some 
    specific application om event that took place( in Django often we use Signals while creating or modifying 
    one of the models to simply execute some action
    *sinals ==> communication between user and profile

2.posts
    -Post
    -Comment
    -Like/unlike
    

3.allauth(authentication)
