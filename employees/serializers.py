from datetime import date as date_today
from rest_framework import serializers
from .models import Employee, Attendance


class EmployeeSerializer(serializers.ModelSerializer):
    total_present = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['id', 'employee_id', 'full_name', 'email', 'department', 'created_at', 'total_present']
        read_only_fields = ['id', 'created_at']

    def get_total_present(self, obj):
        return obj.attendance_records.filter(status='Present').count()

    def validate_email(self, value):
        if self.instance is None:
            if Employee.objects.filter(email=value).exists():
                raise serializers.ValidationError("An employee with this email already exists.")
        else:
            if Employee.objects.filter(email=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("An employee with this email already exists.")
        return value

    def validate_employee_id(self, value):
        if self.instance is None:
            if Employee.objects.filter(employee_id=value).exists():
                raise serializers.ValidationError("An employee with this ID already exists.")
        else:
            if Employee.objects.filter(employee_id=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("An employee with this ID already exists.")
        return value


class AttendanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    employee_eid = serializers.CharField(source='employee.employee_id', read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'employee', 'employee_name', 'employee_eid', 'date', 'status', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_date(self, value):
        if value > date_today.today():
            raise serializers.ValidationError("Cannot mark attendance for a future date.")
        return value

    def validate(self, data):
        employee = data.get('employee')
        date = data.get('date')
        if self.instance is None:
            if Attendance.objects.filter(employee=employee, date=date).exists():
                raise serializers.ValidationError(
                    "Attendance for this employee on this date already exists."
                )
        return data
