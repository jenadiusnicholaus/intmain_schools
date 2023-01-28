from ckeditor_uploader.fields import RichTextUploadingField
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

# Create your models here.
from django.db.models import URLField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from imagekit.models import ImageSpecField
from pilkit.processors import Thumbnail
from django.conf import settings
from django.contrib.auth.models import User
from mdeditor.fields import MDTextField
from django.urls import reverse


from markdownfield.models import MarkdownField, RenderedMarkdownField
from markdownfield.validators import VALIDATOR_STANDARD


STATUS = (
    ('not_start', 'No Started'),
    ('started', 'Started'),
    ('reviewed', 'reviewed'),
    ('done', 'Done'),
    ('incomplete', 'Incomplate'),
)

class Module(models.Model):
    id = models.BigAutoField(primary_key=True)
    module_name = models.CharField(max_length=255, blank=False, null=False, unique=True)
    module_description = MDTextField(null= True)
    order_id = models.IntegerField(blank=False, null=False, default=1)
    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)
    icon = models.ImageField(default='', blank=True, upload_to='module_icons')
    icon_medium = ImageSpecField(source='icon',
                                 processors=[Thumbnail(200, 100)],
                                 format='JPEG',
                                 options={'quality': 60})
    icon_small = ImageSpecField(source='icon',
                                processors=[Thumbnail(100, 50)],
                                format='JPEG',
                                options={'quality': 60}
                                )
    icon_extra_small = ImageSpecField(source='icon',
                                      processors=[Thumbnail(72, 36)],
                                      format='JPEG',
                                      options={'quality': 60}
                                      )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "01. module"
        verbose_name_plural = "01. Module"

    def __str__(self):
        return f' {str(self.module_name)} '

    def save(self, *args, **kwargs):
        unique_id = get_random_string(length=8)
        combined_slug = f' {str(self.module_name)}-{str(unique_id)}'
        self.slug = slugify(combined_slug)
        return super(Module, self).save(*args, **kwargs)

class Weeks(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, blank=False, null=True, related_name='module_week',)

    author = models.ForeignKey(User, on_delete= models.CASCADE, null = True)
    id = models.BigAutoField(primary_key=True)
    week_number = models.CharField(max_length=255, blank=False, null=True)
    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)
    week_description = models.CharField(max_length=255, blank=True, null=True)
    order_id = models.IntegerField(blank=False, null=False, default=1)
    icon = models.ImageField(default='', blank=True, upload_to='weeks_icons')
    icon_medium = ImageSpecField(source='icon',
                                 processors=[Thumbnail(200, 100)],
                                 format='JPEG',
                                 options={'quality': 60})
    icon_small = ImageSpecField(source='icon',
                                processors=[Thumbnail(100, 50)],
                                format='JPEG',
                                options={'quality': 60}
                                )
    icon_extra_small = ImageSpecField(source='icon',
                                      processors=[Thumbnail(72, 36)],
                                      format='JPEG',
                                      options={'quality': 60}
                                      )

    status = models.CharField(default='not_start', max_length=20, choices=STATUS, null=True, )
    created_at = models.DateTimeField(auto_now_add=True, null= True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "02. Weeks"
        verbose_name_plural = "02. Weeks"

    def __str__(self):
        return f'Week No: {str(self.week_number )} -Module Name: {self.module.module_name}'

    def save(self, *args, **kwargs):
        unique_id = get_random_string(length=8)
        combined_slug = f' {str(self.week_number)}-{str(unique_id)}'
        self.slug = slugify(combined_slug)
        return super(Weeks, self).save(*args, **kwargs)


@receiver(post_save, sender=Weeks)
def create_or_update_class_module(sender, instance, created, **kwargs):
    # for each module, add class in the table of moduleWeeModuleWeek
    if created:
        try:
            module_list = Module.objects.order_by('created_at')
            for module in module_list:
                item_obj, item_created = Weeks.objects.update_or_create(Weeks=instance, module=module)
        except Exception as ex:
            print(ex)
            pass




# @receiver(post_save, sender=Module)
# def create_or_update_module_week(sender, instance, created, **kwargs):
#     # for each class, add module in the table of moduleWeeModuleWeek
#     if created:
#         try:
#             Weeks_list = Weeks.objects.order_by('created_at')
#             for Weeks in Weeks_list:
#                 item_obj, item_created = ModuleWeek.objects.update_or_create(Weeks=Weeks, module=instance)
#         except Exception as ex:
#             # print(ex)
#             pass



class Topics(models.Model):
    id = models.BigAutoField(primary_key=True)
    module_week = models.ForeignKey(Weeks, on_delete=models.CASCADE, blank=False, null=True,
                                      related_name='related_topics')
    topic_name = models.CharField(max_length=255, blank=False, null=False)
    order_id = models.IntegerField(blank=False, null=False, default=1)
    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)
    icon = models.ImageField(default='', blank=True, upload_to='topics_icons')
    icon_medium = ImageSpecField(source='icon',
                                 processors=[Thumbnail(200, 100)],
                                 format='JPEG',
                                 options={'quality': 60})
    icon_small = ImageSpecField(source='icon',
                                processors=[Thumbnail(100, 50)],
                                format='JPEG',
                                options={'quality': 60}
                                )
    icon_extra_small = ImageSpecField(source='icon',
                                      processors=[Thumbnail(72, 36)],
                                      format='JPEG',
                                      options={'quality': 60}
                                      )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "03. Topic"
        verbose_name_plural = verbose_name
        unique_together = ('module_week', 'topic_name')

    def __str__(self):
        return f' {str(self.module_week)}  - {str(self.topic_name)} '

    def save(self, *args, **kwargs):
        unique_id = get_random_string(length=8)
        combined_slug = f' {str(self.topic_name)}-{str(unique_id)}'
        self.slug = slugify(combined_slug)
        return super(Topics, self).save(*args, **kwargs)

    @property
    def topic_name_first_letter(self):
         if self.topic_name:
            return self.topic_name[0]



class Activity(models.Model):
    id = models.BigAutoField(primary_key=True)
    topic = models.ForeignKey(Topics, on_delete=models.CASCADE, blank=False, null=True, related_name="activity_set")

    # notes = RichTextUploadingField(blank=False, null=False)
    Activity = MDTextField(null= True)
    status = models.BooleanField(default='not_start', choices=STATUS, null=True, )
    status = models.CharField(choices=STATUS, blank=False, null=False, default='draft', max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "05. Activity"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f' {str(self.topic.topic_name)}  :  {str(self.topic.id)}'




class ModuleEnrollemnet(models.Model):
    ENROLMENT_STATUS = (
        ('full_enrolled', 'Full enrolled'),
        ('partial_enrolled', 'Partial enrolled'),
    )
    modules = models.ManyToManyField(Module, related_name='enroled_module_set')
    user =  models.ForeignKey(User, related_name='enroled_user', on_delete= models.SET_NULL, null =True)
    enrollement_status = models.CharField(max_length=20, choices=ENROLMENT_STATUS)
   
    class Meta:
        verbose_name = "6: ModuleEnrolemnet"
        verbose_name_plural = "ModuleEnrolemnets"

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("moduleEnrolemnet_detail", kwargs={"pk": self.pk})


