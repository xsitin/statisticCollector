import plotly.graph_objs as go
import pandas as pd


def Visualize(dictionary,group_name):
    companies = []
    for e in dictionary:
        companies.append([-len(dictionary[e]), e.company_name])
    companies.sort()
    indexes = []
    values = []
    take_first = min(30, len(companies))
    for i in range(take_first):
        indexes.append(companies[i][1])
        values.append(-companies[i][0])
    other_count = 0
    for i in range(take_first, len(companies)):
        other_count += -companies[i][0]
    indexes.append("Другие")
    values.append(other_count)
    data = pd.Series(values, index=indexes)
    fig = go.Figure()
    fig.add_trace(go.Pie(values=data, labels=data.index, hole=0.7))
    fig.update_layout(annotations=[dict(text='Работодатели<br>'+group_name, x=0.5, y=0.5, font_size=40, showarrow=False)])
    fig.show()