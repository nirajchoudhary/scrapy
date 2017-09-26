from django import forms


link_type_choices = [["-1", "All Types"],
                     ["Internal - Relative", "Internal - Relative"],
                     ["Internal - Absolute - HTTP", "Internal - Absolute - HTTP"],
                     ["Internal - Absolute - HTTPS", "Internal - Absolute - HTTPS"],
                     ["External - Absolute - HTTP", "Internal - Absolute - HTTP"],
                     ["External - Absolute - HTTPS", "Internal - Absolute - HTTPS"]]

category_choices = [["-1", "All Categories"],
                     ["link href", "link href"],
                     ["anchor href", "anchor href"],
                     ["script src", "script src"],
                     ["image src", "image src"],
                     ["iframe src", "iframe src"],
                     ["unknown", "unknown"]]


class URLFilterForm(forms.Form):
    """URL filter form."""
    start_url = forms.CharField(max_length=256)
    link_type = forms.ChoiceField(choices=link_type_choices, required=False)
    page_URL = forms.CharField(max_length=256, required=False)
    category = forms.ChoiceField(choices=category_choices, required=False)
    link_input = forms.CharField(max_length=256, required=False)
