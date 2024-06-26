
from django.core.exceptions import ObjectDoesNotExist
from .models import Transaction, UserAccount
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import serializers


class UserAccountSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username if obj.user else None

    class Meta:
        model = UserAccount
        fields = ['id', 'username', 'account_no', 'balance', 'profile_image']


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password', 'confirm_password']

    def save(self):
        username = self.validated_data['username']
        email = self.validated_data['email']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        password = self.validated_data['password']
        password2 = self.validated_data['confirm_password']
        if password != password2:
            raise serializers.ValidationError(
                {'error': "Password doesn't match"})

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'error': "Email already exists"})
        user = User(username=username, email=email,
                    first_name=first_name, last_name=last_name)
        print(user)

        user.set_password(password)
        user.is_active = False
        user.save()
        UserAccount.objects.create(
            user=user, balance=0, account_no=int(user.id))
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class AllUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['account', 'amount']
        read_only_fields = ['balance_after_transaction', 'transaction_type']

    def validate_account(self, value):
        try:
            account = UserAccount.objects.get(id=value.id)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                {'error': 'Account does not exist'})
        return account

    def validate_amount(self, value):
        min_deposit_amount = 100

        if value > min_deposit_amount:
            return value
        else:
            raise serializers.ValidationError(
                f'Minimum deposit amount is {min_deposit_amount}')

    def create(self, validated_data):
        account = validated_data['account']
        amount = validated_data['amount']

        current_balance = account.balance
        new_balance = current_balance + amount

        account.balance = new_balance
        validated_data['transaction_type'] = 'Deposit'
        account.save()

        transaction = Transaction.objects.create(
            account=account, amount=amount, balance_after_transaction=new_balance, transaction_type='Deposit'
        )

        return transaction
