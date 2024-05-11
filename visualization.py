from DotsOnScreen import DrawDots

from rich.console import Console
from rich.table import Table

import plotly.express as px
import pandas as pd

import json

class VisualizationTool():
    def __init__(self) -> None:
        self.jsonfile = 'data/values.json'
        self.click_coords = 'data/clicking_coords.csv'

        self.data = self.extract_data() #reextracting

    # Data extraction and some preprocessing
    def extract_data(self) -> pd.DataFrame:
        data = pd.read_csv(self.click_coords)
        # Returns the color for each button type
        def assign_color(button: str) -> str:
            button_color_mapping ={
                'Button.left': 'blue',
                'Button.right': 'red',
                'Button.middle': 'green'}
            
            return button_color_mapping.get(str(button), 'black')
            
        data['color'] = data['button'].apply(assign_color)

        data['days'] = data['time'].apply(lambda x: x[:10])
        data['hours'] = data['time'].apply(lambda x: x[10:][:3])

        return data
    
    # Load values.json
    def load_file(self) -> dict:
        with open(self.jsonfile, 'r') as jsonFile:
            data = json.load(jsonFile)
        return data

    # Shows on the screen where the mouse click was made
    def area_of_clicking(self) -> None:
        drawing_tool = DrawDots(self.data)
        drawing_tool.draw_dots()

    # Shows the number of mouse clicks
    def stats_of_mouse(self) -> None:
        df = self.data.groupby('button').count().reset_index()
        df = df.rename(columns={'color':'num_clicks'}).sort_values('num_clicks', ascending=False)

        table = Table(title="\n[b]Your Mouse Clicks Stats[/b]\n")

        self.print_table_stats(table, df)

    # Shows the number of keystrokes
    def stats_of_keyboard(self) -> None:
        df = pd.DataFrame(self.load_file().items(), columns=['button', 'num_clicks'])
        df = df.assign(num_clicks=df.num_clicks.astype(int)).sort_values('num_clicks', ascending=False) # I convert it to 'int' to sort

        table = Table(title="\n[b]Your Keyboard Clicks Stats[/b]\n")

        self.print_table_stats(table, df)

    # Print tables with information
    def print_table_stats(self, table: Table, df: pd.DataFrame) -> None:
        console = Console()
        table.add_column("#", style="cyan")
        table.add_column("Button", style='green')
        table.add_column("Number of Clicks", style='magenta')

        for i, row in enumerate(df.itertuples(), start=1):
            table.add_row(str(i), row.button, str(row.num_clicks))

        console.print(table)

    # Shows all-time clicks per day data
    def clicks_per_day(self) -> None:
        count_per_day = self.data.groupby(['days','button']).size().unstack(fill_value=0)
        count_per_day = count_per_day.reset_index()

        melted_df = pd.melt(count_per_day, id_vars='days', value_vars=count_per_day.columns[1:], var_name='button', value_name='count')

        fig = px.bar(melted_df, x='days', y='count', color='button', text='count')
        fig.show()

    # Shows all-time clicks per hour data
    def clicks_per_hour(self) -> None:
        count_per_hour = self.data.groupby(['hours','button']).size().unstack(fill_value=0)
        count_per_hour = count_per_hour.reset_index()

        melted_df = pd.melt(count_per_hour, id_vars='hours', value_vars=count_per_hour.columns[1:], var_name='button', value_name='count')

        fig = px.bar(melted_df, x='hours', y='count', color='button', text='count')
        fig.show()

    # Shows the top 50 keystrokes as a bar
    def show_top_50_keys(self) -> None:
        df = pd.DataFrame(self.load_file().items(), columns=['button', 'num_clicks']).sort_values(by='num_clicks', ascending=False)
        df = df.assign(num_clicks=df.num_clicks.astype(int)).sort_values('num_clicks', ascending=False)[:50] # Top 50
        
        fig = px.bar(df, x='button',y='num_clicks')
        fig.show()