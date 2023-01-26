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

TRUE_FALSE_CHOICES = (
    ('true', 'True'),
    ('false', 'False')
)

APPROVAL_CHOICES = (
    ('draft', 'Draft'),
    ('send_for_approval', 'Send For Approval'),
    ('return_for_amendment', 'Return For Amendment'),
    ('approved', 'Approved'),
)


class Classes(models.Model):
    id = models.BigAutoField(primary_key=True)
    class_name = models.CharField(max_length=255, blank=False, null=False)
    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)
    class_description = models.CharField(max_length=255, blank=True, null=True)
    order_id = models.IntegerField(blank=False, null=False, default=1)
    icon = models.ImageField(default='', blank=True, upload_to='classes_icons')
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

    active_status = models.BooleanField(default=True, )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "01. Class"
        verbose_name_plural = "01. Classes"

    def __str__(self):
        return f'{str(self.class_name)}'

    def save(self, *args, **kwargs):
        unique_id = get_random_string(length=8)
        combined_slug = f' {str(self.class_name)}-{str(unique_id)}'
        self.slug = slugify(combined_slug)
        return super(Classes, self).save(*args, **kwargs)


@receiver(post_save, sender=Classes)
def create_or_update_class_subject(sender, instance, created, **kwargs):
    # for each subject, add class in the table of subjectClass
    if created:
        try:
            subject_list = Subjects.objects.order_by('created_at')
            for subject in subject_list:
                item_obj, item_created = SubjectClass.objects.update_or_create(classes=instance, subject=subject)
        except Exception as ex:
            print(ex)
            pass


class Subjects(models.Model):
    id = models.BigAutoField(primary_key=True)
    subject_name = models.CharField(max_length=255, blank=False, null=False, unique=True)
    subject_description = RichTextUploadingField(blank=False, null=True)
    order_id = models.IntegerField(blank=False, null=False, default=1)
    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)
    icon = models.ImageField(default='', blank=True, upload_to='subject_icons')
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
        verbose_name = "02. Subject"
        verbose_name_plural = "02. Subjects"

    def __str__(self):
        return f' {str(self.subject_name)} '

    def save(self, *args, **kwargs):
        unique_id = get_random_string(length=8)
        combined_slug = f' {str(self.subject_name)}-{str(unique_id)}'
        self.slug = slugify(combined_slug)
        return super(Subjects, self).save(*args, **kwargs)


@receiver(post_save, sender=Subjects)
def create_or_update_subject_class(sender, instance, created, **kwargs):
    # for each class, add subject in the table of subjectClass
    if created:
        try:
            classes_list = Classes.objects.order_by('created_at')
            for classes in classes_list:
                item_obj, item_created = SubjectClass.objects.update_or_create(classes=classes, subject=instance)
        except Exception as ex:
            print(ex)
            pass


class SubjectClass(models.Model):
    id = models.BigAutoField(primary_key=True)
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE, blank=False, null=False)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, blank=False, null=False)
    order_id = models.IntegerField(blank=False, null=False, default=1)
    slug = models.SlugField(unique=True, max_length=512, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "02_2. Subject Class"
        verbose_name_plural = verbose_name
        ordering = ('classes', 'subject')
        unique_together = ('subject', 'classes')

    def __str__(self):
        return f' {str(self.classes.class_name)}  : {str(self.subject.subject_name)} '

    def save(self, *args, **kwargs):
        combined_slug = f' {str(self.classes.slug)}-{str(self.subject.slug)}'
        unique_id = get_random_string(length=8)
        combined_slug = f' {str(combined_slug)}-{str(unique_id)}'
        self.slug = slugify(combined_slug)
        return super(SubjectClass, self).save(*args, **kwargs)


class Topics(models.Model):
    id = models.BigAutoField(primary_key=True)
    subject_class = models.ForeignKey(SubjectClass, on_delete=models.CASCADE, blank=False, null=False,
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
        unique_together = ('subject_class', 'topic_name')

    def __str__(self):
        return f' {str(self.subject_class)}  - {str(self.topic_name)} '

    def save(self, *args, **kwargs):
        unique_id = get_random_string(length=8)
        combined_slug = f' {str(self.topic_name)}-{str(unique_id)}'
        self.slug = slugify(combined_slug)
        return super(Topics, self).save(*args, **kwargs)


class SubTopics(models.Model):
    id = models.BigAutoField(primary_key=True)
    topic = models.ForeignKey(Topics, on_delete=models.CASCADE, blank=False, null=False, related_name="subtopics")
    subtopic_name = models.CharField(max_length=255, blank=False, null=False)
    order_id = models.IntegerField(blank=False, null=False, default=1)
    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)
    icon = models.ImageField(default='', blank=True, upload_to='language_icons')
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
        verbose_name = "04. Sub Topics"
        verbose_name_plural = verbose_name
        unique_together = ('topic', 'subtopic_name')

    def __str__(self):
        return f' {str(self.topic.subject_class)}  - {str(self.topic.topic_name)}  :  {str(self.subtopic_name)}'

    def save(self, *args, **kwargs):
        unique_id = get_random_string(length=8)
        combined_slug = f' {str(self.subtopic_name)}-{str(unique_id)}'
        self.slug = slugify(combined_slug)
        return super(SubTopics, self).save(*args, **kwargs)

    def get_segments(self):
        return self.primarysegments_set.filter(respective_notes__status = "approved")


class Segments(models.Model):
    id = models.BigAutoField(primary_key=True)
    subtopic = models.ForeignKey(SubTopics, on_delete=models.CASCADE, blank=False, null=False, related_name="primarysegments_set")
    segment_id = models.IntegerField(blank=True, null=True)
    segment_name = models.CharField(max_length=255, blank=False, null=False)
    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "05. Segments"
        verbose_name_plural = verbose_name
        unique_together = ('subtopic', 'segment_id')

    def __str__(self):
        return f' {str(self.subtopic.topic.subject_class)}  - {str(self.subtopic.topic.topic_name)}  :  {str(self.subtopic.subtopic_name)} - {str(self.segment_name)}'

    def save(self, *args, **kwargs):
        unique_id = get_random_string(length=8)
        combined_slug = f' {str(self.subtopic.slug)}-{str(unique_id)}'
        self.slug = slugify(combined_slug)
        if self.segment_id is None or self.segment_id == 0:
            self.segment_id = 0
            try:
                segment = Segments.objects.filter(subtopic=self.subtopic).order_by('-segment_id')[:1]
                segment = segment.get()
                self.segment_id = segment.segment_id + 1

            except ObjectDoesNotExist as ex:
                self.segment_id = 1

        return super(Segments, self).save(*args, **kwargs)

    def get_notes(self):
        if hasattr(self, 'respective_notes'):
            return self.respective_notes.notes
        return None

    def get_true_or_false_questions(self):
        return self.respective_notes.all()


class Notes(models.Model):
    id = models.BigAutoField(primary_key=True)
    segment = models.OneToOneField(Segments, on_delete=models.CASCADE, blank=False, null=False, unique=True,
                                   related_name="respective_notes")
    notes = RichTextUploadingField(blank=False, null=False)
    status = models.CharField(choices=APPROVAL_CHOICES, blank=False, null=False, default='draft', max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "06. Notes"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f' {str(self.segment.subtopic.subtopic_name)}  :  {str(self.segment.segment_id)}'

    def approved_notes(self):
        return self.filter(status='approved')



class QuizMultipleChoicesQuestions(models.Model):
    id = models.BigAutoField(primary_key=True)
    segment = models.ForeignKey(Segments, on_delete=models.CASCADE, blank=False, null=False)
    question = models.CharField(max_length=4000, blank=False, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "07. Quiz Multiple-Choice"
        verbose_name_plural = verbose_name
        unique_together = ('question', 'segment')

    def __str__(self):
        return f' {str(self.question)}'


class QuizMultipleChoicesOptions(models.Model):
    id = models.BigAutoField(primary_key=True)
    question = models.ForeignKey(QuizMultipleChoicesQuestions, on_delete=models.CASCADE, blank=False, null=False,
                                 related_name="options")
    choice = models.CharField(max_length=4000, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "07_2. Quiz M-Choice Options"
        verbose_name_plural = verbose_name
        unique_together = ('question', 'choice')

    def __str__(self):
        return f' {str(self.question.question)}  -  {str(self.choice)}'


class QuizMultipleChoicesAnswers(models.Model):
    id = models.BigAutoField(primary_key=True)
    question = models.OneToOneField(QuizMultipleChoicesQuestions, on_delete=models.CASCADE, blank=False, null=False,
                                    unique=True, related_name="respective_answer")
    choice = models.ForeignKey(QuizMultipleChoicesOptions, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "07_3. Quiz M-Choice Answers"
        verbose_name_plural = verbose_name
        unique_together = ('question', 'choice')

    def __str__(self):
        return f' {str(self.question.question)}  -  {str(self.choice.choice)}'


class QuizTrueOrFalse(models.Model):
    segment = models.ForeignKey(Segments, on_delete=models.CASCADE, related_name='primary_quiztrueorfalse_set',
                                blank=False, null=False)
    question = models.CharField(max_length=4000, blank=False, null=False, unique=True)
    answer = models.CharField(choices=TRUE_FALSE_CHOICES, blank=True, null=True, max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "08. Quiz True/False"
        verbose_name_plural = verbose_name
        unique_together = ('question', 'segment')

    def __str__(self):
        return f' {str(self.question)}'


class QuizShortAnswer(models.Model):
    segment = models.ForeignKey(Segments, on_delete=models.CASCADE, blank=False, null=False)
    question = models.CharField(max_length=4000, blank=False, null=False)
    answer = models.CharField(max_length=4000, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "09. Quiz Short Answers"
        verbose_name_plural = verbose_name
        unique_together = ('question', 'segment')

    def __str__(self):
        return f' {str(self.question)}'


class QuizMatchingItem(models.Model):
    segment = models.OneToOneField(Segments, on_delete=models.CASCADE, blank=False, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "10. Quiz Matching-Items"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f' {str(self.segment.subtopic.subtopic_name)}  :  {str(self.segment.segment_id)}'


class QuizMatchingItemQuestions(models.Model):
    matching_item = models.ForeignKey(QuizMatchingItem, on_delete=models.CASCADE, blank=False, null=False, default="")
    question = models.CharField(max_length=4000, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "10_2. Questions"
        verbose_name_plural = verbose_name
        unique_together = ('question', 'matching_item')

    def __str__(self):
        return f' {str(self.question)}'


@receiver(post_save, sender=QuizMatchingItemQuestions)
def create_or_update_quiz_matching_item_answer(sender, instance, created, **kwargs):
    # for each subject, add class in the table of subjectClass
    if created:
        try:
            item_obj, item_created = QuizMatchingItemAnswers.objects.update_or_create(
                matching_item=instance.matching_item, question=instance)
        except Exception as ex:
            print(ex)
            pass


class QuizMatchingItemOptions(models.Model):
    matching_item = models.ForeignKey(QuizMatchingItem, on_delete=models.CASCADE, blank=False, null=False, default="")
    option = models.CharField(max_length=4000, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "10_3. Items"
        verbose_name_plural = verbose_name
        unique_together = ('option', 'matching_item')

    def __str__(self):
        return f' {str(self.option)}'


class QuizMatchingItemAnswers(models.Model):
    matching_item = models.ForeignKey(QuizMatchingItem, on_delete=models.CASCADE, blank=False, null=False, default="")
    question = models.ForeignKey(QuizMatchingItemQuestions, on_delete=models.CASCADE, blank=False, null=False)
    answer = models.ForeignKey(QuizMatchingItemOptions, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "10_4. Answers"
        verbose_name_plural = verbose_name
        unique_together = ('matching_item', 'question')

    def __str__(self):
        selected_option = ''
        if self.answer is not None:
            selected_option = str(self.answer.option)
        return f' {str(self.question.question)}  -  {selected_option}'


class MultipleChoicesQuestions(models.Model):
    id = models.BigAutoField(primary_key=True)
    subtopic = models.ForeignKey(SubTopics, on_delete=models.CASCADE, blank=False, null=False)
    question = models.CharField(max_length=4000, blank=False, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "11. Test Multiple-Choice"
        verbose_name_plural = verbose_name
        unique_together = ('question', 'subtopic')

    def __str__(self):
        return f' {str(self.question)}'


class MultipleChoicesOptions(models.Model):
    id = models.BigAutoField(primary_key=True)
    question = models.ForeignKey(MultipleChoicesQuestions, on_delete=models.CASCADE, blank=False, null=False,
                                 related_name="options")
    choice = models.CharField(max_length=4000, blank=False, null=False)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "11_2. Multiple Choice Options"
        verbose_name_plural = verbose_name
        unique_together = ('question', 'choice')

    def __str__(self):
        return f' {str(self.question.question)}  -  {str(self.choice)}'


class MultipleChoicesAnswers(models.Model):
    id = models.BigAutoField(primary_key=True)
    question = models.OneToOneField(MultipleChoicesQuestions, on_delete=models.CASCADE, blank=False, null=False,
                                    unique=True, related_name="respective_answer")
    choice = models.ForeignKey(MultipleChoicesOptions, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "11_3. Multiple Choice Answers"
        verbose_name_plural = verbose_name
        unique_together = ('question', 'choice')

    def __str__(self):
        return f' {str(self.question.question)}  -  {str(self.choice.choice)}'


class TrueOrFalseQuestions(models.Model):
    id = models.BigAutoField(primary_key=True)
    subtopic = models.ForeignKey(SubTopics, on_delete=models.CASCADE, blank=False, null=False)
    question = models.CharField(max_length=4000, blank=False, null=False, unique=True)
    answer = models.CharField(choices=TRUE_FALSE_CHOICES, blank=True, null=True, max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "10. Test True/False"
        verbose_name_plural = verbose_name
        unique_together = ('question', 'subtopic')

    def __str__(self):
        return f' {str(self.question)}'


class ShortAnswerQuestions(models.Model):
    id = models.BigAutoField(primary_key=True)
    subtopic = models.ForeignKey(SubTopics, on_delete=models.CASCADE, blank=False, null=False)
    question = models.CharField(max_length=4000, blank=False, null=False)
    answer = models.CharField(max_length=4000, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "13. Test Short Answers"
        verbose_name_plural = verbose_name
        unique_together = ('question', 'subtopic')

    def __str__(self):
        return f' {str(self.question)}'


class TestMatchingItem(models.Model):
    subtopic = models.OneToOneField(SubTopics, on_delete=models.CASCADE, blank=False, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "14. Test Matching-Items"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f' {str(self.subtopic.subtopic_name)} '


class TestMatchingItemQuestions(models.Model):
    id = models.BigAutoField(primary_key=True)
    matching_item = models.ForeignKey(TestMatchingItem, on_delete=models.CASCADE, blank=False, null=False)
    question = models.CharField(max_length=4000, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "14_2. Questions"
        verbose_name_plural = verbose_name
        unique_together = ('question', 'matching_item')

    def __str__(self):
        return f' {str(self.question)}'


@receiver(post_save, sender=TestMatchingItemQuestions)
def create_or_update_test_matching_item_answer(sender, instance, created, **kwargs):
    # for each subject, add class in the table of subjectClass
    if created:
        try:
            item_obj, item_created = TestMatchingItemAnswers.objects.update_or_create(
                matching_item=instance.matching_item,
                question=instance)
        except Exception as ex:
            print(ex)
            pass


class TestMatchingItemOptions(models.Model):
    id = models.BigAutoField(primary_key=True)
    matching_item = models.ForeignKey(TestMatchingItem, on_delete=models.CASCADE, blank=False, null=False)
    option = models.CharField(max_length=4000, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "14_3. Items"
        verbose_name_plural = verbose_name
        unique_together = ('option', 'matching_item')

    def __str__(self):
        return f' {str(self.option)}'


class TestMatchingItemAnswers(models.Model):
    id = models.BigAutoField(primary_key=True)
    matching_item = models.ForeignKey(TestMatchingItem, on_delete=models.CASCADE, blank=False, null=False)
    question = models.ForeignKey(TestMatchingItemQuestions, on_delete=models.CASCADE, blank=False, null=False)
    answer = models.ForeignKey(TestMatchingItemOptions, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "14_4. Answers"
        verbose_name_plural = verbose_name
        unique_together = ('question', 'matching_item')

    def __str__(self):
        selected_option = ''
        if self.answer is not None:
            selected_option = str(self.answer.option)
        return f' {str(self.question.question)}  -  {selected_option}'


class ChatRoom(models.Model):
    id = models.BigAutoField(primary_key=True)
    subtopic = models.OneToOneField(SubTopics, on_delete=models.CASCADE, blank=False, null=False, unique=True)
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
        verbose_name = "15. ChatRooms"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'Chat Room for {str(self.subtopic.subtopic_name)}'


def post_save_chatroom_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            ChatRoom.objects.create(subtopic=instance)
        except:
            pass


post_save.connect(post_save_chatroom_model_receiver, sender=SubTopics)


class Messages(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, blank=False, null=False,
                             related_name='lcms_lcms_primary_messages_set')
    session = models.CharField(max_length=4000, blank=True, null=True)
    message = models.TextField(blank=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             related_name='lcms_lcms_primary_messages_user_set')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "16. Messages"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'Messages for {str(self.room.subtopic.subtopic_name)}  Chat Room'