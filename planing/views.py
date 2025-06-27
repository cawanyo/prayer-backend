from rest_framework import generics, permissions
from .models import Program
from .serializers import ProgramSerializer
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import permissions, status

from accounts.permissions import ResponsablePermission

class ProgramListCreateView(generics.ListCreateAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ProgramDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    

class ProgramByDateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, date):
        program = Program.objects.filter(date=date).order_by('start_time').first()
        if program is None:
            return Response({"detail": "No program found for this date."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProgramSerializer(program)
        return Response(serializer.data)
    

class ProgramsByMonthView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, year, month):

        programs = Program.objects.filter(date__month=month, date__year=year).order_by('date', 'start_time')
        serializer = ProgramSerializer(programs, many=True)
        return Response(serializer.data)


class ProgramUpsertView(APIView):
    permission_classes = [permissions.IsAuthenticated, ResponsablePermission]

    def post(self, request):
        data = request.data.copy()
        date = data.get('date')

        if not date:
            return Response({"detail": "Date is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            program, created = Program.objects.update_or_create(
                date=date,
                defaults={
                    'name': data.get('name'),
                    'start_time': data.get('start_time'),
                    'end_time': data.get('end_time'),
                    'person_id': data.get('person'),
                    'created_by': request.user,
                }
            )
            serializer = ProgramSerializer(program)
            return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)