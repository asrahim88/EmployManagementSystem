from .serializers import EmployeeSerializer
from .models import Employee
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin, IsManager, IsEmployee

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]  # ডিফল্ট পারমিশন

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # list এবং retrieve অ্যাকশনের জন্য
            permission_classes = [IsAdmin | IsManager | IsEmployee]  # তিনটি পারমিশন একত্রে
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:  # create, update এবং delete অপারেশনের জন্য
            permission_classes = [IsAdmin]  # শুধুমাত্র Admin
        else:
            permission_classes = [IsAuthenticated]  # অন্যান্য ক্ষেত্রে সাধারণ অথেনটিকেটেড ইউজার

        return [permission() for permission in permission_classes]
