import matplotlib.pyplot as plt
import plotly.express as px
import base64
from io import BytesIO
import seaborn as sns


# def get_graph():
#     buffer = BytesIO()
#     plt.savefig(buffer, format='png')
#     buffer.seek(0)
#     image_png = buffer.getvalue()
#     graph = base64.b64encode(image_png)
#     graph = graph.decode('utf-8')
#     buffer.close()
#     return graph


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_interactive_lineplot(df, a, b):
    fig = px.line(df, x=a, y=b, markers=True)
    fig.update_layout(
        title='Interactive Line Plot',
        xaxis_title=a,
        yaxis_title=b,
        xaxis=dict(tickangle=45),
    )
    
    graph = fig.to_html(full_html=False)
    return graph

def get_interactive_barplot(df, a, b):
    fig = px.bar(df, x=a, y=b)
    fig.update_layout(
        title='Interactive Bar Plot',
        xaxis_title=a,
        yaxis_title=b
    )
    
    graph = fig.to_html(full_html=False)
    return graph

def get_interactive_scatterplot(df, x, y, color=None, size=None):
    fig = px.scatter(df, x=x, y=y, color=color, size=size)
    fig.update_layout(
        title='Interactive Scatter Plot',
        xaxis_title=x,
        yaxis_title=y
    )
    
    graph = fig.to_html(full_html=False)
    return graph

###############################################

def get_lineplot(df,a,b):
    sns.set()
    plt.switch_backend('AGG')
    plt.figure(figsize=(7,5))
    plt.title('test')
    sns.lineplot(x= a, y= b, data=df, marker='o',
    color='b')
    plt.xticks(rotation=45)
    plt.xlabel(a)
    plt.ylabel(b)
    plt.tight_layout()
    graph = get_graph()
    return graph

def get_barplot(x, y, data):
    sns.set()
    plt.switch_backend('AGG')
    plt.figure(figsize=(5,3))
    plt.title('test')
    sns.barplot(x=x , y=y, data=data)
    plt.xticks(rotation=45)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.tight_layout()
    graph = get_graph()
    return graph

def get_scatterplot(x,y,data):
    sns.set()
    plt.switch_backend('AGG')
    plt.figure(figsize=(5,3))
    plt.title('test')
    sns.scatterplot(x=x, y=y, data=data)
    plt.xticks(rotation=45)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.tight_layout()
    graph = get_graph()
    return graph



