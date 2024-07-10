import pandas as pd
from shiny import App, Inputs, Outputs, Session, render, ui
from shinywidgets import output_widget, render_widget
import plotly.graph_objs as go
from utils import setup_logging


# from views.fetch_db import fetch_journals, get_author_dict

# app_ui = ui.page_fluid(
#     ui.input_select("select_country","select",choices= fetch_journals,selected=None),
#     ui.output_text("value"),
#     output_widget("plot")
# )

# def server(input: Inputs, output: Outputs, session: Session):
#     return
# app =App(app_ui, server)

# import shiny
# from shiny import App, ui, render
from views.fetch_db import fetch_publications, get_author_dict
import matplotlib.pyplot as plt
import tempfile

# Fetch initial data
authors_data = get_author_dict()
author_ids = list(authors_data.keys())
author_names = list(authors_data.values())

# Fetch publications data
publications_df = fetch_publications(authors=author_ids)

# Define the Shiny app
app_ui = ui.page_fluid(
    ui.h2("Author Citations Plot"),
    ui.input_select("author_select", "Select Authors", choices=author_names, multiple=True),
    ui.output_plot("citation_plot")
)

# Define the server logic
def server(input, output, session):
    @output
    @render.image
    def citation_plot():
        selected_authors = input.author_select()
        if not selected_authors:
            return None

        selected_df = publications_df[publications_df['author'].isin(selected_authors)]
        
        plt.figure(figsize=(10, 6))
        for author in selected_authors:
            author_df = selected_df[selected_df['author'] == author]
            citations = author_df['citations'].sum()
            plt.bar(author, citations, label=author)

        plt.xlabel("Authors")
        plt.ylabel("Total Citations")
        plt.title("Number of Citations per Author")
        plt.legend()
        plt.tight_layout()

        # Save plot to a temporary file
        tmpfile = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        plt.savefig(tmpfile.name)
        plt.close()

        return {"src": tmpfile.name, "width": "100%", "height": "auto"}

# Create and run the Shiny app
app = App(app_ui, server)

if __name__ == "__main__":
    app.run()