from django.contrib.auth import get_user_model, login, logout
from django.middleware.csrf import get_token
from django.db import transaction
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Profile
from .serializers import RegistrationSerializer

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    @transaction.atomic
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        if User.objects.filter(username=data["username"]).exists() or User.objects.filter(email=data["email"]).exists():
            return Response({"detail": "اسم المستخدم أو البريد مسجل مسبقاً."}, status=status.HTTP_400_BAD_REQUEST)
        if data["requested_role"] in (Profile.RequestedRole.VOLUNTEER, Profile.RequestedRole.COMMITTEE_LEAD) and not data.get("requested_committee"):
            return Response({"detail": "يرجى تحديد اللجنة المطلوبة."}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(
            username=data["username"], email=data["email"], password=data["password"],
            first_name=data["first_name"], last_name=data.get("last_name", ""), is_active=False,
        )
        Profile.objects.create(
            user=user, university_id=data["university_id"], phone=data.get("phone", ""),
            requested_role=data["requested_role"], status=Profile.Status.PENDING,
            requested_committee=data.get("requested_committee", ""),
        )
        return Response({"status": "pending", "detail": "استلمنا طلب إنشاء الحساب. تفعّل الصلاحيات بعد تحقق الإدارة من الانتساب والدور."}, status=status.HTTP_201_CREATED)

class SessionView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({"authenticated": False})
        profile = getattr(user, "profile", None)
        if not user.is_active or not profile or profile.status != Profile.Status.ACTIVE:
            return Response({"authenticated": True, "active": False, "detail": "الحساب بانتظار اعتماد الإدارة."})
        roles = list(user.role_assignments.filter(is_active=True).values_list("role", flat=True))
        committees = list(user.committee_memberships.filter(status="active").values("committee__name", "role"))
        return Response({"authenticated": True, "active": True, "name": user.get_full_name(), "email": user.email, "roles": roles, "committees": committees})

    def post(self, request):
        if request.data.get("action") == "logout":
            logout(request)
            return Response({"authenticated": False})
        from django.contrib.auth import authenticate
        user = authenticate(request, username=request.data.get("username"), password=request.data.get("password"))
        if not user:
            return Response({"detail": "بيانات الدخول غير صحيحة أو الحساب غير معتمد."}, status=status.HTTP_401_UNAUTHORIZED)
        login(request, user)
        profile = getattr(user, "profile", None)
        return Response({"authenticated": True, "active": bool(profile and profile.status == Profile.Status.ACTIVE)})

class CsrfView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    def get(self, request):
        return Response({"csrfToken": get_token(request)})
