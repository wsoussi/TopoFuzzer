from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import manage_mappings, manage_mapping, host_alloc, conntrack

urlpatterns = {
    path('mappings/', manage_mappings, name="mappings"),
    path('mappings/<slug:key>', manage_mapping, name="single_mapping"),
    path('host_alloc/', host_alloc, name="host_alloc"),
    path('conntrack/', conntrack, name="conntrack")
}
urlpatterns = format_suffix_patterns(urlpatterns)