from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.models import Group

from .models import CustomUser, MemberDemand
from .serializers import CustomUserSerializer, MemberDemandSerializer, UserUpdateSerializer
from .permissions import ResponsablePermission


class RegisterUserView(generics.CreateAPIView):
    """
     Registration View 
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    
class UpdateOwnInfoView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

@api_view(['GET'])
def check_username(request):
    """
        Check if the username already exist
    """
    username = request.query_params.get('username')
    if username is None:
        return Response({'error': 'Username parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

    exists = CustomUser.objects.filter(username=username).exists()
    return Response({'available': not exists})

@api_view(['GET'])
def check_email(request):
    """
        Check if the email already exist
    """
    email = request.query_params.get('email')
    if email is None:
        return Response({'error': 'Email parameter is required.'}, status=400)

    exists = CustomUser.objects.filter(email=email).exists()
    return Response({'available': not exists})



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_view(request):
    """ 
        Retrieve the information of the current user
    """
    serializer = CustomUserSerializer(request.user)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def is_intercesseur(request):
    """ 
        Check if the current user is a member of the intercesseur group
    """
    user = request.user
    in_group = user.groups.filter(name="intercesseur").exists()
    return Response({"is_intercesseur": in_group})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def is_responsable(request):
    """ 
        Check if the current user is a member of the responsable group
    """
    user = request.user
    in_group = user.groups.filter(name="responsable").exists()
    return Response({"is_responsable": in_group})





class MemberDemandCreateView(generics.CreateAPIView):
    """ 
        Create a request to join the intercesseur group
    """
    queryset = MemberDemand.objects.all()
    serializer_class = MemberDemandSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)
        


class MemberDemandListView(generics.ListAPIView):
    """ 
        List the requests to join the intercesseur group
    """
    
    queryset = MemberDemand.objects.all()
    serializer_class = MemberDemandSerializer
    permission_classes = [IsAuthenticated, ResponsablePermission]


class MemberDemandUpdateView(generics.RetrieveUpdateAPIView):
    """ 
        Update the requests to join the intercesseur group
    """
    queryset = MemberDemand.objects.all()
    serializer_class = MemberDemandSerializer
    permission_classes = [IsAuthenticated, ResponsablePermission]

    def perform_update(self, serializer):
        demand = serializer.save(validated_by=self.request.user)
        # If the state was changed to 'accepted', add requester to group
        intercesseur_group, _ = Group.objects.get_or_create(name='intercesseur')
        user = demand.requester
        if demand.state == 'accepted':
            user.groups.add(intercesseur_group)
        elif demand.state == 'refused':
            user.groups.remove(intercesseur_group)


class MembershipRequestView(APIView):
    """ 
        View the equest to join the intercesseur group of the current user
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            latest_request = MemberDemand.objects.filter(requester=request.user).first()
        except MemberDemand.DoesNotExist:
            return Response({"detail": "Aucune demande trouvée."}, status=status.HTTP_404_NOT_FOUND)

        serializer = MemberDemandSerializer(latest_request)
        return Response(serializer.data)
    
    


