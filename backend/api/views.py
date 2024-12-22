from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import BusinessUser
from .serializers import BusinessUserSerializer
from .serializers import RegisterSerializer, SystemUserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


SystemUser = get_user_model()

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def business_user_list(request):
    if request.method == 'GET':
        # Retrieve all businessUsers from the database
        businessUsers = BusinessUser.objects.all()
        # Serialize the queryset of businessUsers
        serializer = BusinessUserSerializer(businessUsers, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # Create a new business_user from the request data
        serializer = BusinessUserSerializer(data=request.data)
        if serializer.is_valid():
            # Save the new business_user if data is valid
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Return validation errors if data is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def business_user_delete(request, pk):
    try:
        # Attempt to find the business_user by primary key
        business_user = BusinessUser.objects.get(pk=pk)
    except BusinessUser.DoesNotExist:
        # Return 404 if business_user doesn't exist
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # Delete the business_user and return success response
    business_user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    print(request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED
        )
    else:
        print(serializer.errors)
    return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def business_user_update(request, pk):
    business_user = get_object_or_404(BusinessUser, pk=pk)
    serializer = BusinessUserSerializer(business_user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_concrete_business_user(request, pk):
    business_user = get_object_or_404(BusinessUser, pk=pk)
    serializer = BusinessUserSerializer(business_user)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_me(request):
    user = request.user
    serializer = SystemUserSerializer(user)
    return Response(serializer.data)