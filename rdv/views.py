from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import RDV, RDVAvailability
from accounts.permissions import ResponsablePermission
from .serializers import RDVSerializer, RDVAvailabilitySerializer
from rest_framework.pagination import PageNumberPagination


class CustomRDVPagination(PageNumberPagination):
    page_size = 31
    
    
class RDVCreateView(generics.CreateAPIView):
    serializer_class = RDVSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class RDVListView(generics.ListAPIView):
    serializer_class = RDVSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomRDVPagination

    def get_queryset(self):
        return RDV.objects.filter(created_by=self.request.user)

class AllRDVListView(generics.ListAPIView):
    serializer_class = RDVSerializer
    permission_classes = [permissions.IsAuthenticated, ResponsablePermission]

    def get_queryset(self):
        return RDV.objects.filter(state='pending')

class ValidateRDVAvailabilityView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, rdv_id, avail_id):
        try:
            rdv = RDV.objects.get(id=rdv_id)
            availability = RDVAvailability.objects.get(id=avail_id)

            if availability not in rdv.rdv_availabilities.all():
                return Response({'error': 'Availability does not belong to this RDV'}, status=400)

            rdv.selected_availability = availability
            rdv.validated_by = request.user
            rdv.save()

            return Response({'success': 'RDV validated'}, status=200)
        except RDV.DoesNotExist:
            return Response({'error': 'RDV not found'}, status=404)
        except RDVAvailability.DoesNotExist:
            return Response({'error': 'Availability not found'}, status=404)


class RDVByDateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, date):
        try:
            rdv = RDV.objects.filter(created_by=request.user, date=date).first()
            if not rdv:
                return Response({"detail": "Aucun rendez-vous trouvé."}, status=status.HTTP_404_NOT_FOUND)
            serializer = RDVSerializer(rdv)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        


class RDVUpdateView(generics.RetrieveUpdateAPIView):
    queryset = RDV.objects.all()
    serializer_class = RDVSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        data = request.data

        is_responsable = user.groups.filter(name="responsable").exists()

        # Restriction des champs modifiables
        restricted_fields = {'state', 'date', 'time', 'selected_availability'}

        if not is_responsable:
            for field in restricted_fields:
                if field in data:
                    return Response(
                        {"error": f"Le champ '{field}' ne peut être modifié que par un responsable."},
                        status=status.HTTP_403_FORBIDDEN
                    )

        return self.partial_update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save()
        
        
class DeleteRDVView(generics.DestroyAPIView):
    queryset = RDV.objects.all()
    serializer_class = RDVSerializer
    permission_classes = [permissions.IsAuthenticated]

class AvailabilityView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RDVAvailability.objects.all()
    serializer_class = RDVAvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    