from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import pandas as pd
import io
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import seaborn as sns
import numpy as np
#from .utils import get_plot
from .utils import get_barplot
import pickle
 # Créer une dataframe
    # data = {'Date': ['2023-01-01', '2023-01-02', '2023-01-03',
    # '2023-01-04', '2023-01-05'],
    # 'Value': [10, 15, 13, 18, 12]}
    # df = pd.DataFrame(data)
    # df['Date'] = pd.to_datetime(df['Date'])

    # graph = get_plot(df,'Date','Value')


def index(request):
    return render(request,"data_app/index.html")


def upload(request):
   
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
        return render(request, 'data_app/upload.html', context)
      
    
    # Handle GET requests
    return render(request, 'data_app/upload.html')
           
def traiter(request):
    df = request.session.get('df')
    df = pd.read_csv(io.StringIO(df))
    
    if request.method == 'POST':
        col1= str(request.POST['select1'])
        col2= str(request.POST['select2'])
        #graph = get_lineplot(df, col1, col2)
        graph = get_barplot( col1, col2, df)

    context={
        'graph':graph
        }
    return render(request, 'data_app/upload.html',context)



   
