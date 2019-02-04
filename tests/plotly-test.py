import plotly.plotly as py
import plotly.graph_objs as go

fig = go.Figure(data = [{'x': [1,2], 'y':[1,2]}], layout={})
plot_url = py.plot(fig)
