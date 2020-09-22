from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext as _

from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


def token_refresh(token):
    token.created = timezone.now()
    token.save()
    return token

def is_token_expired(token):
    time_elapsed = timezone.now() - token.created
    left_time = timedelta(seconds = settings.TOKEN_EXPIRED_TIME) - time_elapsed
    is_token_expired = left_time < timedelta(seconds = 0)
    if is_token_expired:
        token.delete()
    return is_token_expired


class UltronAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))
        
        if is_token_expired(token):
            raise AuthenticationFailed("Token expired")

        return (token.user, token)
    