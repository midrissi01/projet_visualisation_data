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
        return render(request, 'data_app/lineplot.html', context)

    # Handle GET requests
    return render(request, 'data_app/lineplot.html')

def lineplot_result(request):
    df = request.session.get('df')
    df = pd.read_csv(io.StringIO(df))
    
    if request.method == 'POST':
        col1= str(request.POST['select1'])
        col2= str(request.POST['select2'])
        graph = utils.get_interactive_lineplot(df, col1, col2)

    context={
        'graph':graph
        }
    return render(request, 'data_app/lineplot.html',context)

def scatterplot_upload(request):
   
    if  request.method == 'POST':
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



def piechart_upload(request):
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
            'columns': df.columns.tolist(),
            'csv_file': csv_file,
            'data_frame': df,
        }
        return render(request, 'data_app/piechart.html', context)

    # Handle GET requests
    return render(request, 'data_app/piechart.html')


def piechart_result(request):
    df = request.session.get('df')
    df = pd.read_csv(io.StringIO(df))


    if request.method == 'POST':
        col1 = str(request.POST['select1'])
       
        graph = utils.get_piechart(df, col1)  

    context = {
        'graph': graph,
    }
    return render(request, 'data_app/piechart.html', context)
###################################################################

def boxplot_upload(request):
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
            'columns': df.columns.tolist(),
            'csv_file': csv_file,
            'data_frame': df,
        }
        return render(request, 'data_app/boxplot.html', context)

    # Handle GET requests
    return render(request, 'data_app/boxplot.html')


def boxplot_result(request):
    df = request.session.get('df')
    df = pd.read_csv(io.StringIO(df))


    if request.method == 'POST':
        col1 = str(request.POST['select1'])
       
        graph = utils.get_boxplot(df, col1)  

    context = {
        'graph': graph,
    }
    return render(request, 'data_app/boxplot.html', context)

def histogram_upload(request):
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
            'columns': df.columns.tolist(),
            'csv_file': csv_file,
            'data_frame': df,
        }
        return render(request, 'data_app/histogram.html', context)

    # Handle GET requests
    return render(request, 'data_app/histogram.html')


def histogram_result(request):
    df_csv = request.session.get('df')
    df = pd.read_csv(io.StringIO(df_csv))

    if request.method == 'POST':
        col1 = str(request.POST['select1'])
       
        # Generate the interactive HTML code for the histogram
        graph = utils.get_histogram(df, col1)

    context = {
        'graph': graph,
    }
    return render(request, 'data_app/histogram.html', context)

def kdeplot_upload(request):
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
            'columns': df.columns.tolist(),
            'csv_file': csv_file,
            'data_frame': df,
        }
        return render(request, 'data_app/kdeplot.html', context)

    # Handle GET requests
    return render(request, 'data_app/kdeplot.html')

def kdeplot_result(request):
    df_csv = request.session.get('df')
    df = pd.read_csv(io.StringIO(df_csv))

    if request.method == 'POST':
        col1 = str(request.POST['select1'])
       
        # Generate the interactive HTML code for the KDE plot
        graph = utils.get_kdeplot(df, col1)

    context = {
        'graph': graph,
    }
    return render(request, 'data_app/kdeplot.html', context)

def heatmap_upload(request):
    if request.method == 'POST':
        try:
            csv_file = request.FILES['csv_file']
            file_type = csv_file.name.split('.')[-1].lower()  # Get the file extension

            if file_type == 'csv':
                # Lire le fichier CSV sans spécifier les dates pour voir les colonnes disponibles
                df = pd.read_csv(csv_file)
                # Assurez-vous que 'nom_de_la_colonne_date' est dans les colonnes du DataFrame
                if 'nom_de_la_colonne_date' in df.columns:
                    # Spécifiez la colonne de dates lors de la lecture du fichier CSV
                    df = pd.read_csv(csv_file, parse_dates=['nom_de_la_colonne_date'])
            elif file_type in ['xls', 'xlsx']:
                # Convertir Excel en CSV
                df = pd.read_excel(csv_file)
                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False)
                csv_file = ContentFile(csv_buffer.getvalue().encode('utf-8'))
                csv_file = SimpleUploadedFile('converted_file.csv', csv_file.read())
            else:
                return HttpResponse("File type not supported. Please upload a CSV or Excel file.")

            # Générer le code HTML interactif pour le Heatmap
            
            graph = utils.get_heatmap(df)

            context = {
                'graph': graph,
            }
            return render(request, 'data_app/heatmap.html', context)

        except Exception as e:
            print(f"Error in heatmap_upload: {e}")
            return HttpResponse(f"An error occurred: {e}")

    return render(request, 'data_app/heatmap.html')

def violinplot_upload(request):
   
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
        return render(request, 'data_app/violinplot.html', context)
      
    # Handle GET requests
    return render(request, 'data_app/violinplot.html')

def violinplot_result(request):
    df_csv = request.session.get('df')
    df = pd.read_csv(io.StringIO(df_csv))

    if request.method == 'POST':
        col1 = str(request.POST['select1'])
       
        # Générer le code HTML interactif pour le Violin Plot
        graph = utils.get_violinplot(df, col1)

    context = {
        'graph': graph,
    }
    return render(request, 'data_app/violinplot.html', context)


