from operator import truediv
from os import stat
from pickletools import read_unicodestring1
from rest_framework import permissions, views, response, status, viewsets
from .models import Category, Wallet, Transactions
from .serializers import UserSerializer, UserRegisterSerializer, CategorySerializer


class UserRegisterView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response({'detail': "ERROR"}, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context