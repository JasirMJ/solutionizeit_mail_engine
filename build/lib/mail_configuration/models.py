from django.db import models

# Create your models here.


class MailingService(models.Model):
    # e.g., 'SMTP', 'SendGrid'
    name = models.CharField(max_length=50, unique=True)
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

    def __str__(self):
        return self.name

    def get_backend_config(self):
        print("\n\n\nSelf name", self.name)
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

# class MailConfiguration(models.Model):
#     name = models.CharField(max_length=50)  # Optional: to identify different configurations
#     service = models.ForeignKey(MailingService, on_delete=models.CASCADE)

#     def __str__(self):
#         return f'{self.name} ({self.service.name})'

#     def get_backend_config(self):
#         return self.service.get_backend_config()


class MailRecord(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    recipient = models.EmailField()
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)  # e.g., 'sent', 'failed', etc.
    service = models.ForeignKey(
        MailingService, on_delete=models.SET_NULL, null=True, blank=True)
    # Store any response or error message
    response = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.subject} to {self.recipient} ({self.status})'


class EmailTemplate(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subject = models.CharField(max_length=255)
    template_html = models.TextField(
        help_text="Variables format ##OTP##  ,for preview copy html content and paste it on https://www.programiz.com/html/online-compiler/")  # Store HTML with placeholders

    def __str__(self):
        return self.name
