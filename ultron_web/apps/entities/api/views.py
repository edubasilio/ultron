from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from entities.authentication import token_refresh


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def token_refresh(request):
    print(request)
    return Response("")
