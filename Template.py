from collections import OrderedDict
import sys
import tkinter
import tkinter.messagebox
from tkintermapview import TkinterMapView
from pyswip import Prolog
import pandas as pd


class App(tkinter.Tk):

    APP_NAME = "map_view_demo.py"
    WIDTH = 800
    HEIGHT = 750  # This is now the initial size, not fixed.

    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)

        self.title(self.APP_NAME)
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")

        # Configure the grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)  # Text area and submit button combined row
        self.grid_rowconfigure(1, weight=4)  # Map row

        # Upper part: Text Area and Submit Button
        self.text_area = tkinter.Text(self, height=5)  # Reduced height for text area
        self.text_area.grid(row=0, column=0, pady=(10, 0), padx=10, sticky="nsew")

        self.submit_button = tkinter.Button(self, text="Submit", command=self.process_text)
        self.submit_button.grid(row=0, column=0, pady=(0, 10), padx=10, sticky="se")  # Placed within the same cell as text area

        # Lower part: Map Widget
        self.map_widget = TkinterMapView(self)
        self.map_widget.grid(row=1, column=0, sticky="nsew")

        self.marker_list = []  # Keeping track of markers
        self.marker_path = None


    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)

        self.title(self.APP_NAME)
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")

        # Configure the grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)  # Text area can expand/contract.
        self.grid_rowconfigure(1, weight=0)  # Submit button row; doesn't need to expand.
        self.grid_rowconfigure(2, weight=3)  # Map gets the most space.

        # Upper part: Text Area and Submit Button
        self.text_area = tkinter.Text(self)
        self.text_area.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")
        
        self.submit_button = tkinter.Button(self, text="Submit", command=self.process_text)
        self.submit_button.grid(row=1, column=0, pady=10, sticky="ew")

        # Lower part: Map Widget
        self.map_widget = TkinterMapView(self)
        self.map_widget.grid(row=2, column=0, sticky="nsew")

        self.marker_list = []  # Keeping track of markers

    def check_connections(self, results):
        print('result2 ', results)
        locations = []
        for result in results:
            city  = result["City"]
            locations.append(city)
            # TODO 5: create the knowledgebase of the city and its connected destinations using Adjacency_matrix.csv


        return locations

    def process_text(self):
        """Extract locations from the text area and mark them on the map."""
        text = self.text_area.get("1.0", "end-1c")  # Get text from text area
        locations = self.extract_locations(text)  # Extract locations (you may use a more complex method here)


        # TODO 4: create the query based on the extracted features of user desciption 
        ################################################################################################
        query = "destination(City,_, _, _, low, _, _, _, _, _, _, _, _)"
        results = list(prolog.query(query))
        print(results)
        locations = self.check_connections(results)
        # TODO 6: if the number of destinations is less than 6 mark and connect them 
        ################################################################################################
        print(locations)
        locations = ['mexico_city','rome' ,'brasilia']
        self.mark_locations(locations)

    def mark_locations(self, locations):
        """Mark extracted locations on the map."""
        for address in locations:
            marker = self.map_widget.set_address(address, marker=True)
            if marker:
                self.marker_list.append(marker)
        self.connect_marker()
        self.map_widget.set_zoom(1)  # Adjust as necessary, 1 is usually the most zoomed out


    def connect_marker(self):
        print(self.marker_list)
        position_list = []

        for marker in self.marker_list:
            position_list.append(marker.position)

        if hasattr(self, 'marker_path') and self.marker_path is not None:
            self.map_widget.delete(self.marker_path)

        if len(position_list) > 0:
            self.marker_path = self.map_widget.set_path(position_list)

    def extract_locations(self, text):
        """Extract locations from text. A placeholder for more complex logic."""
        # Placeholder: Assuming each line in the text contains a single location name
        # TODO 3: extract key features from user's description of destinations
        ################################################################################################

        return [line.strip() for line in text.split('\n') if line.strip()]

    def start(self):
        self.mainloop()

df = pd.read_csv('github-classroom/UIAI-4021/fol-skylake/Destinations.csv')

prolog = Prolog()

prolog.retractall("language(_,_)")
prolog.retractall("accommodation(_,_)")
prolog.retractall("natural_wonder(_,_)") 
prolog.retractall("history(_,_)")
prolog.retractall("duration(_,_)")
prolog.retractall("cuisine(_,_)")
prolog.retractall("demographics(_,_)")
prolog.retractall("activity(_,_)")
prolog.retractall("budget(_,_)")
prolog.retractall("climate(_,_)")
prolog.retractall("region(_,_)")
prolog.retractall("country(_,_)")
prolog.retractall("my_destination(_)")

for row in df.iterrows():
    prolog.assertz("my_destination(\"{}\")".format(row[1]['Destinations']))
    prolog.assertz("country(\"{}\",\"{}\")".format(row[1]['country'], row[1]['Destinations']))
    prolog.assertz("region(\"{}\",\"{}\")".format(row[1]['region'], row[1]['Destinations']))
    prolog.assertz("climate(\"{}\",\"{}\")".format(row[1]['Climate'], row[1]['Destinations']))
    prolog.assertz("budget(\"{}\",\"{}\")".format(row[1]['Budget'], row[1]['Destinations']))
    prolog.assertz("activity(\"{}\",\"{}\")".format(row[1]['Activity'], row[1]['Destinations']))
    prolog.assertz("demographics(\"{}\",\"{}\")".format(row[1]['Demographics'], row[1]['Destinations']))
    prolog.assertz("duration(\"{}\",\"{}\")".format(row[1]['Duration'], row[1]['Destinations']))
    prolog.assertz("cuisine(\"{}\",\"{}\")".format(row[1]['Cuisine'], row[1]['Destinations']))
    prolog.assertz("history(\"{}\",\"{}\")".format(row[1]['History'], row[1]['Destinations']))
    prolog.assertz("natural_wonder(\"{}\",\"{}\")".format(row[1]['Natural Wonder'], row[1]['Destinations']))
    prolog.assertz("accommodation(\"{}\",\"{}\")".format(row[1]['Accommodation'], row[1]['Destinations']))
    prolog.assertz("language(\"{}\",\"{}\")".format(row[1]['Language'], row[1]['Destinations']))

unique_features = OrderedDict()
for column in df.columns:
    unique_values = df[column].unique()
    unique_values = set(unique_values)
    unique_features[column] = list(unique_values)


if __name__ == "__main__":
    app = App()
    app.start()
