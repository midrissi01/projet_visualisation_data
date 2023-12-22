from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import pandas as pd
import io
import matplotlib.pyplot as plt
import base64
from io import BytesIO, StringIO
import seaborn as sns
import numpy as np
from . import utils
import pickle
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.base import ContentFile
import os
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponse
import pandas as pd  # Note the corrected import statement
from .forms import BinomialForm
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO, BytesIO
import base64
from .forms import ExponentielleForm,TraitementForm
import json
import plotly.express as px
import matplotlib
import plotly.graph_objs as go
from scipy.stats import binom
from django.http import JsonResponse
import plotly.io as pio
from .forms import BernoulliForm 
from scipy.stats import bernoulli
matplotlib.use('Agg')
from statistics import mean, median, mode, variance, stdev
from .forms import NormaleForm 
from .forms import PoissonForm 
from .forms import UniformeForm

from . import forms
from scipy.stats import bernoulli,binom

def index(request):
    return render(request,"data_app/index.html")

def laws(request):
    return render(request,"data_app/laws.html")

def dataframe(request):
    return render(request,"data_app/dataFrameTable.html")

def dataframe_upload(request):
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
        

        df_html = df.to_html(classes='table')
        cols = list(df.columns)
        print(cols)
        request.session['cols'] = cols

        context = {
            'df': df_html,
            'cols': cols
        }
        return render(request, 'data_app/dataFrameTable.html', context)
    return render(request,"data_app/dataFrameTable.html")

def dataframe_search1(request):
    df = None
    columns_choices = None

    if 'df' in request.session:
        df = request.session['df']
        df = pd.read_csv(io.StringIO(df))
        columns_choices = request.session['cols']
        
        
    if request.method == 'POST':
        parcourir_chart_type = request.POST.get('parcourir_chart')
        col_name1 = request.POST.get('col_name1')
        row_numb = request.POST.get('RowNumb')
        

        if parcourir_chart_type == 'FindElem' and df is not None:
            # Logique pour rechercher l'élément
            try:
                row_numb = int(row_numb)
                max_row = df.shape[0] - 1  # La taille maximale du DataFrame
                row_numb = min(row_numb, max_row)  # Assurez-vous que row_numb ne dépasse pas la taille du DataFrame
                resultats_recherche = df.at[row_numb, col_name1]
                contexte = {'resultat': resultats_recherche, 'cols': columns_choices, 'df': df.to_html(classes='table table-bordered'), 'max_row': max_row}
                return render(request, 'data_app/dataFrameTable.html', contexte)
            except (ValueError, KeyError, IndexError):
                pass

        # Nouvelle logique pour le parcours spécifique
        parcourir_rows_type = request.POST.get('parcourir_rows')

        if parcourir_rows_type == 'NbrOfRowsTop':
            nb_rows_top = int(request.POST.get('Head'))
            df = df.head(nb_rows_top)
        elif parcourir_rows_type == 'NbrOfRowsBottom':
            nb_rows_bottom = int(request.POST.get('Tail'))
            df = df.tail(nb_rows_bottom)
        elif parcourir_rows_type == 'FromRowToRow':
            from_row = int(request.POST.get('FromRowNumb'))
            to_row = int(request.POST.get('ToRowNumb'))
            df = df.loc[from_row:to_row]

        # Récupération des colonnes sélectionnées
        selected_columns = request.POST.getlist('selected_columns')
        if selected_columns:
            df = df[selected_columns]

    # Si la méthode n'est pas POST, ou si aucune recherche n'est effectuée, affichez simplement la page avec le DataFrame actuel
    contexte = {'df': df.to_html(classes='table table-bordered') if df is not None else None, 'cols': columns_choices}
    return render(request, 'data_app/dataFrameTable.html', contexte)

def dataframe_search(request):
    df = request.session.get('df')
    df = pd.read_csv(io.StringIO(df))
    df_html = df.to_html(classes='table')

    if request.method == 'get':
        methode = request.get['methode']
        line1 = request.get['line1']
        line2 = request.get['line2']

        if methode == "Slicing":

            if line1 and line2:
                sliced_df = df.loc[line1 : line2]
            elif line1:
                sliced_df = df.loc[line1:]
            elif line2:
                sliced_df = df.loc[:line2]
            else:
                # Aucun choix, afficher le DataFrame entier
                sliced_df = df

            df_html = sliced_df.to_html(classes='table table-striped', index=False)

            context={
            'df': df_html,
            }
            return render(request,"data_app/dataFrameTable.html", context)
    context={
        'df': df_html,
        }
    return render(request,"data_app/dataFrameTable.html", context)

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
            'df' : df_csv,
            'columns': cols,
            'csv_file': csv_file,
        }
        return render(request, 'data_app/barplot.html', context)
      
    # Handle GET requests
    return render(request, 'data_app/barplot.html')
    
def barplot_result(request):
    df = request.session.get('df')
    df = pd.read_csv(io.StringIO(df))
    cols = list(df.columns)
    
    if request.method == 'POST':
        col1= str(request.POST['select1'])
        col2= str(request.POST['select2'])
       
        graph = utils.get_interactive_barplot(df,col1, col2)

    context={
        'graph':graph,
        'columns' : cols
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
    cols = list(df.columns)
    
    if request.method == 'POST':
        col1= str(request.POST['select1'])
        col2= str(request.POST['select2'])
        graph = utils.get_interactive_lineplot(df, col1, col2)

    context={
        'graph':graph,
        'columns':cols
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
    cols = list(df.columns)
    
    if request.method == 'POST':
        col1= str(request.POST['select1'])
        col2= str(request.POST['select2'])
        graph = utils.get_interactive_scatterplot(df, col1, col2, color=None, size=None)
        #graph = utils.get_scatterplot(col1, col2, df)

    context={
        'graph':graph,
        'columns': cols
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
    cols = list(df.columns)

    if request.method == 'POST':
        col1 = str(request.POST['select1'])
       
        graph = utils.get_piechart(df, col1)  

    context = {
        'graph': graph,
        'columns': cols
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
    cols = list(df.columns)

    if request.method == 'POST':
        col1 = str(request.POST['select1'])
       
        graph = utils.get_boxplot(df, col1)  

    context = {
        'graph': graph,
        'columns':cols
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
    cols = list(df.columns)

    if request.method == 'POST':
        col1 = str(request.POST['select1'])
       
        # Generate the interactive HTML code for the histogram
        graph = utils.get_histogram(df, col1)

    context = {
        'graph': graph,
        'columns': cols
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
    cols = list(df.columns)

    if request.method == 'POST':
        col1 = str(request.POST['select1'])
       
        # Generate the interactive HTML code for the KDE plot
        graph = utils.get_kdeplot(df, col1)

    context = {
        'graph': graph,
        'columns': cols 
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
    cols = list(df.columns)

    if request.method == 'POST':
        col1 = str(request.POST['select1'])
       
        # Générer le code HTML interactif pour le Violin Plot
        graph = utils.get_violinplot(df, col1)

    context = {
        'graph': graph,
        'columns' : cols
    }
    return render(request, 'data_app/violinplot.html', context)


#//////////////////////////////// LOIS ////////////////////////////////////////////////////////////////
def Binomiale(request):
    if request.method == 'POST':
        form = forms.BinomialForm(request.POST)
        if form.is_valid():
            n = form.cleaned_data['n']
            p = form.cleaned_data['p']

            # Générer des échantillons de la distribution binomiale
            data_binomial = binom.rvs(n=n, p=p, loc=0, size=1000)

            # Créer un histogramme interactif avec Plotly Express
            fig = px.histogram(x=data_binomial, nbins=n+1, title='Distribution Binomiale')
            fig.update_layout(xaxis_title='Binomial', yaxis_title='Fréquence relative',bargap=0.2)

            # Convertir la figure en JSON
            plot_data = fig.to_html()

            return render(request, 'data_app/binomiale.html', {'form': form, 'plot_data': plot_data})
    else:
        form = forms.BinomialForm()

    return render(request, 'data_app/binomiale.html', {'form': form})


def Bernoulli(request):
    if request.method == 'POST':
        form = BernoulliForm(request.POST)
        if form.is_valid():
            p = form.cleaned_data['p']
            # Générer des échantillons de la distribution de Bernoulli
            data_bernoulli = bernoulli.rvs(p, size=1000)
            # Créer un histogramme interactif avec Plotly Express
            fig = px.histogram(x=data_bernoulli, nbins=2, title='Distribution de Bernoulli')
            fig.update_layout(xaxis_title='Bernoulli', yaxis_title='Fréquence relative',bargap=0.2)
            # Convertir la figure en JSON
            plot_data = fig.to_html()

            return render(request, 'data_app/bernoulli.html', {'form': form, 'plot_data': plot_data})
    else:
        form = BernoulliForm()

    return render(request, 'data_app/bernoulli.html', {'form': form})

#///////////////////////////


def Normale(request):
    if request.method == 'POST':
        form = NormaleForm(request.POST)
        if form.is_valid():
            mean = form.cleaned_data['mean']
            std_dev = form.cleaned_data['std_dev']

            # Générer des échantillons de la distribution normale
            data_normale = np.random.normal(mean, std_dev, size=1000)

            # Créer un histogramme interactif avec Plotly Express
            fig = px.histogram(x=data_normale, title='Distribution Normale Continue')
            fig.update_layout(xaxis_title='Valeur', yaxis_title='Fréquence relative',bargap=0.2)

            # Convertir la figure en JSON
            plot_data = fig.to_html()

            return render(request, 'data_app/normale.html', {'form': form, 'plot_data': plot_data})
    else:
        form = NormaleForm()

    return render(request, 'data_app/normale.html', {'form': form})



def Poisson(request):
    if request.method == 'POST':
        form = PoissonForm(request.POST)
        if form.is_valid():
            lambda_param = form.cleaned_data['lambda_param']

            # Générer des échantillons de la distribution de Poisson
            data_poisson = np.random.poisson(lambda_param, size=1000)

            # Créer un histogramme interactif avec Plotly Express
            fig = px.histogram(x=data_poisson, title='Distribution de Poisson')
            fig.update_layout(xaxis_title='Valeur', yaxis_title='Fréquence relative',bargap=0.2)

            # Convertir la figure en JSON
            plot_data = fig.to_html()

            return render(request, 'data_app/poisson.html', {'form': form, 'plot_data': plot_data})
    else:
        form = PoissonForm()

    return render(request, 'data_app/poisson.html', {'form': form})



def Uniforme(request):
    if request.method == 'POST':
        form = UniformeForm(request.POST)
        if form.is_valid():
            a = form.cleaned_data['a']
            b = form.cleaned_data['b']

            # Générer des échantillons de la distribution uniforme
            data_uniforme = np.random.uniform(a, b, size=1000)

            # Créer un histogramme interactif avec Plotly Express
            fig = px.histogram(x=data_uniforme, title='Distribution Uniforme')
            fig.update_layout(xaxis_title='Valeur', yaxis_title='Fréquence relative',bargap=0.2)

            # Convertir la figure en JSON
            plot_data = fig.to_html()

            return render(request, 'data_app/uniforme.html', {'form': form, 'plot_data': plot_data})
    else:
        form = UniformeForm()

    return render(request, 'data_app/uniforme.html', {'form': form})



def Exponentielle(request):
    if request.method == 'POST':
        form = ExponentielleForm(request.POST)
        if form.is_valid():
            beta = form.cleaned_data['beta']

            # Générer des échantillons de la distribution exponentielle
            data_exponentielle = np.random.exponential(scale=beta, size=1000)

            # Créer un histogramme interactif avec Plotly Express
            fig = px.histogram(x=data_exponentielle, title='Distribution Exponentielle')
            fig.update_layout(xaxis_title='Valeur', yaxis_title='Fréquence relative',bargap=0.2)

            # Convertir la figure en JSON
            plot_data = fig.to_html()

            return render(request, 'data_app/exponentielle.html', {'form': form, 'plot_data': plot_data})
    else:
        form = ExponentielleForm()

    return render(request, 'data_app/exponentielle.html', {'form': form})


def mode(valeurs):
    uniques, counts = np.unique(valeurs, return_counts=True)
    max_count = np.max(counts)
    modes = uniques[counts == max_count]
    if max_count == 1:
        return "Il n'y a pas de mode"
    else:
        return modes.tolist()

def Calcules(request):
    if request.method == 'POST':
        form = TraitementForm(request.POST)
        if form.is_valid():
            valeurs_input = form.cleaned_data['valeurs']
            
            # Traiter les valeurs saisies
            valeurs = [float(x.strip()) for x in valeurs_input.replace('-', ',').split(',') if x.strip()]
            
            # Calcul des statistiques
            mean_value = np.mean(valeurs)
            median_value = np.median(valeurs)
            mode_value = mode(valeurs)
            variance_value = np.var(valeurs)
            stdev_value = np.std(valeurs)

            return render(request, 'calcules.html', {'form': form, 'mean': mean_value,
                                                     'median': median_value, 'mode': mode_value,
                                                     'variance': variance_value, 'stdev': stdev_value})
    else:
        form = TraitementForm()

    return render(request, 'calcules.html', {'form': form})

