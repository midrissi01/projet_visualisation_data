from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import pandas as pd
import io
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import seaborn as sns
import numpy as np
from .utils import get_plot

penguins = sns.load_dataset('penguins')
penguins.head()
def index(request):
    return render("data_app/index.html")
def upload(request):
    if request.method == 'POST':
        # Get the uploaded file from the request
        csv_file = request.FILES['csv_file']

        if csv_file:
            # Read the CSV file using Pandas
            cols=[]
            df = pd.read_csv(csv_file)
            for col in df.columns:
                cols.append(col)
            print(cols)
            context={
                'columns' : cols,
                'csv_file' : csv_file
            }
            return render(request, 'data_app/upload.html', context)
        
        
           

    # Handle GET requests
    return render(request, 'data_app/upload.html')
           
def result(request):
    # Créer une dataframe
    data = {'Date': ['2023-01-01', '2023-01-02', '2023-01-03',
    '2023-01-04', '2023-01-05'],
    'Value': [10, 15, 13, 18, 12]}
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])

    graph = get_plot(df,'Date','Value')

    # Pass the file path to the template
    context = {'graph': graph}

    # Render the template with the plot
    return render(request, 'data_app/result.html', context)



   
