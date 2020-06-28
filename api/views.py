from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from segmentoj import tools
from problem.models import Problem, Tag
from .serializers import ProblemSerializer, TagSerializer

# Create your views here.
class UserView(APIView):

	def post(self, request):
		# Create user session(Login)
		data = request.data
		username = data.get('username')
		password = data.get('password')

		if not username or not password:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		user = auth.authenticate(request,username=username,password=password)

		if user:
			auth.login(request, user)
			return Response({
				"detail": "Success",
				"res": {
					"id": user.id
				}}, status=status.HTTP_201_CREATED)
		else:
			return Response({"detail": "Username or password wrong"}, status=status.HTTP_403_FORBIDDEN)

	def delete(self, request):
		# delete session(logout)

		if not request.user.is_authenticated:
			return Response({"detail": "Not logged in!"}, status=status.HTTP_401_UNAUTHORIZED)
		
		auth.logout(request)
		return Response(status=status.HTTP_204_NO_CONTENT)
	
	def put(self, request):
		# put a record(register an account)

		username = request.data.get('username')
		password = request.data.get('password')
		email = request.data.get('email')

		if not username or not password or not email:
			return Response(status.HTTP_400_BAD_REQUEST)

		if not tools.isEmail(email):
			return Response({"detail": "Email is not correct!"}, status=status.HTTP_400_BAD_REQUEST)

		try: 
			user = auth.models.User.objects.create_user(username=username, password=password, email=email)
		except IntegrityError:
			# failed, probably because username already exits
			return Response({"detail": "Failed to create user."}, status=status.HTTP_409_CONFLICT)

		if user: # Success
			user.save() # Save user

			return Response(status=status.HTTP_201_CREATED)
		else: # failed, probably because username already exits
			return Response({"detail": "Failed to create user."}, status=status.HTTP_409_CONFLICT)


class ProblemView(APIView):
	
	def get(self, request):
		# Get the conten of a problem

		data = request.data
		id = data.get('pid')

		if not id:
			return Response({"detail": "pid is required."}, status=status.HTTP_400_BAD_REQUEST)

		problem = get_object_or_404(Problem, show_id=id)

		if not problem.enabled and not request.user.has_perm('problem.view_hidden'):
			return Response({"detail": "Problem is hidden."}, status=status.HTTP_403_FORBIDDEN)
		
		ps = ProblemSerializer(problem)

		return Response(ps.get_problem(), status=status.HTTP_200_OK)

	@method_decorator(permission_required('problem.add_problem', raise_exception=True))
	def post(self, request):
		# Add a new problem

		data = request.data
		data['show_id'] = data.get('pid') # change pid to show_id

		ps = ProblemSerializer(data=data)
		ps.is_valid(raise_exception=True)
		ps.save()
		return Response(status=status.HTTP_201_CREATED)

	@method_decorator(permission_required('problem.change_problem', raise_exception=True))
	def patch(slef, request):
		data = request.data
		id = data.get('pid')

		if not id:
			return Response({"detail": "pid is required."}, status=status.HTTP_400_BAD_REQUEST)

		data['show_id'] = id

		problem = get_object_or_404(Problem, show_id=id)
		ps = ProblemSerializer(problem, data=data, partial=True)
		ps.is_valid(raise_exception=True)
		ps.save()
		return Response(status=status.HTTP_204_NO_CONTENT)
	
	@method_decorator(permission_required('problem.delete_problem'))
	def delete(self, request):
		data = request.data
		id = data.get('pid')

		if not id:
			return Response({"detail": "pid is required."}, status=status.HTTP_400_BAD_REQUEST)

		problem = get_object_or_404(Problem, show_id=id)
		problem.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


class TagView(APIView):

	def get(self, request):
		# Get a tag

		data = request.data
		id = data.get('id')

		if not id:
			return Response({"detail": "id is required"}, status=status.HTTP_400_BAD_REQUEST)

		tag = get_object_or_404(Tag, id=id)
		ts = TagSerializer(tag)

		return Response(ts.data, status=status.HTTP_200_OK)

	@method_decorator(permission_required('problem.add_tag', raise_exception=True))
	def post(slef, request):
		# add new tag
		data = request.data
		ts = TagSerializer(data=data)
		ts.is_valid(raise_exception=True)
		ts.save()
		return Response(status=status.HTTP_201_CREATED)