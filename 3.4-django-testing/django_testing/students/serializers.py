from rest_framework import serializers
from .models import Course, Student

class CourseSerializer(serializers.ModelSerializer):
    students = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Student.objects.all(),
        required=False
    )

    class Meta:
        model = Course
        fields = ['id', 'name', 'students']

    def update(self, instance, validated_data):
        students_data = validated_data.pop('students', None)
        instance = super().update(instance, validated_data)
        if students_data is not None:
            instance.students.set(students_data)
        return instance