from django.contrib.auth.models import User
from django.db import models

from ckeditor_uploader.fields import RichTextUploadingField

from django.utils.html import strip_tags


class Post(models.Model):

    TANK = 'TK'
    HEALER = 'HL'
    DAMAGE_DEALER = 'DD'
    VENDOR = 'VR'
    GUILD_MASTER = 'GM'
    QUEST_GIVER = 'QG'
    BLACKSMITH = 'BS'
    SKINNER = 'SN'
    POTION_MASTER = 'PM'
    SPELL_MASTER = 'SP'

    CATEGORIES = [
        (TANK, 'Tank'),
        (HEALER, 'Healer'),
        (DAMAGE_DEALER, 'Damage dealer'),
        (VENDOR, 'Vendor'),
        (GUILD_MASTER, 'Guild master'),
        (QUEST_GIVER, 'Quest giver'),
        (BLACKSMITH, 'Blacksmith'),
        (SKINNER, 'Skinner'),
        (POTION_MASTER, 'Potion master'),
        (SPELL_MASTER, 'Spell master'),
    ]

    title = models.CharField(max_length=128)
    content = RichTextUploadingField()
    date_creation = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=2, choices=CATEGORIES)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def preview(self):
        return strip_tags(self.content)

    def __str__(self):
        return f'{self.title}'


class Comment(models.Model):
    text = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    is_accept = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
