import jwt
import requests
import json
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError, ValidationError, NotFound
from .serializers import PrivateUserSerializer
from .models import User
from utils.auth import issue_app_jwt


class Me(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = PrivateUserSerializer(user)
        return Response(PrivateUserSerializer(user).data)

    def put(self, request):
        user = request.user
        serializer = PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = PrivateUserSerializer(user)
            return Response(serializer.data)

        else:
            return Response(serializer.errors)


class Users(APIView):
    @transaction.atomic
    def post(self, request):
        data = request.data
        password = data.get("password")
        if not password:
            raise ParseError("password is required")
        if len(password) < 4:
            raise ValidationError("Password length error")

        email = data.get("email")
        username = data.get("username")
        name = data.get("name")

        if User.objects.filter(email=email).exists():
            return Response({"detail": "이미 가입된 사용자"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            email=email,
            username=username,
            password=password, 
        )
        if name:
            user.name = name
            user.save(update_fields=["name"])
        login(request, user) 
        return Response({"ok": True}, status=status.HTTP_201_CREATED)

class PublicUser(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound
        serializer = PrivateUserSerializer(user)
        return Response(serializer.data)


class ChangePassword(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise ParseError
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogIn(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            login(request, user)
            return Response({"ok": "Welcome!"})
        else:
            return Response(
                {"error": "wrong password"}, status=status.HTTP_401_UNAUTHORIZED
            )


class LogOut(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok": "bye!"})


class JWTLogIn(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            token = jwt.encode(
                {"pk": user.pk},
                settings.SECRET_KEY,
                algorithm="HS256",
            )
            return Response({"token": token})
        else:
            return Response({"error": "wrong password"})


class GithubLogIn(APIView):

    def post(self, request):
        try:
            code = request.data.get("code")

            access_token = requests.post(
                f"https://github.com/login/oauth/access_token?code={code}&client_id=Ov23liRsfBLCuzEBIEZG&client_secret={settings.GH_SECRET}",
                headers={"Accept": "application/json"},
            )

            access_token = access_token.json().get("access_token")
            user_data = requests.get(
                "https://api.github.com/user",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            user_data = user_data.json()

            user_emails = requests.get(
                "https://api.github.com/user/emails",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            user_emails = user_emails.json()
            username = (user_data.get("login"),)
            email = (user_emails[0]["email"],)
            name = (user_data.get("name"),)
            avatar = (user_data.get("avatar_url"),)
            if user_emails[0]["verified"] == True:
                try:
                    user = User.objects.get(email=user_emails[0]["email"])
                    login(request, user)
                    return Response(status=status.HTTP_200_OK)
                except User.DoesNotExist:
                    user = User.objects.create(
                        username=user_data.get("login"),
                        email=user_emails[0]["email"],
                        name=user_data.get("id"),
                        avatar=user_data.get("avatar_url"),
                    )
                    user.set_unusable_password()
                    user.save()
                    login(request, user)
                    return Response(status=status.HTTP_200_OK)
            else:
                return Response({"error": "인증되지 않은 계정입니다."})
        except Exception as e:
            import traceback

            print("❌ 예외:", e)
            print(traceback.format_exc())
            return Response(status=status.HTTP_400_BAD_REQUEST)


class KakaoLogIn(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")
            access_token = requests.post(
                "https://kauth.kakao.com/oauth/token",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
                },
                data={
                    "grant_type": "authorization_code",
                    "client_id": "6da7da66688ba381beec154a612d06af",
                    "redirect_uri": "http://127.0.0.1:3000/social/kakao",
                    "code": code,
                },
            )
            access_token = access_token.json().get("access_token")
            user_data = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
                },
            )
            user_data = user_data.json()
            kakao_account = user_data.get("kakao_account")
            profile = kakao_account.get("profile")
            try:
                user = User.objects.get(email=kakao_account.get("email"))
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                user = User.objects.create(
                    email=kakao_account.get("email"),
                    username=profile.get("nickname"),
                    name=profile.get("nickname"),
                    avatar=profile.get("profile_image_url"),
                )
                user.set_unusable_password()
                user.save()
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        except Exception as e:
            import traceback

            print("❌ 예외:", e)
            print(traceback.format_exc())
            return Response(status=status.HTTP_400_BAD_REQUEST)




# class KakaoLogInJWT(APIView):
#     permission_classes = []  # AllowAny면 생략해도 됨

#     def post(self, request):
#         code = request.data.get("code")
#         if not code:
#             return Response({"error": "code required"}, status=status.HTTP_400_BAD_REQUEST)

#         # 1) 코드 → 카카오 액세스 토큰 교환
#         try:
#             token_res = requests.post(
#                 "https://kauth.kakao.com/oauth/token",
#                 headers={"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"},
#                 data={
#                     "grant_type": "authorization_code",
#                     "client_id": settings.KAKAO_CLIENT_ID,
#                     "redirect_uri": settings.KAKAO_REDIRECT_URI,
#                     "code": code,
#                 },
#                 timeout=5,
#             )
#         except requests.RequestException:
#             return Response({"error": "token_request_failed"}, status=status.HTTP_400_BAD_REQUEST)

#         if token_res.status_code != 200:
#             return Response({"error": "token_exchange_failed", "detail": token_res.text}, status=status.HTTP_400_BAD_REQUEST)

#         tokens = token_res.json()
#         access_token = tokens.get("access_token")
#         if not access_token:
#             return Response({"error": "no_access_token", "detail": tokens}, status=status.HTTP_400_BAD_REQUEST)

#         # 2) 액세스 토큰으로 카카오 사용자 정보 조회
#         try:
#             me_res = requests.get(
#                 "https://kapi.kakao.com/v2/user/me",
#                 headers={
#                     "Authorization": f"Bearer {access_token}",
#                     "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
#                 },
#                 timeout=5,
#             )
#         except requests.RequestException:
#             return Response({"error": "userinfo_request_failed"}, status=status.HTTP_400_BAD_REQUEST)

#         if me_res.status_code != 200:
#             return Response({"error": "userinfo_failed", "detail": me_res.text}, status=status.HTTP_400_BAD_REQUEST)

#         data = me_res.json()
#         kakao_id = data.get("id")
#         kakao_account = (data.get("kakao_account") or {})
#         profile = (kakao_account.get("profile") or {})
#         email = kakao_account.get("email")  # 동의 안 했다면 None일 수 있음
#         nickname = profile.get("nickname") or f"kakao_{kakao_id}"
#         avatar_url = profile.get("profile_image_url") or ""

#         if not kakao_id:
#             return Response({"error": "invalid_kakao_response"}, status=status.HTTP_400_BAD_REQUEST)

#         # 3) 우리 서비스 유저 upsert (이메일 없을 수도 있으니 대체값 생성)
#         #  - 네 User 모델 필드에 맞춰 수정: profile_image, nickname 등
#         user, created = User.objects.get_or_create(
#             email=email or f"{kakao_id}@kakao.local",
#             defaults={
#                 "username": nickname,
#                 "nickname": nickname,
#                 "avatar": avatar_url,  # 네 모델이 avatar가 아니라 profile_image였던 점 주의!
#             },
#         )
#         # 필요하면 최초 로그인 시 추가 업데이트
#         if not created:
#             changed = False
#             if not user.nickname and nickname:
#                 user.nickname = nickname; changed = True
#             if avatar_url and user.profile_image != avatar_url:
#                 user.profile_image = avatar_url; changed = True
#             if changed:
#                 user.save(update_fields=["nickname", "profile_image"])

#         # 4) 세션 로그인 대신, 우리 서비스용 JWT 발급
#         token = issue_app_jwt(user)

#         return Response(
#             {
#                 "token": token,
#                 "user": {
#                     "id": user.id,
#                     "email": user.email,
#                     "username": user.username,
#                     "nickname": user.nickname,
#                     "profile_image": user.profile_image,
#                 },
#             },
#             status=200,
#         )