from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import pandas as pd
import io
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import seaborn as sns
import numpy as np
from . import utils
import pickle
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.base import ContentFile


 # Créer une dataframe
    # data = {'Date': ['2023-01-01', '2023-01-02', '2023-01-03',
    # '2023-01-04', '2023-01-05'],
    # 'Value': [10, 15, 13, 18, 12]}
    # df = pd.DataFrame(data)
    # df['Date'] = pd.to_datetime(df['Date'])

    # graph = get_plot(df,'Date','Value')


def index(request):
    return render(request,"data_app/index.html")

def barplot_upload(request):
   
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        file_type = csv_file.name.split('.')[-1].lower()  # Get the file extension

        if file_type == 'csv':
            df = pd.read_csv(csv_file)
        elif file_type in ['xls', 'xlsx']:
            # Convert Excel to CSV
            df = pd.read_excel(csv_file)
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            csv_file = ContentFile(csv_buffer.getvalue().encode('utf-8'))  # Encode the CSV data to bytes
            csv_file = SimpleUploadedFile('converted_file.csv', csv_file.read())
        else:
            return HttpResponse("File type not supported. Please upload a CSV or Excel file.")

        # Serialize the DataFrame to CSV as a string
        df_csv = df.to_csv(index=False)
        # Store the CSV string in the session
        request.session['df'] = df_csv
        
        cols = list(df.columns)
        
        context = {
            'columns': cols,
            'csv_file': csv_file,
        }
        return render(request, 'data_app/barplot.html', context)
      
    # Handle GET requests
    return render(request, 'data_app/barplot.html')
    
def barplot_result(request):
    df = request.session.get('df')
    df = pd.read_csv(io.StringIO(df))
    
    if request.method == 'POST':
        col1= str(request.POST['select1'])
        col2= str(request.POST['select2'])
       
        graph = utils.get_interactive_barplot(df,col1, col2)

    context={
        'graph':graph
        }
    return render(request, 'data_app/barplot.html',context)

def lineplot_upload(request):
   
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        print(type(csv_file))
        cols=[]
        
        df = pd.read_csv(csv_file)
        # Serialize the DataFrame to CSV as a string
        df_csv = df.to_csv(index=False)
        # Store the CSV string in the session
        request.session['df'] = df_csv
        
        for col in df.columns:
            cols.append(col)
        print(cols)        
        context={
            'columns' : cols,
            'csv_file' : csv_file,
        }
        return render(request, 'data_app/lineplot.html', context)
    
    # Handle GET requests
    return render(request, 'data_app/lineplot.html')

def lineplot_result(request):
    df = request.session.get('df')
    df = pd.read_csv(io.StringIO(df))
    
    if request.method == 'POST':
        col1= str(request.POST['select1'])
        col2= str(request.POST['select2'])
        #graph = utils.get_lineplot(df, col1, col2)
        graph = utils.get_interactive_lineplot(df, col1, col2)

    context={
        'graph':graph
        }
    return render(request, 'data_app/lineplot.html',context)

def scatterplot_upload(request):
   
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        print(type(csv_file))
        cols=[]
        
        df = pd.read_csv(csv_file)
        # Serialize the DataFrame to CSV as a string
        df_csv = df.to_csv(index=False)
        # Store the CSV string in the session
        request.session['df'] = df_csv
        
        for col in df.columns:
            cols.append(col)
        print(cols)        
        context={
            'columns' : cols,
            'csv_file' : csv_file,
        }
        return render(request, 'data_app/scatterplot.html', context)
    
    # Handle GET requests
    return render(request, 'data_app/scatterplot.html')

def scatterplot_result(request):
    df = request.session.get('df')
    df = pd.read_csv(io.StringIO(df))
    
    if request.method == 'POST':
        col1= str(request.POST['select1'])
        col2= str(request.POST['select2'])
        graph = utils.get_interactive_scatterplot(df, col1, col2, color=None, size=None)
        #graph = utils.get_scatterplot(col1, col2, df)

    context={
        'graph':graph
        }
    return render(request, 'data_app/scatterplot.html',context)

   
