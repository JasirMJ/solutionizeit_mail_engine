

from django.template import Template, Context
from django.template.loader import render_to_string
from .models import EmailTemplate, MailingService


def render_email_template(template_name, context):
    try:
        # Fetch the template from the database
        template = EmailTemplate.objects.get(name=template_name)
        template_html = template.template_html

        # Replace placeholders with context values
        context = {key: value for key, value in context.items()}
        return Template(template_html).render(Context(context))
    except EmailTemplate.DoesNotExist:
        raise ValueError("Template not found.")


def get_mail_service(service_name='SMTP'):
    mail_service = MailingService.objects.get(name=service_name)
    return mail_service
