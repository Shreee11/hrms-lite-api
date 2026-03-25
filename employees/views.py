from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count, Q
from .models import Employee, Attendance
from .serializers import EmployeeSerializer, AttendanceSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['employee_id', 'full_name', 'department']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Employee deleted successfully."},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        total_employees = Employee.objects.count()
        total_departments = Employee.objects.values('department').distinct().count()
        department_counts = list(
            Employee.objects.values('department')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        return Response({
            'total_employees': total_employees,
            'total_departments': total_departments,
            'department_counts': department_counts,
        })


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.select_related('employee').all()
    serializer_class = AttendanceSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        queryset = super().get_queryset()
        employee_id = self.request.query_params.get('employee')
        date = self.request.query_params.get('date')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')

        if employee_id:
            queryset = queryset.filter(employee_id=employee_id)
        if date:
            queryset = queryset.filter(date=date)
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
        return queryset
