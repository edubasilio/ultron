from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from entities.authentication import token_refresh as refresh
from rest_framework.authtoken.models import Token


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def token_refresh(request):
    auth = request.META.get('HTTP_AUTHORIZATION', b'')    
    key = auth.split(' ')[1]
    
    token = Token.objects.get(key=key)
    refresh(token) 

    return Response({"detail": "Token refreshed."})
