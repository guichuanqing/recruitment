import logging
from django.contrib import admin
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.utils.safestring import mark_safe

from interview.models import Candidate
from interview import candidate_fieldset as cf
from datetime import datetime

import csv
# Register your models here.
from jobs.models import Resume

logger = logging.getLogger(__name__)

exportable_fields = ('username', 'city', 'phone', 'bachelor_school', 'master_school', 'degree', 'first_result', 'first_interviewer_user',
                     'second_result', 'second_interviewer_user', 'hr_result', 'hr_score', 'hr_remark', 'hr_interviewer_user')

# 通知一面面试官面试
def notify_interviewer(modeladmim, request, queryset):
    candidates = ''
    interviewers = ''
    for obj in queryset:
        candidates =obj.username  +';'+candidates
        interviewers = obj.first_interviewer_user.username +';'+interviewers
    messages.success(request, "候选人 %s 进入面试环节，亲爱的面试官，请准备好面试；%s" % (candidates, interviewers))

notify_interviewer.short_description = '通知一面面试官'
notify_interviewer.allowed_permissions =('notify',)

# 导出候选人功能
def export_model_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv', charset='utf-8-sig')
    field_list = exportable_fields
    response['Content-Disposition'] = 'attachement; filename=recruitment-candidate-list-%s.csv' %(
        datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
    )

    # 写入表头
    writer = csv.writer(response)
    writer.writerow(
        [queryset.model._meta.get_field(f).verbose_name.title() for f in field_list]
    )

    for obj in queryset:
        # 单行的记录（各个字段的值），写入到csv文件
        csv_line_values = []
        for filed in field_list:
            filed_object = queryset.model._meta.get_field(filed)
            filed_value = filed_object.value_from_object(obj)
            csv_line_values.append(filed_value)
        writer.writerow(csv_line_values)

    logger.info('%s exported %s candidate records' % (request.user, len(queryset)))

    return response

export_model_as_csv.short_description = '导出为CSV文件'
export_model_as_csv.allowed_permissions =('export',)

# 候选人管理类
class CandidateAdmin(admin.ModelAdmin):
    exclude = ('creator', 'created_date', 'modified_date')

    actions = [export_model_as_csv, notify_interviewer,]

    # 当前用户是否有导出权限：
    def has_export_permission(self, request):
        opts = self.opts
        return request.user.has_perm('%s.%s' % (opts.app_label, 'export'))

    list_display = (
        'username', 'city','bachelor_school', 'get_resume','first_score', 'first_result', 'first_interviewer_user',
        'second_result', 'second_interviewer_user', 'hr_score', 'hr_result', 'last_editor'
    )

    # 当前用户是否有通知权限：
    def has_notify_permission(self, request):
        opts = self.opts
        return request.user.has_perm('%s.%s' % (opts.app_label, 'notify'))

    # 筛选条件
    list_filter = ('city', 'first_result', 'second_result', 'hr_result', 'first_interviewer_user', 'second_interviewer_user', 'hr_interviewer_user',)

    # 查询字段
    search_fields = ('username', 'phone', 'email', 'bachelor_school')

    # 排序条件
    ordering = ('hr_result', 'second_result', 'first_result')

    # 列表编辑
    default_list_editable = ('first_interviewer_user', 'second_interviewer_user',)

    # 查看简历
    def get_resume(self, obj):
        if not obj.phone:
            return ''
        resume = Resume.objects.filter(phone = obj.phone)
        if resume and len(resume)>0:
            return mark_safe('<a href="/resume/%s" target="_blank"> %s </a>' % (resume[0].id, '查看简历'))
        return ''

    get_resume.short_description = '查看简历'
    get_resume.allow_tags = True

    def get_list_editable(self, request):
        group_names = self.get_group_names(request.user)

        if request.user.is_superuser or 'hr' in group_names:
            return self.default_list_editable
        return ()

    def get_changelist_instance(self, request):
        self.list_editable = self.get_list_editable(request)
        return super(CandidateAdmin, self).get_changelist_instance(request)

    # readonly_fields = ('first_interviewer_user', 'second_interviewer_user')
    def get_group_names(self, user):
        group_names = []
        for g in user.groups.all():
            group_names.append(g.name)
        return group_names

    # 对于非管理员，非HR，获取自己是一面面试官或者二面面试官的候选人集合：s
    def get_queryset(self, request):
        qs = super(CandidateAdmin, self).get_queryset(request)

        group_name = self.get_group_names(request.user)
        if request.user.is_superuser or 'hr' in group_name:
            return qs
        return Candidate.objects.filter(
            Q(first_interviewer_user = request.user) | Q(second_interviewer_user=request.user)
        )

    def get_readonly_fields(self, request, obj):
        group_names = self.get_group_names(request.user)

        if 'interviewer' in group_names:
            logger.info("interviewer is in user's group for %s" % request.user.username)
            return ('first_interviewer_user', 'second_interviewer_user')
        return ()

    # 一面面试官仅填写一面反馈，二面面试官可以填写二面反馈
    def get_fieldsets(self, request, obj=None):
        group_names = self.get_group_names(request.user)

        if 'interviewer' in group_names and obj.first_interviewer_user == request.user:
            return cf.default_fieldsets_first
        if 'interviewer' in group_names and obj.second_interviewer_user == request.user:
            return cf.default_fieldsets_second
        return cf.default_fieldsets

admin.site.register(Candidate, CandidateAdmin)