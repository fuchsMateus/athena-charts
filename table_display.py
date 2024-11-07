# table_display.py

from tkinter import ttk

def display_table(dataframe, table_frame, max_rows=1000):
    # Remove o conteúdo anterior da tabela
    for widget in table_frame.winfo_children():
        widget.destroy()

    # Exibir o cabeçalho
    columns = list(dataframe.columns)
    table = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)
    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=100, anchor="center")

    # Preencher com os dados da query, limitado a max_rows
    for index, row in dataframe.iterrows():
        if index >= max_rows:
            break
        table.insert("", "end", values=list(row))

    table.pack(fill="both", expand=True)