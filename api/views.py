from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import *
from .utils import *


import logging
import sys
logger = logging.getLogger(__name__)

class GetAuthTokenAPI(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key
        })
    
class CreateUserAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        response = {}
        response["status"] = "500"
        response["status_message"] = "Internal server Error"
        try:
            try:
                data = request.data
            except:
                response['status'] = 400
                response['status_message'] = "Malformed request body."
                return Response(data=response)
            
            email = data.get('email','')
            password = data.get('password','')
            full_name = data.get('full_name','')
            phone = data.get('phone','')
            address = data.get('address','')
            city = data.get('city','')
            state = data.get('state','')
            country = data.get('country','')
            pincode = data.get('pincode','')

            if email and password and full_name and phone and pincode:
                validator = UserValidator(email,password,full_name,phone,pincode)
                validation_errors = validator.validate_all()

                if validation_errors:
                    for error in validation_errors:
                        response['status'] = 400
                        response['status_message'] = error
                else:
                    first_name = full_name.split(" ")[0]
                    last_name = full_name.split(" ")[1]
                    user_obj = User.objects.filter(username=email) 
                    if not user_obj:
                        user_obj = User.objects.create(username=email, email=email, first_name=first_name,last_name=last_name,
                                                                phone=phone,address=address,city=city,state=state,country=country,
                                                                pincode=pincode,role='2')
                        user_obj.set_password(password)
                        user_obj.save()

                        response["pk"] = user_obj.pk
                        response["status"] = "200"
                        response["status_message"] = "Success"
                    else:
                        user_obj = user_obj.first()
                        user_obj.email = email
                        user_obj.first_name = first_name
                        user_obj.last_name = last_name
                        user_obj.phone = phone
                        user_obj.address = address
                        user_obj.city = city
                        user_obj.state = state
                        user_obj.country = country
                        user_obj.pincode = pincode
                        user_obj.set_password(password)
                        user_obj.save()

                        response["pk"] = user_obj.pk
                        response["status"] = "200"
                        response["status_message"] = "Data Updated"
            else:
                response['status'] = 400
                response['status_message'] = "email, password, full_name, phone and pincode are required."

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("CreateUserAPI Error %s at %s",str(e), str(exc_tb.tb_lineno))

        return Response(data=response)



class ContentItemsAPI(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        response = {}
        response["status"] = "500"
        response["status_message"] = "Internal server Error"
        try:
            try:
                data = request.data
            except:
                response['status'] = 400
                response['status_message'] = "Malformed request body."
                return Response(data=response)

            title = data.get('title','')
            body = data.get('body','')
            summary = data.get('summary','')
            document = data.get('document','')
            categories = data.get('categories','')

            username = request.user.username
            user_obj = User.objects.filter(username=str(username)).first()

            # if user is admin required and 
            if user_obj.role == "1":
                author = data.get('author_email','')
                if author == "":
                    response['status'] = 400
                    response['status_message'] = "author_email required for admin"
                    return Response(data=response)

                user_obj = User.objects.filter(username=str(username)).first()
                
                if not user_obj:
                    response['status'] = 400
                    response['status_message'] = "author not present in database"
                    return Response(data=response)
                
            if user_obj:
                if title and body and summary and document:
                    validator = ContentValidator(title,body,summary)
                    validation_errors = validator.validate_all()

                    if validation_errors:
                        for error in validation_errors:
                            response['status'] = 400
                            response['status_message'] = error
                    else:
                        content_obj, created = ContentItem.objects.get_or_create(title=title,user=user_obj)
                        content_obj.user = user_obj
                        content_obj.body = body
                        content_obj.summary = summary
                        content_obj.document = document

                        categories = categories.split(",")
                        for cat in categories:
                            category_obj, _ = Categories.objects.get_or_create(name=cat)
                            content_obj.categories.add(category_obj)

                        content_obj.save()
                        serializer = ContentItemSerializer(content_obj).data
                        response["content_data"] = serializer
                        if created:
                            response['status_message'] = "Success"
                        else:
                            response['status_message'] = "Data Updated"
                        response['status'] = 200
                else:
                    response['status'] = 400
                    response['status_message'] = "title, body, summary and document are required."
            else:
                response['status'] = 400
                response['status_message'] = "User is not registered"
                return Response(data=response)


        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("CreateUserAPI Error %s at %s",str(e), str(exc_tb.tb_lineno))

        return Response(data=response)

    def get(self, request, *args, **kwargs):
        response = {}
        response["status"] = "500"
        response["status_message"] = "Internal server Error"
        try:
            try:
                data = request.data
            except:
                response['status'] = 400
                response['status_message'] = "Malformed request body."
                return Response(data=response)
            
            title = data.get('title','')
            body = data.get('body','')
            summary = data.get('summary','')
            categories = data.get('categories','')

            username = request.user.username
            user_obj = User.objects.filter(username=str(username)).first()

            # check and get ContentItem by user wise
            content_obj = ContentItem.objects.all()
            if user_obj.role == "2":
                content_obj = content_obj.filter(user=user_obj)

            # get data by filter
            if title != '':
                content_obj = content_obj.filter(title__icontains=title)

            if body != '':
                content_obj = content_obj.filter(body__icontains=body)

            if summary != '':
                content_obj = content_obj.filter(summary__icontains=summary)
            
            if categories != '':
                content_obj = content_obj.filter(categories=categories)

            serializer = ContentItemSerializer(content_obj,many=True).data
            response["content_data"] = serializer
            response["status"] = "200"
            response["status_message"] = "Suucess"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("ContentItemsAPI Error %s at %s",str(e), str(exc_tb.tb_lineno))

        return Response(data=response)


GetAuthToken = GetAuthTokenAPI.as_view()
CreateUser = CreateUserAPI.as_view()
ContentItems = ContentItemsAPI.as_view()
