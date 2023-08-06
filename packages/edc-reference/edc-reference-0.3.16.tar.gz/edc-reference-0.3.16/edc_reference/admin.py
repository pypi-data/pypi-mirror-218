from django.contrib import admin
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_sites.admin import SiteModelAdminMixin

from .admin_site import edc_reference_admin
from .models import Reference


@admin.register(Reference, site=edc_reference_admin)
class ReferenceAdmin(SiteModelAdminMixin, ModelAdminSubjectDashboardMixin, admin.ModelAdmin):
    date_hierarchy = "report_datetime"

    list_display = (
        "identifier",
        "dashboard",
        "model",
        "report_datetime",
        "visit",
        "timepoint",
        "field_name",
        "value",
    )
    list_filter = ("model", "timepoint", "field_name")
    search_fields = (
        "identifier",
        "value_str",
        "value_int",
        "value_date",
        "value_datetime",
        "value_uuid",
    )

    def visit(self, obj=None):
        return f"{obj.visit_code}.{obj.visit_code_sequence}"
