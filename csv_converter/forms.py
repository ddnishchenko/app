from django import forms

class CsvConverterForm(forms.Form):
    csv_file = forms.FileField(label='CSV File')

class DifferenceConverterForm(forms.Form):
    file1 = forms.FileField(label='File 1')
    file2 = forms.FileField(label='File 2')