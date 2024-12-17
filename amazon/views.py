from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import serializers
from amazon.serializers import ProductModelSerializer, UserModelSerializer
from amazon.models import Product, User
from django.utils import timezone
from django.db import transaction

# Create your views here.

class RegisterUser(APIView):
    permission_classes = []
    authentication_classes = []

    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField()
        first_name = serializers.CharField()
        last_name = serializers.CharField()

        class Meta:
            ref_name = "UserInputSerializer"
    
    class OutputSerializer(UserModelSerializer):
        user_id = serializers.IntegerField(source="id")

        class Meta(UserModelSerializer.Meta):
            ref_name = "UserOutputSerializer"
            fields = ('user_id',)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = self.request.data
        user = User.objects.filter(username=data.get("username")).first()
        if not user:
            serializer = self.InputSerializer(data=data)
            if serializer.is_valid():
                user_data = serializer.validated_data
                user = User()
                user.email = user_data.get("email")
                user.first_name = user_data.get("first_name")
                user.last_name = user_data.get("last_name")
                user.set_password(user_data.get("password"))
                user.save()
                return Response(self.OutputSerializer(user).data, status=201)
            else:
                return Response(serializer.errors, status=400)
        else:
            return Response("User already registered with this username.", status=400)
    

class LoginUser(APIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [JWTAuthentication]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        return Response("User logged in successfully", status=200)
        

class AddProductApi(APIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [JWTAuthentication]

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=150)
        description = serializers.CharField()
        price = serializers.DecimalField(max_digits=10, decimal_places=2)
        quantity = serializers.IntegerField()

        class Meta:
            ref_name = "ProductInputSerializer"

    class OutputSerializer(ProductModelSerializer):
        product_id = serializers.IntegerField()

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = self.request.data
        serializer = self.InputSerializer(data=data)
        try:
            if serializer.is_valid():
                product_data = serializer.validated_data
                obj = Product()
                obj.name = product_data.get("name")
                obj.price = product_data.get("price")
                obj.description = product_data.get("description")
                obj.quantity = product_data.get("quantity")
                obj.created_by_id = self.request.user_id
                obj.save()
                obj_data = self.OutputSerializer(obj).data
                return Response(obj_data.get("id"), status=201)
        except Exception as e:
            return Response(str(e), status=400)
        
class ProductUpdateAPI(APIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [JWTAuthentication]

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=150)
        description = serializers.CharField()
        price = serializers.DecimalField(max_digits=10, decimal_places=2)
        quantity = serializers.IntegerField()

        class Meta:
            ref_name = "ProductUpdateInputSerializer"
    
    @transaction.atomic
    def put(self, request, product_id, *args, **kwargs):
        data = self.request.data
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return Response("Product not found", status=404)
        serializer = self.InputSerializer(data=data)
        try:
            if serializer.is_valid():
                product_data = serializer.validated_data
                product.name = product_data.get("name")
                product.price = product_data.get("price")
                product.description = product_data.get("description")
                product.quantity = product_data.get("quantity")
                product.updated_by_id = self.request.user_id
                product.save()
                return Response("Product updated successfully", status=200)
        except Exception as e:
            return Response(str(e), status=400)


class ProductListApi(APIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [JWTAuthentication]

    class OutputSerializer(ProductModelSerializer):
        class Meta(ProductModelSerializer.Meta):
            fields = '__all__'

    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(deleted_at__isnull=True)
        data = self.OutputSerializer(products, many=True).data
        return Response(data, status=200)


class ProductDeleteApi(APIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [JWTAuthentication]

    @transaction.atomic
    def delete(self, request, product_id, *args, **kwargs):
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return Response("Product not found", status=404)
        product.deleted_at = timezone.now()
        product.deleted_by_id = self.request.user_id
        product.save()
        return Response("Product deleted successfully", status=200)