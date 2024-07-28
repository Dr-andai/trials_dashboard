from utils import setup_logging
from views.fetch_db import fetch_publications, fetch_journals, get_author_dict

from shiny import App, Inputs, Outputs, Session, render, ui
from shinywidgets import output_widget, render_widget

import pandas as pd
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import tempfile

# Fetch initial data
authors_data = get_author_dict()
author_ids = list(authors_data.keys())
author_names = list(authors_data.values())

# Fetch data
publications_df = fetch_publications(authors = author_ids)
journals_df = fetch_journals(authors = author_ids)

# Shiny app
app_ui = ui.page_fluid(
    ui.h2("Author Citations Plot"),
    ui.layout_column_wrap(
        ui.card(
            ui.layout_sidebar(
                ui.sidebar(
                    ui.h2("Clinical Citations Plot"),
                    ui.input_slider("Year","Select Year", min = 2000, max=2023, value=[2015,2023]),
                    ui.input_select("author_select", "Select Authors", choices=author_names, multiple=True)
                ),
                ui.tags.div(
                    ui.output_plot("citation_plot", width="100%", height='500px'),
                )
            ),
        ),
        ui.card(
            # Add more content or another card here if needed
            ui.tags.div(
                ui.output_plot("journal_plot", width="100%", height='500px'),
                    class_="output-plot"
                )
        ),
    )
)

# Define the server logic
def server(input, output, session):
    @output
    @render.image
    def citation_plot():
        selected_authors = input.author_select()
        selected_year = input.Year()
        if not selected_authors:
            return None

        selected_df = publications_df[
            
            (publications_df['author'].isin(selected_authors))&
            (publications_df['year'] >= selected_year[0])&
            (publications_df['year'] <= selected_year[1])
             
            ]
        
        publication_counts = selected_df.groupby(['author', 'year']).size().reset_index(name = 'count')
        
        plt.figure(figsize=(10, 6))
        for author in selected_authors:
            author_df = publication_counts[publication_counts['author'] == author]
            plt.plot(author_df['year'], author_df['count'], marker='o', label=author)

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
    
    @output
    @render.image
    def journal_plot():
        selected_authors = input.author_select()
        selected_year = input.Year()
        if not selected_authors:
            return None

        selected_df = journals_df[
            
            (journals_df['author'].isin(selected_authors))&
            (journals_df['year'] >= selected_year[0])&
            (journals_df['year'] <= selected_year[1])
             
            ]
        
        # journal_counts = selected_df.groupby(['author', 'year','citation']).size().reset_index(name = 'count')
        
        plt.figure(figsize=(12, 8))
        for author in selected_authors:
            author_df = selected_df[selected_df['author'] == author]
            for year in range(selected_year[0], selected_year[1]+1):
                year_df = author_df[author_df['year'] == year]
                if not year_df.empty:
                    journals = ', '.join(year_df['citation'].dropna().unique())
                    plt.barh(f"{author} ({year})", len(year_df), label=journals)

        plt.xlabel("Number of Publications")
        plt.ylabel("Authors and Year")
        plt.title("Journals per Author per Year")
        plt.legend(title="Journals", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()

        # Save plot to a temporary file
        tmpfile = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        plt.savefig(tmpfile.name)
        plt.close()
        #####

        return {"src": tmpfile.name, "width": "100%", "height": "auto"}
        

# Create and run the Shiny app
app = App(app_ui, server)

if __name__ == "__main__":
    app.run()