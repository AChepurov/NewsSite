from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        postR = self.post_set.aggregate(postRating=Sum('ratingPost'))
        pRat = 0
        pRat += postR.get('postRating')

        comR = self.authorUser.comment_set.aggregate(comRating=Sum('commentRating'))
        cRat = 0
        cRat += comR.get('comRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    categoryPost = models.CharField(max_length=64, unique=True)

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья')
    )
    postType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    creationMoment = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    titlePost = models.CharField(max_length=128)
    textPost = models.TextField()
    ratingPost = models.SmallIntegerField(default=0)

    def like(self):
        self.ratingPost += 1
        self.save()

    def dislike(self):
        self.ratingPost -= 1
        self.save()

    def preview(self):
        return self.textPost[0:123] + '...'


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment = models.ForeignKey(Post, on_delete=models.CASCADE)
    UserComment = models.ForeignKey(User, on_delete=models.CASCADE)
    commentText = models.TextField(max_length=1024)
    commentMoment = models.DateTimeField(auto_now_add=True)
    commentRating = models.SmallIntegerField(default=0)


    def like(self):
        self.commentRating += 1
        self.save()

    def dislike(self):
        self.commentRating -= 1
        self.save()

