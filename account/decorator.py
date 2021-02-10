from django.conf import settings

from rest_framework.response import Response
from rest_framework import status

from datetime import timedelta
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired


def password_verification_required():
    def decorator(func):
        def _wrapped_view(request, *args, **kwargs):
            cur_passworld = request.data.get('current_password')

            if not cur_passworld:
                return Response({
                    'detail': 'Password verification required before accessing to target API'
                }, status=status.HTTP_403_FORBIDDEN)

            if not request.user.check_password(cur_passworld):
                return Response({
                    'detail': 'Invalid password.'
                }, status=status.HTTP_403_FORBIDDEN)

            return func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


def email_verification_required():
    def decorator(func):
        def _wrapped_view(request, *args, **kwargs):
            signer = TimestampSigner()
            user = request.user
            vid = request.data.get('email_verify_code')

            try:
                value = signer.unsign(vid, max_age=timedelta(minutes=settings.VERIFY_EMAIL_MAX_AGE))
            except SignatureExpired:
                return Response({'detail': 'Signature expired.'}, status=status.HTTP_403_FORBIDDEN)
            except BadSignature:
                return Response({'detail': 'Bad signature.'}, status=status.HTTP_403_FORBIDDEN)

            if value != user.username:
                return Response({'detail': 'Mismatch signature.'}, status=status.HTTP_403_FORBIDDEN)

            if not user.email_verified:
                user.email_verified = True
                user.save()

            return func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
