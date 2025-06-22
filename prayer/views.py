from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from .models import Prayer, PrayerCategory, Comment
from .serializers import PrayerSerializer, PrayerCategorySerializer, CommentSerializer
from accounts.permissions import ResponsablePermission
# PrayerCategory Views

class PrayerCategoryListCreateView(generics.ListCreateAPIView):
    queryset = PrayerCategory.objects.all()
    serializer_class = PrayerCategorySerializer
    permission_classes = [permissions.AllowAny]  # Anyone can view or create


class PrayerCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PrayerCategory.objects.all()
    serializer_class = PrayerCategorySerializer
    permission_classes = [permissions.AllowAny]


# Prayer Views

class PrayerCreateView(generics.CreateAPIView):
    queryset = Prayer.objects.all()
    serializer_class = PrayerSerializer

    def perform_create(self, serializer):
        # If the user is authenticated, save it; else leave user as null
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()

class PrayerListView(generics.ListAPIView):
    queryset = Prayer.objects.all()
    serializer_class = PrayerSerializer
    permission_classes = [permissions.IsAuthenticated, ResponsablePermission ]


class PrayerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Prayer.objects.all()
    serializer_class = PrayerSerializer
    permission_classes = [permissions.AllowAny]


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_prayers(request):
    prayers = Prayer.objects.filter(user=request.user)
    serializer = PrayerSerializer(prayers, many=True)
    print(request)
    return Response(serializer.data)

class PrayerCommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]  # or IsAuthenticated if needed

    def get_queryset(self):
        prayer_id = self.kwargs['prayer_id']
        return Comment.objects.filter(prayer_id=prayer_id)

    def perform_create(self, serializer):
        prayer_id = self.kwargs['prayer_id']
        serializer.save(prayer_id=prayer_id)
        

@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_prayer_state(request, pk):
    try:
        prayer = Prayer.objects.get(pk=pk)
    except Prayer.DoesNotExist:
        return Response({"detail": "Prayer not found"}, status=status.HTTP_404_NOT_FOUND)

    user = request.user
    is_owner = prayer.user == user
    is_responsable = user.groups.filter(name='responsable').exists()

    if not (is_owner or is_responsable):
        return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

    new_state = request.data.get('state')
    if new_state not in dict(Prayer.STATE_CHOICES):
        return Response({"detail": "Invalid state"}, status=status.HTTP_400_BAD_REQUEST)

    prayer.state = new_state
    prayer.save()

    return Response({"detail": "Prayer state updated", "state": prayer.state})