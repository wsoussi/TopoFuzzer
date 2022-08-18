from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import manage_mappings, manage_mapping

urlpatterns = {
    path('mappings/', manage_mappings, name="mappings"),
    path('mappings/<slug:key>', manage_mapping, name="single_mapping")
}
urlpatterns = format_suffix_patterns(urlpatterns)