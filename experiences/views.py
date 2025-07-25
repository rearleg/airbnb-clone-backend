from django.db import transaction
from django.conf import settings
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.status import HTTP_204_NO_CONTENT
from .models import Experience, Perk
from .serializers import PerkSerializer, ExperienceSerializer
from categories.models import Category
from bookings.models import Booking
from bookings.serializers import (
    PublicBookingSerializer,
    CreateExperienceBookingSerializer,
)
from reviews.models import Review
from reviews.serializers import ReviewSerializer


class Experiences(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_experiences = Experience.objects.all()
        serializer = ExperienceSerializer(
            all_experiences,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = ExperienceSerializer(data=request.data)
        if serializer.is_valid():
            # 카테고리 검증
            category_id = request.data.get("category")
            if not category_id:
                raise ParseError("Category is required.")
            try:
                category = Category.objects.get(pk=category_id)
                if category.kind == Category.CategoryKindChoices.ROOMS:
                    raise ParseError("The category kind should be 'experience'")
            except Category.DoesNotExist:
                raise NotFound
            try:
                with transaction.atomic():
                    updated_experience = serializer.save(
                        host=request.user,
                        category=category,
                    )
                    perks = request.data.get("perks")
                    for perk_pk in perks:
                        perk = Perk.objects.get(pk=perk_pk)
                        updated_experience.perks.add(perk)
                    serializer = ExperienceSerializer(updated_experience)
                    return Response(serializer.data)
            except Exception:
                raise ParseError("Perk Not Found.")
        else:
            return Response(serializer.errors)


class ExperienceDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        serializer = ExperienceSerializer(experience)
        return Response(serializer.data)

    def put(self, request, pk):
        experience = self.get_object(pk)
        if experience.host != request.user:
            raise PermissionError
        serializer = ExperienceSerializer(
            experience,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            category = None
            if request.data.get("category"):
                category_pk = request.data.get("category")
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.ROOMS:
                        raise ParseError("Category should be 'experience'")
                except Category.DoesNotExist:
                    raise ParseError("Category Not Found.")
            with transaction.atomic():
                updated_experience = serializer.save(
                    host=request.user,
                    category=category,
                )
                if request.data.get("perks"):
                    perks = request.data.get("perks")
                    for perk_pk in perks:
                        perk = Perk.objects.get(pk=perk_pk)
                        updated_experience.perks.add(perk)
                    serializer = ExperienceSerializer(updated_experience)
                return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        experience = self.get_object(pk)
        if experience.host != request.user:
            raise PermissionError
        experience.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class ExperiencePerks(APIView):

    def get_objects(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        experience = self.get_objects(pk)
        serializer = PerkSerializer(
            experience.perks.all()[start:end],
            many=True,
        )
        return Response(serializer.data)


class ExperienceBookings(APIView):
    """[ ] GET POST /experiences/1/bookings"""

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        now = timezone.localtime(timezone.now()).date()
        bookings = Booking.objects.filter(
            experience=experience,
            kind=Booking.BookingKindChoices.EXPERIENCE,
            experience_time__gt=now,
        )
        serializer = PublicBookingSerializer(
            bookings,
            many=True,
        )
        return Response(serializer.data)

    def post(self, requst, pk):
        pass


class ExperienceBookingsDetail(APIView):
    """[ ] GET PUT DELETE /experiences/1/bookings/2"""

    permission_classes = [IsAuthenticated]

    def get_objects(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except:
            return NotFound("Experience Not Found")

    def get(self, request, pk, booking_pk):
        experience = self.get_objects(pk)
        try:
            booking = Booking.objects.get(
                pk=booking_pk,
                experience=experience,
            )
        except Booking.DoesNotExist:
            raise NotFound("Booking Not Found")
        serializer = PublicBookingSerializer(booking)
        return Response(serializer.data)

    def put(self, request, pk, booking_pk):
        experience = self.get_objects(pk)
        if request.user != experience.host:
            raise PermissionError
        try:
            booking = Booking.objects.get(pk=booking_pk, experience=experience)
        except Booking.DoesNotExist:
            raise NotFound("Booking Not Found")
        serializer = CreateExperienceBookingSerializer(
            booking,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_booking = serializer.save()
            serializer = CreateExperienceBookingSerializer(updated_booking)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk, booking_pk):
        experience = self.get_objects(pk)
        try:
            booking = Booking.objects.get(pk=booking_pk, experience=experience)
        except Booking.DoesNotExist:
            raise NotFound("Booking Not Found")
        if request.user == experience.host:
            booking.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        else:
            raise PermissionError


class ExperienceReviews(APIView):

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound("Experience Not Found")

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        experience = self.get_object(pk)
        serializer = ReviewSerializer(
            experience.reviews.all()[start:end],
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = ReviewSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            review = serializer.save(
                user=request.user,
                experience=self.get_object(pk),
            )
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class Perks(APIView):

    def get(self, request):
        all_perks = Perk.objects.all()
        serializer = PerkSerializer(
            all_perks,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = PerkSerializer(data=request.data)
        if serializer.is_valid():
            perk = serializer.save()
            return Response(PerkSerializer(perk).data)
        else:
            return Response(serializer.errors)


class PerkDetail(APIView):

    def get_objects(self, pk):
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        perk = self.get_objects(pk)
        serializer = PerkSerializer(perk)
        return Response(serializer.data)

    def put(self, request, pk):
        perk = self.get_objects(pk)
        serializer = PerkSerializer(
            perk,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_perk = serializer.save()
            return Response(PerkSerializer(updated_perk).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        perk = self.get_objects(pk)
        perk.delete()
        return Response(status=HTTP_204_NO_CONTENT)
