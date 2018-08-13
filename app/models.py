from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField
#import collections

class Expertise(models.Model):
    expertise = models.CharField(max_length=32, blank=True, unique=True)
"""
    majority_types = (
        ('MATH', 'math'),
        ('COMPUTER_SCIENCE', 'computer_science'),
        ('ENGLISH', 'english')
    )
    majorities = (choices=majority_types)
"""

class Friend(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='friend', unique=True)

"""
class ExpectedFriend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend', unique=True)

class FriendRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend', unique=True)
"""

class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    expertises = models.ManyToManyField(Expertise)

    friends = models.ManyToManyField(Friend, related_name='friend')

    expected_friends = models.ManyToManyField(Friend, related_name='expected_friend')

    friend_requests = models.ManyToManyField(Friend, related_name='friend_request')
    
    followers = models.ManyToManyField(Friend, related_name='follower')

    followings = models.ManyToManyField(Friend, related_name='following')

    star_givings = models.ManyToManyField(Friend, related_name='star_giving')

    star_givers = models.ManyToManyField(Friend, related_name='star_giver')

    class Meta:
        verbose_name = 'User Profile'

    def __str__(self):
        return "{}".format(self.user.__str__())


class QuestionForm(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_form')

    title = models.CharField('Title', max_length=128)

    content = models.CharField('Content', max_length=10000, blank=True)

    create_date = models.DateTimeField('Create modified')
    
    mod_date = models.DateTimeField('Last modified', auto_now=True)

    answer_number = models.IntegerField('Answer Number', default=0)
    
    comment_number = models.IntegerField('Comment Number', default=0)
    
    expertises = models.ManyToManyField(Expertise)

    resolved = models.BooleanField('Resovled', default=False)

    class Meta:
        verbose_name = 'Question Form'

    def __str__(self):
        return "{}".format(self.__str__())

class AnswerForm(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer_form')

    question = models.ForeignKey(QuestionForm, on_delete=models.CASCADE, related_name='answer_form')

    content = models.CharField('Content', max_length=10000, blank=True)

    create_date = models.DateTimeField('Create modified')
    
    mod_date = models.DateTimeField('Last modified', auto_now=True)

    comment_number = models.IntegerField('Comment Number', default=0)
    
    class Meta:
        verbose_name = 'Answer Form'

    def __str__(self):
        return "{}".format(self.__str__())

class CommentForm(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_form')

    question = models.ForeignKey(QuestionForm, on_delete=models.CASCADE, related_name='comment_form')

    answer = models.ForeignKey(AnswerForm, on_delete=models.CASCADE, related_name='comment_form', default=-1)
    
    content = models.CharField('Content', max_length=10000, blank=True)

    create_date = models.DateTimeField('Create modified')
    
    mod_date = models.DateTimeField('Last modified', auto_now=True)
    
    class Meta:
        verbose_name = 'Comment Form'

    def __str__(self):
        return "{}".format(self.__str__())


