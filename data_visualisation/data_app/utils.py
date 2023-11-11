import matplotlib.pyplot as plt
import base64
from io import BytesIO
import seaborn as sns


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_plot(df,a,b):
    sns.set()
    plt.switch_backend('AGG')
    plt.figure(figsize=(7,5))
    plt.title('test')
    sns.lineplot(x= a, y= b, data=df, marker='o',
    color='b', label='Value')
    plt.xticks(rotation=45)
    plt.xlabel(a)
    plt.ylabel(b)
    plt.tight_layout()
    graph = get_graph()
    return graph