import plotly.graph_objs as go
import pandas as pd


def Visualize(dictionary):
    indexes = []
    values = []
    indexes.append("Другие")
    values.append(0)
    for e in dictionary:
        if len(dictionary[e]) < 4:
            values[0] += len(dictionary[e])
        else:
            indexes.append(e.company_name)
            values.append(len(dictionary[e]))
    data = pd.Series(values, index=indexes)
    fig = go.Figure()
    fig.add_trace(go.Pie(values=data, labels=data.index, hole=0.7))
    fig.update_layout(annotations=[dict(text='Работодатели<br>матмеха', x=0.5, y=0.5, font_size=40, showarrow=False)])
    fig.show()