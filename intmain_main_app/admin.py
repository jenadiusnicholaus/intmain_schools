from django.contrib import admin

# Register your models here.
# from lcms_primary.models import Classes, Subjects, Topics, YoutubeVideos, DocumentLinks, Notes, Languages, SubTopics
from django.contrib.admin import display
from django.urls import resolve
from django.utils.safestring import mark_safe
from imagekit.admin import AdminThumbnail

from .forms import ContentNotesForm, SupervisorNotesForm, DefaultNotesForm
from .models import ChatRoom, Classes, Messages, Subjects, Topics, Notes, SubjectClass, SubTopics, \
    MultipleChoicesQuestions, \
    MultipleChoicesOptions, MultipleChoicesAnswers, TrueOrFalseQuestions, ShortAnswerQuestions, Segments, \
    QuizMultipleChoicesAnswers, QuizMultipleChoicesOptions, \
    QuizMultipleChoicesQuestions, QuizTrueOrFalse, QuizShortAnswer, QuizMatchingItem, QuizMatchingItemAnswers, \
    QuizMatchingItemQuestions, QuizMatchingItemOptions, TestMatchingItem, TestMatchingItemAnswers, \
    TestMatchingItemOptions, TestMatchingItemQuestions


class ClassesInline(admin.TabularInline):
    model = Classes


class SubjectClassInline(admin.TabularInline):
    model = SubjectClass
    extra = 5


class TopicsInline(admin.TabularInline):
    model = Topics


class SubTopicsInline(admin.TabularInline):
    model = SubTopics
    extra = 5


class SegmentsInline(admin.TabularInline):
    model = Segments
    extra = 2


class NotesInline(admin.TabularInline):
    model = Notes
    extra = 1


class MessagesInline(admin.TabularInline):
    model = Messages
    extra = 1


class ChoicesInline(admin.TabularInline):
    model = MultipleChoicesOptions
    extra = 5


class AnswersInline(admin.TabularInline):
    model = MultipleChoicesAnswers
    extra = 1

    def get_formset(self, request, obj=None, **kwargs):
        """
        Override the formset function in order to remove the add and change buttons beside the foreign key pull-down
        menus in the inline.
        """
        formset = super(AnswersInline, self).get_formset(request, obj, **kwargs)
        form = formset.form
        widget = form.base_fields['choice'].widget
        widget.can_add_related = False
        widget.can_change_related = False
        widget.can_delete_related = False
        return formset

    def get_parent_object_from_request(self, request):
        """
        Returns the parent object from the request or None.

        Note that this only works for Inlines, because the `parent_model`
        is not available in the regular admin.ModelAdmin as an attribute.
        """
        resolved = resolve(request.path_info)
        if resolved.kwargs:
            return self.parent_model.objects.get(pk=resolved.kwargs["object_id"])
        return None

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):

        field = super(AnswersInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == 'choice':
            if request:
                if self.get_parent_object_from_request(request) is not None:
                    # MEANING IT IS FIRST SAVE, IGNORE VALUES PROMPT FOR SAVE AND CONTINUE EDITING
                    # SO THAT IT CAPTURES SAVED VALUES
                    question = self.get_parent_object_from_request(request).question
                    field.queryset = field.queryset.filter(question__question=question)
                else:
                    field.queryset = field.queryset.none()
        return field


class QuizChoicesInline(admin.TabularInline):
    model = QuizMultipleChoicesOptions
    min_num = 4
    extra = 0


class QuizAnswersInline(admin.TabularInline):
    model = QuizMultipleChoicesAnswers
    extra = 1

    def get_formset(self, request, obj=None, **kwargs):
        """
        Override the formset function in order to remove the add and change buttons beside the foreign key pull-down
        menus in the inline.
        """
        formset = super(QuizAnswersInline, self).get_formset(request, obj, **kwargs)
        form = formset.form
        widget = form.base_fields['choice'].widget
        widget.can_add_related = False
        widget.can_change_related = False
        widget.can_delete_related = False
        return formset

    def get_parent_object_from_request(self, request):
        """
        Returns the parent object from the request or None.

        Note that this only works for Inlines, because the `parent_model`
        is not available in the regular admin.ModelAdmin as an attribute.
        """
        resolved = resolve(request.path_info)
        if resolved.kwargs:
            return self.parent_model.objects.get(pk=resolved.kwargs["object_id"])
        return None

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):

        field = super(QuizAnswersInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == 'choice':
            if request:
                if self.get_parent_object_from_request(request) is not None:
                    # MEANING IT IS FIRST SAVE, IGNORE VALUES PROMPT FOR SAVE AND CONTINUE EDITING
                    # SO THAT IT CAPTURES SAVED VALUES
                    question = self.get_parent_object_from_request(request).question
                    field.queryset = field.queryset.filter(question__question=question)
                else:
                    field.queryset = field.queryset.none()
        return field


class QuizMatchingItemInline(admin.TabularInline):
    model = QuizMatchingItem


class QuizMatchingItemQuestionsInline(admin.TabularInline):
    model = QuizMatchingItemQuestions
    min_num = 2
    extra = 0


class QuizMatchingItemOptionsInline(admin.TabularInline):
    model = QuizMatchingItemOptions
    min_num = 2
    extra = 0


class QuizMatchingItemAnswersInline(admin.TabularInline):
    model = QuizMatchingItemAnswers
    extra = 0

    def get_formset(self, request, obj=None, **kwargs):
        """
        Override the formset function in order to remove the add and change buttons beside the foreign key pull-down
        menus in the inline.
        """
        formset = super(QuizMatchingItemAnswersInline, self).get_formset(request, obj, **kwargs)
        form = formset.form
        widget = form.base_fields['question'].widget
        widget.can_add_related = False
        widget.can_change_related = False
        widget.can_delete_related = False
        return formset

    def get_parent_object_from_request(self, request):
        """
        Returns the parent object from the request or None.

        Note that this only works for Inlines, because the `parent_model`
        is not available in the regular admin.ModelAdmin as an attribute.
        """
        resolved = resolve(request.path_info)
        if resolved.kwargs:
            return self.parent_model.objects.get(pk=resolved.kwargs["object_id"])
        return None

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):

        field = super(QuizMatchingItemAnswersInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == 'question' or db_field.name == 'answer':
            if request:
                if self.get_parent_object_from_request(request) is not None:
                    # MEANING IT IS FIRST SAVE, IGNORE VALUES PROMPT FOR SAVE AND CONTINUE EDITING
                    # SO THAT IT CAPTURES SAVED VALUES
                    matching_item = self.get_parent_object_from_request(request)
                    field.queryset = field.queryset.filter(matching_item=matching_item)
                else:
                    field.queryset = field.queryset.none()
        return field


class TestMatchingItemQuestionsInline(admin.TabularInline):
    model = TestMatchingItemQuestions
    min_num = 3
    extra = 0


class TestMatchingItemOptionsInline(admin.TabularInline):
    model = TestMatchingItemOptions
    min_num = 3
    extra = 0


class TestMatchingItemAnswersInline(admin.TabularInline):
    model = TestMatchingItemAnswers
    extra = 0

    def get_formset(self, request, obj=None, **kwargs):
        """
        Override the formset function in order to remove the add and change buttons beside the foreign key pull-down
        menus in the inline.
        """
        formset = super(TestMatchingItemAnswersInline, self).get_formset(request, obj, **kwargs)
        form = formset.form
        widget = form.base_fields['question'].widget
        widget.can_add_related = False
        widget.can_change_related = False
        widget.can_delete_related = False
        return formset

    def get_parent_object_from_request(self, request):
        """
        Returns the parent object from the request or None.

        Note that this only works for Inlines, because the `parent_model`
        is not available in the regular admin.ModelAdmin as an attribute.
        """
        resolved = resolve(request.path_info)
        if resolved.kwargs:
            return self.parent_model.objects.get(pk=resolved.kwargs["object_id"])
        return None

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):

        field = super(TestMatchingItemAnswersInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == 'question' or db_field.name == 'answer':
            print('hello')
            # if request:
            #     if self.get_parent_object_from_request(request) is not None:
            #         # MEANING IT IS FIRST SAVE, IGNORE VALUES PROMPT FOR SAVE AND CONTINUE EDITING
            #         # SO THAT IT CAPTURES SAVED VALUES
            #         matching_item = self.get_parent_object_from_request(request)
            #         field.queryset = field.queryset.filter(matching_item=matching_item)
            #     else:
            #         field.queryset = field.queryset.none()
        return field


@admin.register(Classes)
class ClassesAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'thumbnail', 'slug', 'class_name', 'order_id',  'class_description', 'active_status', 'created_at', 'updated_at',)
    thumbnail = AdminThumbnail(image_field='icon_small')
    list_display_links = ('class_name',)
    search_fields = ('id',
                     'class_name',
                     'class_description',
                     )
    ordering = ['id', 'class_name']
    list_filter = ['active_status', 'class_name', 'created_at', 'updated_at', ]
    prepopulated_fields = {'slug': ('class_name',)}
    list_per_page = 10
    inlines = [SubjectClassInline]


@admin.register(Subjects)
class SubjectsAdmin(admin.ModelAdmin):
    list_display = ('id', 'thumbnail', 'slug', 'subject_name',  'order_id', 'created_at',)
    thumbnail = AdminThumbnail(image_field='icon_small')
    list_display_links = ('subject_name',)
    search_fields = ('id',
                     'subject_name',
                     'subject_description',
                     )
    ordering = ['-id', ]
    list_filter = ['subject_name', 'created_at', 'updated_at']
    list_per_page = 10
    prepopulated_fields = {'slug': ('subject_name',)}


@admin.register(Topics)
class TopicsAdmin(admin.ModelAdmin):
    list_display = ('id', 'thumbnail', 'classes', 'subject', 'subject_class', 'topic_name', 'order_id',  'created_at',)
    thumbnail = AdminThumbnail(image_field='icon_small')
    list_display_links = ('topic_name',)
    search_fields = ('id',
                     'subject_class__subject__subject_name',
                     'subject_class__subject__subject_description',
                     'subject_class__classes__class_name',
                     'subject_class__classes__class_description',
                     'topic_name',
                     )
    ordering = ['-id', ]
    list_filter = ['subject_class__classes__class_name', 'subject_class__subject__subject_name', 'created_at', ]
    list_per_page = 10
    inlines = [SubTopicsInline]
    prepopulated_fields = {'slug': ('topic_name',)}

    @display(ordering='subject_class__classes__class_name', description='Classes')
    def classes(self, obj):
        return obj.subject_class.classes.class_name

    @display(ordering='subject_class__subject__subject_name', description='Subjects')
    def subject(self, obj):
        return obj.subject_class.subject.subject_name


@admin.register(SubTopics)
class SubTopicsAdmin(admin.ModelAdmin):
    list_display = ('id', 'thumbnail',   'classes',  'subject', 'topic_name',  'subtopic_name', 'order_id',  'created_at',)
    thumbnail = AdminThumbnail(image_field='icon_small')
    list_display_links = ('subtopic_name',)
    search_fields = ('id',
                     'topic__subject_class__subject__subject_name',
                     'topic__subject_class__subject__subject_description',
                     'topic__subject_class__classes__class_name',
                     'topic__subject_class__classes__class_description',
                     'topic__topic_name',
                     'subtopic_name',
                     )
    ordering = ['-id', ]
    list_filter = ['topic__subject_class__classes__class_name', 'topic__subject_class__subject__subject_name', 'created_at', ]
    list_per_page = 10
    inlines = [SegmentsInline]
    prepopulated_fields = {'slug': ('subtopic_name',)}

    @display(ordering='topic__subject_class__classes__class_name', description='Classes')
    def classes(self, obj):
        return obj.topic.subject_class.classes.class_name

    @display(ordering='topic__subject_class__subject__subject_name', description='Subjects')
    def subject(self, obj):
        return obj.topic.subject_class.subject.subject_name

    @display(ordering='topic__topic_name', description='Topic')
    def topic_name(self, obj):
        return obj.topic.topic_name


@admin.register(Segments)
class SegmentsAdmin(admin.ModelAdmin):
    list_display = ('id',  'classes',  'subject', 'topic_name',  'subtopic_name', 'segment_id', 'segment_name', 'created_at')
    list_display_links = ('subtopic_name', 'segment_id', 'segment_name', )
    search_fields = ('id',
                     'subtopic__topic__subject_class__subject__subject_name',
                     'subtopic__topic__subject_class__subject__subject_description',
                     'subtopic__topic__subject_class__classes__class_name',
                     'subtopic__topic__subject_class__classes__class_description',
                     'subtopic__topic__topic_name',
                     'subtopic__subtopic_name',
                     'segment_id',
                     'segment_name',
                     )

    ordering = ['-created_at', '-id', ]
    list_filter = ['subtopic__topic__subject_class__classes__class_name', 'subtopic__topic__subject_class__subject__subject_name',
                   'created_at', ]
    list_per_page = 10
    inlines = [NotesInline]

    @display(ordering='subtopic__topic__subject_class__classes__class_name', description='Classes')
    def classes(self, obj):
        return obj.subtopic.topic.subject_class.classes.class_name

    @display(ordering='subtopic__topic__subject_class__subject__subject_name', description='Subjects')
    def subject(self, obj):
        return obj.subtopic.topic.subject_class.subject.subject_name

    @display(ordering='subtopic__topic__topic_name', description='Topic')
    def topic_name(self, obj):
        return obj.subtopic.topic.topic_name

    @display(ordering='subtopic__subtopic_name', description='SubTopic')
    def subtopic_name(self, obj):
        return obj.subtopic.subtopic_name


@admin.register(Notes)
class NotesAdmin(admin.ModelAdmin):
    list_display = ('id', 'classes', 'subject', 'topic', 'subtopic', 'segment_name', 'status', 'created_at')
    list_display_links = ('segment_name',)
    search_fields = ('id',
                     'segment__subtopic__topic__subject_class__subject__subject_name',
                     'segment__subtopic__topic__subject_class__subject__subject_description',
                     'segment__subtopic__topic__subject_class__classes__class_name',
                     'segment__subtopic__topic__subject_class__classes__class_description',
                     'segment__subtopic__topic__topic_name',
                     'segment__subtopic__subtopic_name',
                     )

    ordering = ['-created_at', '-id', ]
    list_filter = ['status', 'segment__subtopic__topic__subject_class__classes__class_name', 'segment__subtopic__topic__subject_class__subject__subject_name',
                   'created_at', ]
    list_per_page = 10

    def get_form(self, request, obj=None, change=False, **kwargs):
        if request.user.groups.filter(name='Primary Content Manager') and obj is None:
            return ContentNotesForm
        elif request.user.groups.filter(name='Primary Supervisor') and obj is None:
            return DefaultNotesForm
        elif request.user.groups.filter(name='Primary Content Manager') and (
                obj.status == 'draft' or obj.status == 'return_for_amendment'):
            return ContentNotesForm
        elif request.user.groups.filter(name='Primary Supervisor') and (
                obj.status == 'send_for_approval' or obj.status == 'approved'):
            return SupervisorNotesForm

        elif request.user.is_superuser:
            return super().get_form(request, obj, change, **kwargs)
        else:
            return DefaultNotesForm

    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name='Primary Supervisor') and obj is not None and (
                obj.status == 'draft' or obj.status == 'return_for_amendment'):
            return ['segment', 'notes', 'status', 'notes_display']
        elif request.user.groups.filter(name='Primary Content Manager') and obj is not None and (
                obj.status == 'send_for_approval' or obj.status == 'approved'):
            return ['segment', 'notes', 'status', 'notes_display']
        elif request.user.is_superuser:
            return ['notes_display', super().get_readonly_fields(request, obj)]
        else:
            return ['notes_display', super().get_readonly_fields(request, obj)]

    def notes_display(self, obj):
        return mark_safe(obj.notes)

    notes_display.short_description = 'Notes Display'

    @display(ordering='segment__subtopic__topic__subject_class__classes__class_name', description='Classes')
    def classes(self, obj):
        return obj.segment.subtopic.topic.subject_class.classes.class_name

    @display(ordering='segment__subtopic__topic__subject_class__subject__subject_name', description='Subjects')
    def subject(self, obj):
        return obj.segment.subtopic.topic.subject_class.subject.subject_name

    @display(ordering='segment__subtopic__topic__topic_name', description='Topic')
    def topic(self, obj):
        return obj.segment.subtopic.topic.topic_name

    @display(ordering='segment__subtopic__subtopic_name', description='SubTopic')
    def subtopic(self, obj):
        return obj.segment.subtopic.subtopic_name

    @display(ordering='segment__segment_name', description='Segment')
    def segment_name(self, obj):
        return obj.segment.segment_name


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


@admin.register(QuizMultipleChoicesQuestions)
class QuizMultipleChoicesQuestionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'segment', 'question', 'has_answer', 'created_at')
    list_display_links = ('question',)
    search_fields = ('id',
                     'segment__subtopic__topic__subject_class__subject__subject_name',
                     'segment__subtopic__topic__subject_class__subject__subject_description',
                     'segment__subtopic__topic__subject_class__classes__class_name',
                     'segment__subtopic__topic__subject_class__classes__class_description',
                     'segment__subtopic__topic__topic_name',
                     'segment__subtopic__subtopic_name',
                     'question',
                     )

    ordering = ['-created_at', '-id', ]
    list_filter = [HasAnswerFilter,
                   'created_at', 'updated_at',
                   ]
    list_per_page = 10
    inlines = [QuizChoicesInline, QuizAnswersInline]

    def has_answer(self, obj):
        return QuizMultipleChoicesAnswers.objects.filter(question=obj).count() > 0

    has_answer.boolean = True


@admin.register(QuizTrueOrFalse)
class QuizTrueOrFalseAdmin(admin.ModelAdmin):
    list_display = ('id', 'segment', 'question', 'answer', 'created_at', 'updated_at')
    list_display_links = ('question',)
    search_fields = ('id',
                     'segment__subtopic__topic__subject_class__subject__subject_name',
                     'segment__subtopic__topic__subject_class__subject__subject_description',
                     'segment__subtopic__topic__subject_class__classes__class_name',
                     'segment__subtopic__topic__subject_class__classes__class_description',
                     'segment__subtopic__topic__topic_name',
                     'segment__subtopic__subtopic_name',
                     'question',
                     'answer',
                     )
    ordering = ['-id', ]
    list_filter = ['created_at', 'updated_at']
    list_per_page = 10


@admin.register(QuizShortAnswer)
class QuizShortAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'segment', 'question', 'answer', 'created_at')
    list_display_links = ('question',)
    search_fields = ('id',
                     'segment__subtopic__topic__subject_class__subject__subject_name',
                     'segment__subtopic__topic__subject_class__subject__subject_description',
                     'segment__subtopic__topic__subject_class__classes__class_name',
                     'segment__subtopic__topic__subject_class__classes__class_description',
                     'segment__subtopic__topic__topic_name',
                     'segment__subtopic__subtopic_name',
                     'question',
                     'answer',
                     )

    ordering = ['-created_at', '-id', ]
    list_filter = ['created_at', 'updated_at']
    list_per_page = 10


@admin.register(QuizMatchingItem)
class QuizMatchingItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'classes', 'subject', 'topic', 'subtopic', 'segment', 'created_at')
    list_display_links = ('segment',)
    search_fields = ('id',
                     'segment__subtopic__topic__subject_class__subject__subject_name',
                     'segment__subtopic__topic__subject_class__subject__subject_description',
                     'segment__subtopic__topic__subject_class__classes__class_name',
                     'segment__subtopic__topic__subject_class__classes__class_description',
                     'segment__subtopic__topic__topic_name',
                     'segment__subtopic__subtopic_name',
                     )

    ordering = ['-created_at', '-id', ]
    list_filter = ['created_at', 'updated_at']
    list_per_page = 10

    inlines = [QuizMatchingItemQuestionsInline, QuizMatchingItemOptionsInline, QuizMatchingItemAnswersInline]

    def classes(self, obj):
        return obj.segment.subtopic.topic.subject_class.classes.class_name

    def subject(self, obj):
        return obj.segment.subtopic.topic.subject_class.subject.subject_name

    def topic(self, obj):
        return obj.segment.subtopic.topic.topic_name

    def subtopic(self, obj):
        return obj.segment.subtopic.subtopic_name


@admin.register(MultipleChoicesQuestions)
class MultipleChoicesQuestionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'subtopic', 'question', 'has_answer', 'created_at')
    list_display_links = ('question',)
    search_fields = ('id',
                     'subtopic__topic__subject_class__subject__subject_name',
                     'subtopic__topic__subject_class__subject__subject_description',
                     'subtopic__topic__subject_class__classes__class_name',
                     'subtopic__topic__subject_class__classes__class_description',
                     'subtopic__topic__topic_name',
                     'question',
                     )

    ordering = ['-created_at', '-id', ]
    list_filter = [HasAnswerFilter,
                   'created_at', 'updated_at',
                   ]
    list_per_page = 10
    inlines = [ChoicesInline, AnswersInline]

    def has_answer(self, obj):
        return MultipleChoicesAnswers.objects.filter(question=obj).count() > 0

    has_answer.boolean = True


@admin.register(TrueOrFalseQuestions)
class TrueOrFalseQuestionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'subtopic', 'question', 'answer', 'created_at', 'updated_at')
    list_display_links = ('question',)
    search_fields = ('id',
                     'subtopic__topic__subject_class__subject__subject_name',
                     'subtopic__topic__subject_class__subject__subject_description',
                     'subtopic__topic__subject_class__classes__class_name',
                     'subtopic__topic__subject_class__classes__class_description',
                     'subtopic__topic__topic_name',
                     'question',
                     'answer',
                     )
    ordering = ['-id', ]
    list_filter = ['created_at', 'updated_at']
    list_per_page = 10


@admin.register(ShortAnswerQuestions)
class ShortAnswerQuestionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'subtopic', 'question', 'answer', 'created_at')
    list_display_links = ('question',)
    search_fields = ('id',
                     'subtopic__topic__subject_class__subject__subject_name',
                     'subtopic__topic__subject_class__subject__subject_description',
                     'subtopic__topic__subject_class__classes__class_name',
                     'subtopic__topic__subject_class__classes__class_description',
                     'subtopic__topic__topic_name',
                     'question',
                     'answer',
                     )

    ordering = ['-created_at', '-id', ]
    list_filter = ['created_at', 'updated_at']
    list_per_page = 10


#
@admin.register(TestMatchingItem)
class TestMatchingItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'classes', 'subject', 'topic', 'subtopic', 'created_at')
    list_display_links = ('subtopic',)
    search_fields = ('id',
                     'subtopic__topic__subject_class__subject__subject_name',
                     'subtopic__topic__subject_class__subject__subject_description',
                     'subtopic__topic__subject_class__classes__class_name',
                     'subtopic__topic__subject_class__classes__class_description',
                     'subtopic__topic__topic_name',
                     'subtopic__subtopic_name',
                     )

    ordering = ['-created_at', '-id', ]
    list_filter = ['created_at', 'updated_at']
    list_per_page = 10

    inlines = [TestMatchingItemQuestionsInline, TestMatchingItemOptionsInline, TestMatchingItemAnswersInline]

    def classes(self, obj):
        return obj.subtopic.topic.subject_class.classes.class_name

    def subject(self, obj):
        return obj.subtopic.topic.subject_class.subject.subject_name

    def topic(self, obj):
        return obj.subtopic.topic.topic_name

    def subtopic(self, obj):
        return obj.subtopic.subtopic_name


@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'message', 'created_at')
    list_display_links = ('message',)
    search_fields = ('id',
                     'room__subtopic__topic__subject_class__subject__subject_name',
                     'room__subtopic__topic__subject_class__subject__subject_description',
                     'room__subtopic__topic__subject_class__classes__class_name',
                     'room__subtopic__topic__subject_class__classes__class_description',
                     'room__subtopic__topic__topic_name',
                     'room__subtopic__subtopic_name',
                     'session',
                     'message'
                     )

    ordering = ['-created_at', '-id', ]
    list_filter = ['created_at', 'updated_at']
    list_per_page = 10


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'subtopic', 'created_at')
    list_display_links = ('subtopic',)
    search_fields = ('id',
                     'subtopic__topic__subject_class__subject__subject_name',
                     'subtopic__topic__subject_class__subject__subject_description',
                     'subtopic__topic__subject_class__classes__class_name',
                     'subtopic__topic__subject_class__classes__class_description',
                     'subtopic__topic__topic_name',
                     'subtopic__subtopic_name'
                     )

    ordering = ['-created_at', '-id', ]
    list_filter = ['created_at', 'updated_at']
    list_per_page = 10
    inlines = [MessagesInline]