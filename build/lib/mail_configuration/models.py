from django.db import models

from mail_configuration.constants import MAILING_SERVICE_SENDGRID, MAILING_SERVICE_SMTP

# Create your models here.
MAILING_SERVICE_CHOICES = (
    (MAILING_SERVICE_SMTP, MAILING_SERVICE_SMTP),
    (MAILING_SERVICE_SENDGRID, MAILING_SERVICE_SENDGRID),
    # Add more services as needed
)


class MailingService(models.Model):
    # e.g., 'SMTP', 'SendGrid'
    name = models.CharField(max_length=50, unique=True,
                            choices=MAILING_SERVICE_CHOICES)
    # e.g., 'django.core.mail.backends.smtp.EmailBackend'
    email_backend = models.CharField(max_length=255, null=True, blank=True)
    # For services like SendGrid
    api_key = models.CharField(max_length=255, blank=True, null=True)
    email_host = models.CharField(
        max_length=255, blank=True, null=True)  # For SMTP
    email_port = models.IntegerField(blank=True, null=True)  # For SMTP
    email_use_tls = models.BooleanField(
        default=True, blank=True, null=True)  # For SMTP
    email_host_user = models.EmailField(blank=True, null=True)  # For SMTP
    email_host_password = models.CharField(
        max_length=255, blank=True, null=True)  # For SMTP
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_backend_config(self):
        if self.name.lower() == 'smtp':
            return {
                'EMAIL_BACKEND': self.email_backend,
                'EMAIL_HOST': self.email_host,
                'EMAIL_PORT': self.email_port,
                'EMAIL_USE_TLS': self.email_use_tls,
                'EMAIL_HOST_USER': self.email_host_user,
                'EMAIL_HOST_PASSWORD': self.email_host_password,
            }
        elif self.name.lower() == 'sendgrid':
            return {
                'EMAIL_BACKEND': 'anymail.backends.sendgrid.EmailBackend',
                'ANYMAIL': {
                    'SENDGRID_API_KEY': self.api_key,
                }
            }
        # Add logic for other services as needed
        else:
            return {}


class MailRecord(models.Model):
    subject = models.CharField(max_length=255)
    sender_mail = models.CharField(max_length=100, blank=False, null=False)
    to_mail = models.JSONField(max_length=100, blank=False, null=False)
    cc_mail = models.JSONField(max_length=100, blank=True, null=True)
    bcc_mail = models.JSONField(max_length=100, blank=True, null=True)
    payload_json = models.JSONField(null=True, blank=True)
    body = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_success = models.BooleanField(default=False)
    mail_response = models.TextField(blank=True, null=True)
    service = models.ForeignKey(
        MailingService, on_delete=models.SET_NULL, null=True, blank=True)
    # Store any response or error message


class EmailTemplate(models.Model):
    name = models.CharField(max_length=100, unique=True)
    template_html = models.TextField(
        help_text="Variables format {{var}}  ,for preview copy html content and paste it on https://www.programiz.com/html/online-compiler/")  # Store HTML with placeholders

    def __str__(self):
        return self.name
