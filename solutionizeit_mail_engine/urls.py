"""solutionizeit_mail_engine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path

from mail_configuration.views import sit_send_mail


def driver_function(request):
    print("Driver function called")
    payload = {
        "mail_service": "smtp",
        "email_from": "goshweet@gmail.com",
        "recipient_list": "jasirmj@gmail.com",
        "subject": "Test Mail",
        "html_template": "OTP",
        "variables": {
            "otp": "0786",
            "content": "Hi your otp is",
            "brand": "SolutionizeIT"
        }
    }

    sit_send_mail(**payload)

    return HttpResponse("Driver function called")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('mail/', driver_function),
    # path('mail/', TestMail.as_view()),
]
