from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from .permission import IsAdmin
from .serializers import DuckSerializer
from .permission import IsAdmin

from .models import Duck, Player

@api_view(['POST'])
def register_api(request):
    username = request.data.get('username')
    password = request.data.get('password')
    print(username, password, "this is the user name and password")

    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.create_user(username=username, password=password)
        Token.objects.create(user=user)  # Generate a token for authentication if needed
        return Response({'success': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):

    username = request.data.get('username')
    password = request.data.get('password')
    print(username, password, 'eski endezi eneyew ayshalmm apapicho')

    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        player, created=Player.objects.get_or_create(user=user)
        
        if created:
            player.currency==0.00
            player.save()  
      
        
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
@api_view(['POST'])
def user_logout(request):
    if not request.user.is_authenticated:
        return Response({"message": "Authentication required."}, status=401)

    logout(request)

    return Response({"message": "User logged out successfully"}, status=200)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def user_delete_api(request):
    """
    API endpoint to delete the authenticated user's account.
    """
    user = request.user

    try:
        user.delete()  # Deletes the user account
        return Response({'success': 'User account deleted successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': f'Failed to delete user: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['PUT'])
def modify_user(request):
    if not request.user.is_authenticated:
        return Response({"message": "Authentication required."}, status=401)

    user = request.user
    
    username = request.data.get('username')
    email = request.data.get('email')

    if username:
        user.username = username
    if email:
        user.email = email

    if 'password' in request.data:
        user.set_password(request.data['password'])  # Hash the password properly

    user.save()

    return Response({"message": "User updated successfully", "username": user.username, "email": user.email}, status=status.HTTP_200_OK) 


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAdmin])
def create_gacha(request):
    """
    API endpoint to create a new gacha.
    """
    serializer = DuckSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': 'Gacha created successfully!', 'data': serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['PUT'])
@permission_classes([IsAdmin])
def update_gacha(request, gacha_id):
    """
    API endpoint to update an existing gacha.
    """
    try:
        gacha = Duck.objects.get(id=gacha_id)
        serializer = DuckSerializer(gacha, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'Gacha updated successfully!', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Duck.DoesNotExist:
        return Response({'error': 'Gacha not found'}, status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@api_view(['DELETE'])
@permission_classes([IsAdmin])
def delete_gacha(request, gacha_id):
    """
    API endpoint to delete a gacha.
    """
    try:
        gacha = Duck.objects.get(id=gacha_id)
        gacha.delete()
        return Response({'success': 'Gacha deleted successfully!'}, status=status.HTTP_200_OK)
    except Duck.DoesNotExist:
        return Response({'error': 'Gacha not found'}, status=status.HTTP_404_NOT_FOUND)
    
@csrf_exempt
@api_view(['GET'])
@permission_classes([ IsAdmin])
def admin_view_all_gachas(request):
    """
    API endpoint to retrieve all gachas in the system.
    """
    gachas = Duck.objects.all()
    serializer = DuckSerializer(gachas, many=True)
    return Response({'gachas': serializer.data}, status=status.HTTP_200_OK)


 
