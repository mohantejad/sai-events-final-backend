from django.db.models import Q
import django_filters
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission
from .models import Event
from .serializers import EventSerializer

class IsEventCreator(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user

class EventFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(field_name="city", lookup_expr="iexact")
    search = django_filters.CharFilter(method="filter_by_keyword")
    event_category = django_filters.CharFilter(field_name="event_category", lookup_expr="iexact")
    date = django_filters.CharFilter(method="filter_by_date")

    class Meta:
        model = Event
        fields = ["city", "event_category"]

    def filter_by_keyword(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) | Q(description__icontains=value)
        )

    def filter_by_date(self, queryset, name, value):
        from datetime import date, timedelta

        today = date.today()
        if value.lower() == "today":
            return queryset.filter(date=today)
        elif value.lower() == "tomorrow":
            return queryset.filter(date=today + timedelta(days=1))
        elif value.lower() == "this_weekend":
            return queryset.filter(date__week_day__in=[6, 7])
        return queryset

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = (filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend)
    filterset_class = EventFilter
    search_fields = ["city", "title", "description"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        elif self.action == "create":
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsEventCreator()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
