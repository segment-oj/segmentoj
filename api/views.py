from account.models import User
from django.contrib import auth
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


from segmentoj import tools
from segmentoj.decorator import syllable_required

# Create your views here.
class UserView(APIView):
    throttle_scope = "user"

    @method_decorator(syllable_required('username', str))
    @method_decorator(syllable_required('password', str))
    def post(self, request):
        # Create user session(Login)
        data = request.data
        username = data.get('username')
        password = data.get('password')

        user = auth.authenticate(request, username=username,password=password)

        if user:
            auth.login(request, user)
            return Response({
                'detail': 'Success',
                'res': {
                    'id': user.id
                }}, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'Username or password wrong'}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request):
        # delete session(logout)

        if not request.user.is_authenticated:
            return Response({'detail': 'Not logged in!'}, status=status.HTTP_401_UNAUTHORIZED)
        
        auth.logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @method_decorator(syllable_required('username', str))
    @method_decorator(syllable_required('password', str))
    @method_decorator(syllable_required('email', str))
    def put(self, request):
        # put a record(register an account)

        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if len(password) < 6:
            return Response({
                'detail': 'Password too short'
            }, status=status.HTTP_400_BAD_REQUEST)

        if not tools.isEmail(email):
            return Response({'detail': 'Email is not correct'}, status=status.HTTP_400_BAD_REQUEST)

        try: 
            user = User.objects.create_user(username=username, password=password, email=email)
        except IntegrityError:
            # failed, probably because username already exits
            return Response({'detail': 'Failed to create user.'}, status=status.HTTP_409_CONFLICT)

        if user: # Success
            user.save() # Save user

            return Response(status=status.HTTP_201_CREATED)
        else: # failed, probably because username already exits
            return Response({'detail': 'Failed to create user.'}, status=status.HTTP_409_CONFLICT)
