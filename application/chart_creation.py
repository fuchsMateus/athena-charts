# chart_creation.py

from tkinter import messagebox
from dashboard_generator import DashboardGenerator

def populate_chart_options(dataframe, x_column_menu, y_column_menu, value_column_menu,
                           color_column_menu, size_column_menu, names_column_menu, values_column_menu):
    columns = list(dataframe.columns)
    x_column_menu["values"] = columns
    y_column_menu["values"] = columns
    value_column_menu["values"] = columns
    color_column_menu["values"] = columns
    size_column_menu["values"] = columns
    names_column_menu["values"] = columns
    values_column_menu["values"] = columns

def create_chart(query_result_df, x_column_menu, y_column_menu, value_column_menu,
                 chart_title_entry, color_style_menu, chart_type_menu, color_column_menu,
                 size_column_menu, names_column_menu, values_column_menu):
    if query_result_df is None:
        messagebox.showerror("Error", "Run a query before creating the chart.")
        return

    chart_title = chart_title_entry.get()
    chart_type = chart_type_menu.get()
    dashboard = DashboardGenerator(query_result_df)

    if chart_type == "Heatmap":
        x_col = x_column_menu.get()
        y_col = y_column_menu.get()
        value_col = value_column_menu.get()
        color_style = color_style_menu.get()

        if not (x_col and y_col and value_col):
            messagebox.showerror("Error", "Please select columns X, Y and Value.")
            return

        dashboard.create_heatmap(x_col=x_col, y_col=y_col, value_col=value_col, style=color_style, name=chart_title)

    elif chart_type == "Line Chart":
        x_col = x_column_menu.get()
        y_col = y_column_menu.get()

        if not (x_col and y_col):
            messagebox.showerror("Error", "Please select columns X and Y.")
            return

        dashboard.create_line_chart(x_col=x_col, y_col=y_col, name=chart_title)

    elif chart_type == "Bar Chart":
        x_col = x_column_menu.get()
        y_col = y_column_menu.get()

        if not (x_col and y_col):
            messagebox.showerror("Error", "Please select columns X and Y.")
            return

        dashboard.create_bar_chart(x_col=x_col, y_col=y_col, name=chart_title)

    elif chart_type == "Scatter Plot":
        x_col = x_column_menu.get()
        y_col = y_column_menu.get()
        color_col = color_column_menu.get() or None
        size_col = size_column_menu.get() or None

        if not (x_col and y_col):
            messagebox.showerror("Error", "Please select columns X and Y.")
            return

        dashboard.create_scatter_plot(x_col=x_col, y_col=y_col, color_col=color_col, size_col=size_col, name=chart_title)

    elif chart_type == "Pie Chart":
        names_col = names_column_menu.get()
        values_col = values_column_menu.get()

        if not (names_col and values_col):
            messagebox.showerror("Error", "Please select columns X and Y.")
            return

        dashboard.create_pie_chart(names_col=names_col, values_col=values_col, name=chart_title)

    elif chart_type == "Histogram":
        x_col = x_column_menu.get()

        if not x_col:
            messagebox.showerror("Error", "Please select columns X and Y.")
            return

        dashboard.create_histogram(x_col=x_col, name=chart_title)

    elif chart_type == "Box Plot":
        x_col = x_column_menu.get()
        y_col = y_column_menu.get()

        if not (x_col and y_col):
            messagebox.showerror("Error", "Please select columns X and Y.")
            return

        dashboard.create_box_plot(x_col=x_col, y_col=y_col, name=chart_title)
