from django.shortcuts import render
from django.http import FileResponse, HttpResponse
from os import path
import pandas as pd
from .forms import CsvConverterForm, DifferenceConverterForm

# Create your views here.
def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CsvConverterForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            # Get the uploaded CSV file from the form
            csv_file = request.FILES['csv_file']
            
            # Read the CSV file into a DataFrame
            df = pd.read_csv(csv_file, delimiter=';')
            
            # Convert DataFrame to XLSX
            xlsx_buffer = pd.ExcelWriter('converted_file.xlsx', engine='xlsxwriter')
            df.to_excel(xlsx_buffer, index=False)
            xlsx_buffer.close()  # Close the ExcelWriter object
            
            # Serve the XLSX file as a response
            with open('converted_file.xlsx', 'rb') as excel_file:
                response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename="converted_file.xlsx"'
                return response

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CsvConverterForm()
    return render(request, "csv_converter/index.html", {"form": form})

def difference(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = DifferenceConverterForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            # Get the uploaded CSV file from the form
            file1 = request.FILES['file1']
            file2 = request.FILES['file2']
            
            # Read the CSV file into a DataFrame
            df1 = pd.read_csv(file1, delimiter=';')
            df2 = pd.read_csv(file2, delimiter=';')
            
            # Concatenate the DataFrames to combine them
            combined_df = pd.concat([df1, df2])
            # Drop duplicate rows to get the unique rows
            unique_rows = combined_df.drop_duplicates(keep=False)
            
            # Convert DataFrame to XLSX
            xlsx_buffer = pd.ExcelWriter('converted_diff.xlsx', engine='xlsxwriter')
            unique_rows.to_excel(xlsx_buffer, index=False)
            xlsx_buffer.close()  # Close the ExcelWriter object
            
            # Serve the XLSX file as a response
            with open('converted_diff.xlsx', 'rb') as excel_file:
                response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename="converted_diff.xlsx"'
                return response

    # if a GET (or any other method) we'll create a blank form
    else:
        form = DifferenceConverterForm()
    return render(request, "csv_converter/difference.html", {"form": form})
    