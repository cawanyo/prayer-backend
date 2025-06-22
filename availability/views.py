from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import Availability
from .serializers import AvailabilitySerializer
from accounts.permissions import ResponsablePermission
from accounts.serializers import CustomUserSerializer
from datetime import datetime

class AvailabilityUpsertView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, date):
        try:
            parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            return Response({"detail": "Invalid date format. Use YYYY-MM-DD."}, status=400)

        state = request.data.get("state")
        if state is None:
            return Response({"detail": "Missing 'state' field."}, status=400)

        # Try to get or create the availability
        availability, created = Availability.objects.get_or_create(
            user=request.user,
            date=parsed_date,
            defaults={"state": state}
        )

        if not created:
            availability.state = state
            availability.save()

        serializer = AvailabilitySerializer(availability)
        return Response(serializer.data, status=200 if not created else 201)


class AvailabilityView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request,date):
        availability = Availability.objects.filter(
                user=request.user,
                date=date
            ).first()
        if not availability:
            return Response({"detail": "Aucune demande trouvée."})
            

        serializer = AvailabilitySerializer(availability)
        return Response(serializer.data)
    

class AvailableUsersByDate(APIView):
    permission_classes = [permissions.IsAuthenticated, ResponsablePermission ]  # ou AllowAny si public

    def get(self, request, date):
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            return Response({"detail": "Format de date invalide. Utilise YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        availabilities = Availability.objects.filter(date=date_obj, state=True).select_related('user')
        users = [a.user for a in availabilities]

        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)