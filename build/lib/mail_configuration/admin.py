from django.contrib import admin


# Register your models here.

from .models import EmailTemplate, MailRecord, MailingService


@admin.register(MailingService)
class MailingServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'email_backend', 'email_host_user')


@admin.register(MailRecord)
class MailRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'to_mail', 'is_success', 'created_date')


# @admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )


admin.site.register(EmailTemplate, EmailTemplateAdmin)
