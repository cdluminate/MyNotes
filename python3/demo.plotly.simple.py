import plotly
import random

data = [random.random() for _ in range(10)]

plotly.offline.plot({
    'data': [plotly.graph_objs.Bar(y=data)],
    }, image='svg')
