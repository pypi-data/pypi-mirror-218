from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from ..site_reference import site_reference_configs


class ReferenceGetterError(Exception):
    pass


class ReferenceObjectDoesNotExist(Exception):
    pass


class ReferenceGetter:
    """A class that gets the reference model instance for a given
    model or attributes of the model.

    See also ReferenceModelMixin.
    """

    def __init__(
        self,
        name: str | None = None,
        field_name: str | None = None,
        model_obj=None,
        related_visit=None,
        subject_identifier: str | None = None,
        report_datetime: datetime | None = None,
        visit_schedule_name: str | None = None,
        schedule_name: str | None = None,
        visit_code: str | None = None,
        visit_code_sequence: str | None = None,
        timepoint: Decimal | None = None,
        site=None,
        create=None,
    ):
        self._object = None
        self.created = None
        self.value = None
        self.has_value = False

        self.create = create
        self.field_name = field_name
        if model_obj:
            try:
                # given a crf model as model_obj
                self.name = model_obj.reference_name
                self.report_datetime = model_obj.related_visit.report_datetime
                self.schedule_name = model_obj.related_visit.schedule_name
                self.site = model_obj.related_visit.site
                self.subject_identifier = model_obj.related_visit.subject_identifier
                self.timepoint = model_obj.related_visit.timepoint
                self.visit_code = model_obj.related_visit.visit_code
                self.visit_code_sequence = model_obj.related_visit.visit_code_sequence
                self.visit_schedule_name = model_obj.related_visit.visit_schedule_name
            except AttributeError as e:
                if "related_visit" not in str(e):
                    raise
                # given a visit model as model_obj
                self.name = model_obj.reference_name
                self.report_datetime = model_obj.report_datetime
                self.schedule_name = model_obj.schedule_name
                self.site = model_obj.site
                self.subject_identifier = model_obj.subject_identifier
                self.timepoint = model_obj.timepoint
                self.visit_code = model_obj.visit_code
                self.visit_code_sequence = model_obj.visit_code_sequence
                self.visit_schedule_name = model_obj.visit_schedule_name
        elif related_visit:
            self.name = name
            self.report_datetime = related_visit.report_datetime
            self.schedule_name = related_visit.schedule_name
            self.site = related_visit.site
            self.subject_identifier = related_visit.subject_identifier
            self.timepoint = related_visit.timepoint
            self.visit_code = related_visit.visit_code
            self.visit_code_sequence = related_visit.visit_code_sequence
            self.visit_schedule_name = related_visit.visit_schedule_name
        else:
            # given only the attrs
            self.name = name
            self.report_datetime = report_datetime
            self.schedule_name = schedule_name
            self.site = site
            self.subject_identifier = subject_identifier
            self.timepoint = timepoint
            self.visit_code = visit_code
            self.visit_code_sequence = visit_code_sequence
            self.visit_schedule_name = visit_schedule_name
        reference_model = site_reference_configs.get_reference_model(name=self.name)
        self.reference_model_cls = django_apps.get_model(reference_model)

        # note: updater needs to "update_value"
        self.value = getattr(self.object, "value")
        self.has_value = True
        setattr(self, self.field_name, self.value)

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}({self.name}.{self.field_name}',"
            f"'{self.subject_identifier},{self.report_datetime}"
            f") value={self.value}, has_value={self.has_value}>"
        )

    @property
    def object(self):
        """Returns a reference model instance."""
        if not self._object:
            self.created = False
            opts = self.required_options
            opts.update(**{k: v for k, v in self.visit_options.items() if v is not None})
            if {k: v for k, v in opts.items() if v is None}:
                raise ReferenceGetterError(
                    "Unable to get a reference instance. Null values for attrs "
                    f"not allowed. {self}. Got {opts}."
                )
            try:
                self._object = self.reference_model_cls.objects.get(**opts)
            except ObjectDoesNotExist as e:
                if self.create:
                    self._object = self.create_reference_obj()
                    self.created = True
                else:
                    raise ReferenceObjectDoesNotExist(f"{e}. Using {opts}")
        return self._object

    @property
    def required_options(self):
        """Returns a dictionary of query options required for both
        get and create.
        """
        opts = dict(
            identifier=self.subject_identifier,
            model=self.name,
            report_datetime=self.report_datetime,
            field_name=self.field_name,
            site=self.site,
        )
        return opts

    @property
    def visit_options(self):
        """Returns a dictionary of query options of the visit attrs."""
        opts = dict(
            visit_schedule_name=self.visit_schedule_name,
            schedule_name=self.schedule_name,
            visit_code=self.visit_code,
            visit_code_sequence=self.visit_code_sequence,
            timepoint=self.timepoint,
            site=self.site,
        )
        return opts

    def create_reference_obj(self):
        """Returns a newly create reference instance.

        Note: updater needs to "update_value".
        """
        opts = self.required_options
        opts.update(**{k: v for k, v in self.visit_options.items() if v is not None})
        if {k: v for k, v in opts.items() if v is None}:
            raise ReferenceGetterError(
                "Unable to create a reference instance. Null values for attrs "
                f"not allowed. {self}. Got {opts}."
            )
        return self.reference_model_cls.objects.create(**opts)
