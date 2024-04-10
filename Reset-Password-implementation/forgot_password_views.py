from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm

"""
IMPORTANT

add the lines bellow to your settings.py 

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = '---'  # Replace with your email address
EMAIL_HOST_PASSWORD = '---'  # Replace with your app password (Google How to setup app password)

"""


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            # Generate password reset token
            token_generator = default_token_generator
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)

            # Build reset link
            reset_link = request.build_absolute_uri(
                f'/reset-password/{uid}/{token}/'
            )

            # Send reset email
            subject = 'Password Reset'
            message = render_to_string('TEMPLATE DIR /password-reset-email.html', {
                'reset_link': reset_link,
            })
            send_mail(subject, message, 'from@example.com', [email])

        return render(request, 'TEMPLATE DIR/password-reset-sent.html')

    return render(request, 'TEMPLATE DIR/forgot-password.html')



def reset_password(request, uidb64, token):
    UserModel = get_user_model()
    try:
        # Decode uidb64 to get the user's primary key
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    # Verify the token
    if user is not None and default_token_generator.check_token(user, token):
        # Token is valid, display the password reset form
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                # Process the form submission and update the user's password
                form.save()
                return render(request, 'TEMPLATE DIR/password-reset-complete.html')  # Redirect to password reset success page
        else:
            #Uses Default Django SetPassword Form if you want to Customize it head to django docs
            form = SetPasswordForm(user)
        return render(request, 'TEMPLATE DIR/reset-password.html', {'form': form})
    else:
        # Token is invalid or expired, handle accordingly (e.g., show an error message)
        return render(request, 'TEMPLATE DIR/password-reset-invalid.html')