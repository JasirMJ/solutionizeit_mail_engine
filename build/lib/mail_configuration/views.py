from django.conf import settings
from django.core.exceptions import ValidationError
from mail_configuration.serializers import MailRecordSerializer
from mail_configuration.utils import get_mail_service, render_email_template
from django.core.mail import EmailMessage
# Create your views here.


def sit_send_mail(**kwargs):
    try:
        # Validate and extract required fields
        mail_service = kwargs.get('mail_service')
        email_from = kwargs.get('email_from')
        recipient_list = kwargs.get('recipient_list')
        cc_mail_list = kwargs.get('cc_mail_list')
        bcc_mail_list = kwargs.get('bcc_mail_list')
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
        elif recipient_list is None:
            raise ValidationError("Recipient list cannot be empty.")
        elif not isinstance(recipient_list, list):
            raise ValidationError(
                "Recipient list must be a list or a single email string.")

        # Ensure CC is a list
        if isinstance(cc_mail_list, str):
            cc_mail_list = [cc_mail_list]
        elif cc_mail_list is None:
            cc_mail_list = []
        elif not isinstance(cc_mail_list, list):
            raise ValidationError(
                "CC list must be a list or a single email string.")

        # Ensure BCC is a list
        if isinstance(bcc_mail_list, str):
            bcc_mail_list = [bcc_mail_list]
        elif bcc_mail_list is None:
            bcc_mail_list = []
        elif not isinstance(bcc_mail_list, list):
            raise ValidationError(
                "BCC list must be a list or a single email string.")

        # Fetch the mail service configuration dynamically
        mail_service_instance = get_mail_service(mail_service)
        if not mail_service_instance:
            raise ValidationError(
                "Mail service not found for {}".format(mail_service))
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
        response = 1  # Dummy response for testing
        response = email.send()
        print(f"Email sent successfully. Response: {response}")

        return {"status": True, "message": "Email sent successfully", "response": response}

    except ValidationError as ve:
        response = f"Validation error: {ve}"
        print(response)

        return {"status": False, "error": str(f"Validation error: {ve}")}
    except Exception as e:
        response = (f"An error occurred: {str(e)}")
        print(response)

        return {"status": False, "error": response}
    finally:
        # Log the attempt, whether successful or not
        try:
            mail_record_data = {
                "subject": subject,
                "sender_mail": mail_service_instance.email_host_user,
                "to_mail": recipient_list,
                "cc_mail": cc_mail_list,
                "bcc_mail": bcc_mail_list,
                "payload_json": kwargs,
                "body": html_content,
                "is_success": True if response == 1 else False,
                "mail_response": response,
                "service": mail_service_instance.id,
            }

            print(f"Mail record data: {mail_record_data}")

            mail_record_obj = MailRecordSerializer(
                data=mail_record_data)
            if mail_record_obj.is_valid(raise_exception=True):
                mail_record_obj.save()
        except Exception as e:
            print(f"An error occurred while logging the mail record: {str(e)}")
        print("sendMail function executed.")
        # Any other cleanup or logging actions can be added here
