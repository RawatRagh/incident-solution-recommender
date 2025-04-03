from django import forms

# This class will create an input control of file type which can accept multiple excel files and on selection trigger a checkfile  JS function
# this will be imported in views.py train view to be rendered in train.html file
"""
class trainingForm(forms.Form):
    excel_path = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True,
                                                                        'accept':".xlsx , .xls",
                                                                        'onchange':"checkfile(this)"}))
"""


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True
    
    def __init__(self,attrs=None):
        super().__init__(attrs)
        self.attrs['accept'] = '.xls,.xlsx'
        self.attrs['onchange'] = 'checkfile(this)'

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class trainingForm(forms.Form):
    excel_path = MultipleFileField()
