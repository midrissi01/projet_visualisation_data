from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import pandas as pd
import io
import matplotlib.pyplot as plt
import base64
from io import BytesIO
def index(request):
    return render("data_app/index.html")
def page1(request):
    if request.method == 'POST':
        # Get the uploaded file from the request
        csv_file = request.FILES['csv_file']
        
        if csv_file:
            # Read the CSV file using Pandas
            df = pd.read_csv(csv_file)

            # Process the data (e.g., select the specified line and column)
            selected_line = request.POST['selected_line']
            selected_column = request.POST['selected_column']
            data = df.loc[df.index[int(selected_line)], selected_column]

            # Generate a bar plot
            plt.bar(data.index, data)
            plt.xlabel('X-Axis')
            plt.ylabel('Y-Axis')
            plt.title('Bar Plot')

            # Convert the plot to a BytesIO object
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            plt.close()

            # Embed the plot in the HTML response
            plot_data = base64.b64encode(buffer.read()).decode()
            return render(request, 'data_app/page1.html', {'plot_data': plot_data})

    # Handle GET requests
    return render(request, 'data_app/page1.html')
