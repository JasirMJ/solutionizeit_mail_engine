from django.conf import settings
from django.core.exceptions import ValidationError
from mail_configuration.utils import get_mail_service, render_email_template
from django.core.mail import EmailMessage
# Create your views here.


def sit_send_mail(**kwargs):
    try:
        # Validate and extract required fields
        mail_service = kwargs.get('mail_service')
        email_from = kwargs.get('email_from')
        recipient_list = kwargs.get('recipient_list')
        subject = kwargs.get('subject')
        html_template = kwargs.get('html_template')
        variables = kwargs.get('variables', {})

        # Basic validation
        if not mail_service:
            raise ValidationError("Mail service is required.")
        if not email_from:
            raise ValidationError("Sender's email is required.")
        if not recipient_list:
            raise ValidationError("Recipient list is required.")
        if not subject:
            raise ValidationError("Email subject is required.")
        if not html_template:
            raise ValidationError("HTML template name is required.")

        # Ensure recipient_list is a list
        if isinstance(recipient_list, str):
            recipient_list = [recipient_list]
        elif not isinstance(recipient_list, list):
            raise ValidationError(
                "Recipient list must be a list or a single email string.")

        # Fetch the mail service configuration dynamically
        mail_service_instance = get_mail_service(mail_service)
        mail_config = mail_service_instance.get_backend_config()

        # Update Django settings dynamically
        settings.EMAIL_BACKEND = mail_config['EMAIL_BACKEND']
        settings.EMAIL_HOST = mail_config['EMAIL_HOST']
        settings.EMAIL_PORT = mail_config['EMAIL_PORT']
        settings.EMAIL_USE_TLS = mail_config['EMAIL_USE_TLS']
        settings.EMAIL_HOST_USER = mail_config['EMAIL_HOST_USER']
        settings.EMAIL_HOST_PASSWORD = mail_config['EMAIL_HOST_PASSWORD']

        # Prepare the email content by rendering the template
        html_content = render_email_template(html_template, variables)

        # Create the EmailMessage object
        email = EmailMessage(
            subject=subject,
            body=html_content,
            to=recipient_list,
            reply_to=[email_from],
        )
        email.content_subtype = 'html'  # Set the content type of the email to HTML

        # Attempt to send the email
        response = email.send()
        print(f"Email sent successfully. Response: {response}")
        return {"status": True, "message": "Email sent successfully", "response": response}

    except ValidationError as ve:
        print(f"Validation error: {ve}")
        return {"status": False, "error": str(ve)}
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {"status": False, "error": str(e)}
    finally:
        # Log the attempt, whether successful or not
        print("sendMail function executed.")
        # Any other cleanup or logging actions can be added here
