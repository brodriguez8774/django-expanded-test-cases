"""
Forms for django-expanded-test-cases project UnitTests.
"""

# Third-Party Imports.
from django import forms
from django.forms import formset_factory


class BasicForm(forms.Form):
    """A base form with trivial fields, to test basic pack logic when handling forms."""

    required_charfield = forms.CharField(label='CharField - Required', required=True, max_length=100)
    optional_charfield = forms.CharField(label='CharField - Optional', required=False, max_length=100)
    required_intfield = forms.IntegerField(label='IntField - Required', required=True)
    optional_intfield = forms.IntegerField(label='IntField - Optional', required=False)

    def clean(self):
        """Some extra cleaning logic, to ensure we can test various cases."""

        # Get IntField values. Optional defaults to 0 if not provided.
        cleaned_data = super().clean()

        try:
            required_intfield = cleaned_data.get('required_intfield')
            optional_intfield = cleaned_data.get('optional_intfield')
            if optional_intfield is None:
                optional_intfield = 0

            # Raise error on individual fields, if either is negative.
            if required_intfield < 0:
                self.add_error('required_intfield', 'Cannot set "IntField - Required" to a negative value.')
            if optional_intfield < 0:
                self.add_error('optional_intfield', 'Cannot set "IntField - Optional" to a negative value.')

            # Raise general form error if both fields sum to above 100.
            if required_intfield + optional_intfield > 100:
                self.add_error(None, 'Invalid values. IntFields cannot add up to above 100.')
        except:
            pass

        return cleaned_data


# Create a formset from above BasicForm class.
BasicFormset = formset_factory(
    BasicForm,
    extra=2,
    min_num=2,
    max_num=2,
)
