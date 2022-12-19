from shiny import App, render, ui
import pandas as pd
import matplotlib.pyplot as plt
from settings import get_names

# app_ui = ui.page_fluid(
#     ui.h2("Hello Shiny!"),
#     ui.input_slider("n", "N", 0, 100, 20),
#     ui.output_text_verbatim("txt"),
# )


# def server(input, output, session):
#     @output
#     @render.text
#     def txt():
#         return f"n*2 is {input.n() * 2}"


# app = App(app_ui, server)

data = pd.read_excel("./DACSS Data Collection Project.xlsx", sheet_name= "datasets")

choices = list(data.dataset_title)
# print(choices)
view_settings = ["table", "plot", "describe"]

app_ui = ui.page_fluid(
    ui.h2("Dashboard for datasets"),
    ui.input_select("x1", "Select", choices),
    #ui.input_checkbox_group("x2", "View Settings", view_settings),
    # ui.output_text("rendered_checkbox"),
    # ui.output_table("return_table"),
    # ui.output_table("return_description"),
    # ui.output_plot("return_plot"),
    ui.navset_tab_card(
        ui.nav(
            "Description",
            ui.input_checkbox("desc", "Enable", False),
            ui.panel_conditional(
                "input.desc",
                ui.output_table("return_description")
            )
        ),
        ui.nav(
                    "Plot",
                    ui.input_checkbox("plot", "Enable", True),
                    ui.panel_conditional(
                        "input.plot",
                        ui.output_plot("return_plot")
                    ),
        ),
        ui.nav(
            "Table",
            ui.input_checkbox("table", "Enable", True),
            ui.panel_conditional(
                "input.table",
                ui.output_table("return_table")
            )
        )
    )
)

def server(input, output, session):
    @output
    @render.text
    def rendered_checkbox():
        option = [x for x in input.x2() if x not in ['(', ')'] ]

        if len(option) == 0:
            option = "None"
        else:
            option = ', '.join(option)

        return f"The selected viewing option is {option}"

    def txt(get):
        return f"{get}"
    @output
    @render.text
    def describeTable():
        return f"{input.x2()}"
  
    @output
    @render.table
    def return_table():
        #option = [x for x in input.x2() if x not in ['(', ')'] ]


        # if 'table' in option:
        
        print(get_names().index)

        temp = data[data.dataset_title == input.x1()].copy()

        location = temp.dataset_link.values[0]
        df = pd.read_csv(f'{location}', sep = ',', names= ['lat', 'lon', 'delta', 'year', 'month', 'date'])

        return df.head(20)

    @output
    @render.table
    def return_description():
        # print(data[data.dataset_title == input.x1()].dataset_link)

                  
        temp = data[data.dataset_title == input.x1()].copy()

        location = temp.dataset_link.values[0]
        df = pd.read_csv(f'{location}', sep = ',', names= ['lat', 'lon', 'delta', 'year', 'month', 'date'])

        describeTable = df.describe().reset_index(drop = False, names = "index").copy()

            # print(describeTable)

        return describeTable
    
    @output
    @render.plot
    def return_plot():

        temp = data[data.dataset_title == input.x1()].copy()

        location = temp.dataset_link.values[0]
        df = pd.read_csv(f'{location}', sep = ',', names= ['lat', 'lon', 'delta', 'year', 'month', 'date'])
        df = df.set_index(['lat', 'lon'])

        return df.head(20).plot()

app = App(app_ui, server)