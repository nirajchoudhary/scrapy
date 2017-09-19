from django import forms


link_type_choices = [["-1", "All Type"],
                     ["Internal - Relative", "Internal - Relative"],
                     ["Internal - Absolute - HTTP", "Internal - Absolute - HTTP"],
                     ["Internal - Absolute - HTTPS", "Internal - Absolute - HTTPS"],
                     ["External - Absolute - HTTP", "Internal - Absolute - HTTP"],
                     ["External - Absolute - HTTPS", "Internal - Absolute - HTTPS"]]

class URLFilterForm(forms.Form):
    """URL filter form."""
    start_url = forms.CharField(max_length=256)
    link_type = forms.ChoiceField(choices=link_type_choices, required=False)
