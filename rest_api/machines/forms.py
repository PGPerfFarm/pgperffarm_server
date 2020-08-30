from django.db.models import Count
from django import forms

from runs.models import RunInfo
from machines.models import Machine


class MachineForm(forms.Form):

	alias = forms.CharField()
	description = forms.CharField()

	class Meta:
		model = Machine


class EditMachineForm(forms.Form):

	description = forms.CharField()

	class Meta:
		model = Machine
		

