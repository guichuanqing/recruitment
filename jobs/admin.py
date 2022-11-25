from django.contrib import admin
from jobs.models import Job, Resume

# Register your models here.

class JobAdmin(admin.ModelAdmin):
    exclude = ("creator", "create_date", "modified_date")
    list_display = ("job_name", "job_type", "job_city", "creator", "create_date", "modified_date")

    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        super().save_model(request, obj, form, change)

class ResumeAdmin(admin.ModelAdmin):
    list_display = ('username', 'applicant', 'city', 'apply_position', 'bachelor_school', 'major', 'create_date')

    readonly_fields = ('applicant', 'create_date', 'modified_date',)

    fieldsets = (
        (None, {'fields': (
            'applicant',('username',  'gender', 'born_address',), ('city','phone',
            'email', ),'apply_position',
            ('bachelor_school', 'master_school'), ('major', 'degree'),
            'candidate_introduction', 'work_experience', 'project_experience', 'create_date', 'modified_date',)}),
    )

    def save_model(self, request, obj, form, change):
        obj.applicant = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Job, JobAdmin)
admin.site.register(Resume, ResumeAdmin)