import datetime

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import User

from mysite.storage_backends import PublicMediaStorage, PrivateMediaStorage


class Borough(models.Model):
    """ Represents a single Borough. """
    objects = models.Manager()

    title = models.CharField(
        max_length=settings.BOROUGH_TITLE_MAX_LENGTH, unique=True, default="Title of your page.")
    author = models.ForeignKey(
        User, on_delete=models.PROTECT, help_text="The user that posted this article.")
    slug = models.CharField(max_length=settings.BOROUGH_TITLE_MAX_LENGTH, blank=True, editable=False,
                            help_text="Unique URL path to access this borough's page. Generated by the system.")

    created = models.DateTimeField(
        auto_now_add=True, help_text="The date and time this page was created. Automatically generated when the model saves.")
    modified = models.DateTimeField(
        auto_now=True, help_text="The date and time this page was updated. Automatically generated when the model updates.")

    zipcode = models.IntegerField(
        default=9401, blank=False, help_text="Add the zipcode of this borough")
    tract = models.CharField(
        max_length=10, default='010100', blank=False, help_text="Add the tract of this borough")

    content = models.TextField(default="Write the content of your page here.")
    sources = models.URLField(null=True, blank=True)

    main_img = models.ImageField(upload_to='main_images/', null=True)
    main_img2 = models.ImageField(upload_to='main_images/'+str(slug), null=True)
    main_img3 = models.ImageField(upload_to='main_images/'+str(slug), null=True)
    main_img4 = models.ImageField(upload_to='main_images/'+str(slug), null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """ Returns a fully-qualified path for a page (/my-new-page). """
        path_components = {'slug': self.slug}
        return reverse('borough-details', kwargs=path_components)

    def save(self, *args, **kwargs):
        """ Creates a URL safe slug automatically when a new a page is created. """
        self.slug = slugify(self.title, allow_unicode=True)
        # Call save on the superclass.
        return super(Borough, self).save(*args, **kwargs)


class Photo(models.Model):
    """ Represents a single Photo. """
    objects = models.Manager()
    created = models.DateTimeField(
        auto_now_add=True, help_text="The date and time this page was created. Automatically generated when the model saves.")
    approved = models.BooleanField(default=False)
    borough = models.ForeignKey(Borough, default=None, on_delete=models.PROTECT)

    image = models.ImageField(storage=PublicMediaStorage(), null=False)
    # private = models.ImageField(storage=PrivateMediaStorage(), null=False)
    content = models.TextField(default="Write the content of your page here.")
    votes = models.IntegerField(default=0)

    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    email = models.EmailField(max_length=200)

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.created <= now
    was_published_recently.admin_order_field = 'created'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def get_absolute_url(self):
        """ Redirects to the borough this photo was uploaded for. """
        path_components = {'slug': self.borough.slug}
        return reverse('borough-details', kwargs=path_components)

    def save(self, *args, **kwargs):
        """ Creates a URL safe slug automatically when a new a page is created. """

        # Call save on the superclass.
        return super(Photo, self).save(*args, **kwargs)
