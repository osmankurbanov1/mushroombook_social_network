from rest_framework.generics import RetrieveUpdateAPIView

from .serializers import UserSerializer
from .permissions import IsProfileOwnerOrReadOnly
from profiles.models import MyUser

# Create your views here.


class UsersProfileView(RetrieveUpdateAPIView):
    """
    get the User /
    update the User
    """
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsProfileOwnerOrReadOnly, )
