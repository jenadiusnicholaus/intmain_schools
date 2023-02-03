from django.contrib import admin

# Register your models here.
# from lcms_primary.models import Weeks, Module, Topics, YoutubeVideos, DocumentLinks, Activity, Languages, topics
from django.contrib.admin import display
from django.urls import resolve
from django.utils.safestring import mark_safe
from imagekit.admin import AdminThumbnail

from .forms import ContentActivityForm, SupervisorActivityForm, DefaultActivityForm
from .models import  *


class WeeksInline(admin.TabularInline):
    model = Weeks



class ModuleInline(admin.TabularInline):
    model = Module
    extra = 4


class TopicsInline(admin.TabularInline):
    model = Topics


class ActivityInline(admin.TabularInline):
    model = Activity
    extra = 1

@admin.register(ModuleCategory)
class ModeuleCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'category_name',)
    thumbnail = AdminThumbnail(image_field='icon_small')
    list_display_links = ('category_name','id')
    search_fields = ('id',
                     'category_name',
                  
                     )
    
    ordering = ['id', 'category_name']
    prepopulated_fields = {'slug': ('category_name',)}
    list_per_page = 10
    inlines = [ModuleInline]

@admin.register(Weeks)
class WeeksAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'author', 'thumbnail', 'slug', 'week_number', 'order_id',  'week_description', 'status', 'created_at', 'updated_at',)
    thumbnail = AdminThumbnail(image_field='icon_small')
    list_display_links = ('week_number','author')
    search_fields = ('id',
                     'week_number',
                     'week_description',
                     )
    
    ordering = ['id', 'week_number']
    list_filter = ['status',"author", 'week_number', 'created_at', 'updated_at', ]
    prepopulated_fields = {'slug': ('week_number',)}
    list_per_page = 10
    inlines = [TopicsInline]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'thumbnail', 'slug', 'module_name',  'order_id', 'created_at',)
    thumbnail = AdminThumbnail(image_field='icon_small')
    list_display_links = ('module_name',)
    search_fields = ('id',
                     'module_name',
                     'module_description',
                     )
    ordering = ['-id', ]
    list_filter = ['module_name', 'created_at', 'updated_at']
    list_per_page = 10
    prepopulated_fields = {'slug': ('module_name',)}
    inlines = [WeeksInline]

@admin.register(Topics)
class TopicsAdmin(admin.ModelAdmin):
    list_display = ('id','estmated_accomplishmet_time', 'thumbnail', 'module', 'module_week', 'topic_name', 'order_id',  'created_at',)
    thumbnail = AdminThumbnail(image_field='icon_small')
    list_display_links = ('topic_name',)
    search_fields = ('id',
                     'module_week__module__module_name',
                     'module_week__module__module_description',
                     'module_week___week_number',
                     'odele_class__week_description',
                     'topic_name',
                     )
    ordering = ['-id', ]
    list_filter = ['module_week__week_number', 'module_week__module__module_name', 'created_at', ]
    list_per_page = 10
    
   
    prepopulated_fields = {'slug': ('topic_name',)}

    @display(ordering='module_week__week_number', description='Weeks')
    def Weeks(self, obj):
        return obj.module_week.week_number

    @display(ordering='module_week__module__module_name', description='Module')
    def module(self, obj):
        return obj.module_week.module.module_name



@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'module', 'topic', 'topic', 'status', 'created_at')
    # list_display_links = ('topic_name',)
    search_fields = ('id',
                     'topic__module_week__module__module_name',
                     'topic__module_week__module__module_description',
                     'topic__module_week__week_number',
                     'topic__module_week__week_description',
                     'topic__topic_name',
                     'topic_name',
                     )

    ordering = ['-created_at', '-id', ]
    list_filter = ['status', 'topic__module_week__week_number', 'topic__module_week__module__module_name',
                   'created_at', ]
    list_per_page = 10
   


    def get_form(self, request, obj=None, change=False, **kwargs):
        if request.user.groups.filter(name='Primary Content Manager') and obj is None:
            return ContentActivityForm
        elif request.user.groups.filter(name='Primary Supervisor') and obj is None:
            return DefaultActivityForm
        elif request.user.groups.filter(name='Primary Content Manager') and (
                obj.status == 'draft' or obj.status == 'return_for_amendment'):
            return ContentActivityForm
        elif request.user.groups.filter(name='Primary Supervisor') and (
                obj.status == 'send_for_approval' or obj.status == 'approved'):
            return SupervisorActivityForm

        elif request.user.is_superuser:
            return super().get_form(request, obj, change, **kwargs)
        else:
            return DefaultActivityForm

    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name='Primary Supervisor') and obj is not None and (
                obj.status == 'draft' or obj.status == 'return_for_amendment'):
            return [ 'activity', 'status', 'activity_display']
        elif request.user.groups.filter(name='Primary Content Manager') and obj is not None and (
                obj.status == 'send_for_approval' or obj.status == 'approved'):
            returnlist_display_links = ('topic_name',) [ 'activity', 'status', 'activity_display']
        elif request.user.is_superuser:
            return ['activity_display', super().get_readonly_fields(request, obj)]
        else:
            return ['activity_display', super().get_readonly_fields(request, obj)]

    def activity_display(self, obj):
        return mark_safe(obj.activity)

    activity_display.short_description = 'activity Display'

    @display(ordering='topic__topic__module_week__week_number', description='Weeks')
    def Weeks(self, obj):
        return obj.topic.topic.module_week.week_number

    @display(ordering='topic__topic__module_week__module__module_name', description='Module')
    def module(self, obj):
        return obj.topic.module_week.module.module_name

    @display(ordering='topic__topic_name', description='Topic')
    def topic(self, obj):
        return obj.topic.topic_name

    @display(ordering='topic__topic_name', description='topic')
    def topic(self, obj):
        return obj.topic.topic_name

    @display(ordering='topic_name', description='topic')
    def topic_name(self, obj):
        return obj.topic.topic_name


class HasAnswerFilter(admin.SimpleListFilter):
    title = 'Has Answer'
    parameter_name = 'has_answer'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes'),
            ('no', 'No'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if not value:
            return queryset
        if value.lower() == 'yes':
            return queryset.filter(respective_answer__isnull=False)
        elif value.lower() == 'no':
            return queryset.filter(respective_answer__isnull=True)

@admin.register(ModuleEnrollemnet)
class ModuleEnrollementAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', )
    list_display_links = ('id','user',)
    # inlines = [ModuleInline]

  