from django import forms
from fetch_api.models import Story


class SprintForm(forms.Form):
    # Specific stories to include
    specific_stories = forms.MultipleChoiceField(
        required=False,
        choices=[(story.nodeID, story.name) for story in Story.nodes.all()],
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-control',
            }
        )
    )

    # Complexity per sprint
    sprint_complexity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Complexity per sprint?'
            }
        )
    )

    # Minimum number of sprints
    min_sprints = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Minimum number of sprints to plan?'
            }
        )
    )

    # Max dependencies to schedule per sprint
    max_dependants_per_story = forms.IntegerField(
        required=False,
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': '(Optional) Max number of dependants per sprint'
            }
        )
    )
