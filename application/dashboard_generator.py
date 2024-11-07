# dashboard_generator.py

import plotly.express as px

class DashboardGenerator:
    def __init__(self, data):
        self.data = data

    def create_heatmap(self, x_col, y_col, value_col, style="YlOrRd", name="Heatmap"):
        heatmap_data = self.data.pivot(index=y_col, columns=x_col, values=value_col)
        fig = px.imshow(
            heatmap_data,
            labels=dict(x=x_col, y=y_col, color=value_col),
            x=heatmap_data.columns,
            y=heatmap_data.index,
            title=name,
            color_continuous_scale=style
        )
        fig.show()
        return fig

    def create_line_chart(self, x_col, y_col, name="Line Chart"):
        fig = px.line(self.data, x=x_col, y=y_col, title=name)
        fig.show()
        return fig

    def create_bar_chart(self, x_col, y_col, name="Bar Chart"):
        fig = px.bar(self.data, x=x_col, y=y_col, title=name)
        fig.show()
        return fig

    def create_scatter_plot(self, x_col, y_col, color_col=None, size_col=None, name="Scatter Plot"):
        fig = px.scatter(self.data, x=x_col, y=y_col, color=color_col, size=size_col, title=name)
        fig.show()
        return fig

    def create_pie_chart(self, names_col, values_col, name="Pie Chart"):
        fig = px.pie(self.data, names=names_col, values=values_col, title=name)
        fig.show()
        return fig

    def create_histogram(self, x_col, name="Histogram"):
        fig = px.histogram(self.data, x=x_col, title=name)
        fig.show()
        return fig

    def create_box_plot(self, x_col, y_col, name="Box Plot"):
        fig = px.box(self.data, x=x_col, y=y_col, title=name)
        fig.show()
        return fig
