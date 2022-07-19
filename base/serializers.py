from rest_framework import serializers
from .models import Category, Wallet, Transactions, User
from rest_framework.authtoken.models import Token
from django.db import transaction
from django.db.models import F


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class CategorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data):
        return Category.objects.create(user=self.context['user'], **validated_data)

class UserRegisterSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, write_only=True)
    token = serializers.CharField(max_length=100, read_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        token = Token.objects.create(user=user)

        return {
            'id': user.id,
            'username': user.username,
            'token': token.key,
        }
        


class WalletTransactionSerializer(serializers.Serializer):
    category_id = serializers.IntegerField(read_only=True)
    amount = serializers.IntegerField()
    photo = serializers.ImageField()
    _type = serializers.CharField(max_length=3, read_only=True)
    date = serializers.DateTimeField(read_only=True)
    comment = serializers.CharField()

    def create(self, validated_data):
        category = self.context.pop('category_id', None)

        with transaction.atomic():
            wallet = Wallet.objects.select_for_update().get(user=self.context['user'])
            wallet_transaction = Transactions(
                wallet=wallet,
                **validated_data,
                )
            if category:
                if Category.objects.filter(user=self.context['user'], id=category).count() == 0:
                    raise serializers.ValidationError({'detail': 'Kechirasiz, sizda bunday kategoriya mavjud emas!'})
                category = Category.objects.get(id=category)
                wallet.balance = F('balance') - validated_data['amount']
                wallet.save()
                wallet_transaction.category = category
                wallet_transaction._type = Transactions.OUT
                
            else: 
                wallet.balance = F('balance') + validated_data['amount']
                wallet.save()
                wallet_transaction._type = Transactions.IN
            wallet_transaction.save()
        return wallet_transaction

class CategoryOutcomeSerializer(serializers.Serializer):
    category = serializers.SerializerMethodField(read_only=True)
    total_sum = serializers.IntegerField(read_only=True)

    @staticmethod
    def get_category(obj):
        return obj['category__name']



