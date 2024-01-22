from collections import OrderedDict
import itertools
import sys
import tkinter
import tkinter.messagebox
from tkintermapview import TkinterMapView
from pyswip import Prolog
import pandas as pd
from tkinter import messagebox


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
        results2 = []
        locations = []
        for result in results:
            results2.append(result["City"])
            neighboring_cities = list(prolog.query("tour(\'{}\' ,Y ,Z)".format(result["City"])))
            for cities in neighboring_cities:
                if result["City"] != cities['Z']:
                    locations.append((result["City"], cities['Y'], cities['Z']))
        one_match_locations = []
        print(results2)
        for location in locations:
            if location[2] in results2:
                one_match_locations.append(location)
        print(one_match_locations)

        best_tour = []
        for i in range(len(one_match_locations)):
            best_tour.append("")

        for i in range(len(one_match_locations)):
            string = ""
            for j in range(i , len(one_match_locations)):
                if string == "":
                    if one_match_locations[i][2] == one_match_locations[j][0]:
                        best_tour[i] += one_match_locations[i][0] + " " + one_match_locations[i][1] + " " + one_match_locations[i][2] + " " + one_match_locations[j][1] + " " + one_match_locations[j][2]
                        string = one_match_locations[j][2]
                else:
                    if string == one_match_locations[j][0]:
                        best_tour[i] += one_match_locations[j][1] + " " + one_match_locations[j][2]
                        string = one_match_locations[j][2]
        print(best_tour)
        return locations

    def process_text(self):
        """Extract locations from the text area and mark them on the map."""
        text = self.text_area.get("1.0", "end-1c")  # Get text from text area
        unique_features = self.extract_locations(text)  # Extract locations (you may use a more complex method here)
        query = ""
        for element in unique_features:
            x = element[0]
            y = element[1]
            query += f"{y}(City, \'{x}\'), "
        print(query[:-2])
        if query == '':
            messagebox.showwarning("Warning", "The desired location was not found")
            return
        results = list(prolog.query(query[:-2]))
        for result in results:
            print(result["City"])
        locations = self.check_connections(results)
        if len(locations) == 0:
            messagebox.showwarning("Warning", "The desired location was not found")
        elif len(locations) > 5:
            messagebox.showwarning("Warning", "Enter more detailed information")
        else:
            print(locations)
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
        words = text.lower()
        words = words.split(" ")
        new_sentence = ""
        for word in words:
            new_sentence += f" {word}\n{word}"
        words += new_sentence.split('\n')[1:-1]
        result = []
        for words in words:
            for key, value in unique_features.items():
                if words in value:
                    result.append((words, key.lower()))      
        return result

    def start(self):
        self.mainloop()

df = pd.read_csv('github-classroom/UIAI-4021/fol-skylake/Destinations.csv')
df = df.apply(lambda x: x.str.lower())
for column in df.columns:
    df[column] = df[column].str.replace("'", "\\'")
prolog = Prolog()

prolog.retractall("region(_,_)")
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
    prolog.assertz("my_destination(\'{}')".format(row[1]['Destinations']))
    prolog.assertz("country(\'{}\',\'{}\')".format(row[1]['Destinations'], row[1]['country']))
    prolog.assertz("region(\'{}\',\'{}\')".format(row[1]['Destinations'], row[1]['region']))
    prolog.assertz("climate(\'{}\',\'{}\')".format(row[1]['Destinations'], row[1]['Climate']))
    prolog.assertz("budget(\'{}\',\'{}\')".format(row[1]['Destinations'], row[1]['Budget']))
    prolog.assertz("activity(\'{}\',\'{}\')".format(row[1]['Destinations'], row[1]['Activity']))
    prolog.assertz("demographics(\'{}\',\'{}\')".format(row[1]['Destinations'], row[1]['Demographics']))
    prolog.assertz("duration(\'{}\',\'{}\')".format(row[1]['Destinations'], row[1]['Duration']))
    prolog.assertz("cuisine(\'{}\',\'{}\')".format(row[1]['Destinations'], row[1]['Cuisine']))
    prolog.assertz("history(\'{}\',\'{}\')".format(row[1]['Destinations'], row[1]['History']))
    prolog.assertz("natural_wonder(\'{}\',\'{}\')".format(row[1]['Destinations'], row[1]['Natural Wonder']))
    prolog.assertz("accommodation(\'{}\',\'{}\')".format(row[1]['Destinations'], row[1]['Accommodation']))
    prolog.assertz("language(\'{}\',\'{}\')".format(row[1]['Destinations'], row[1]['Language']))

unique_features = OrderedDict()
for column in df.columns:
    unique_values = df[column].unique()
    unique_values = set(unique_values)
    unique_features[column] = list(unique_values)

df = pd.read_csv('github-classroom/UIAI-4021/fol-skylake/Adjacency_matrix.csv')
prolog.retractall("directly_connected(_,_)")
prolog.retractall("tour(_,_,_)")

for i in range(len(df)):
    for j in range(1, len(df)):
        if df.iloc[i, j] > 0:
            city1, city2 = df.iloc[i, 0], df.iloc[j - 1, 0]
            city1 = city1.replace("'", "\\'")
            city2 = city2.replace("'", "\\'")
            prolog.assertz("directly_connected(\'{}\',\'{}\')".format(city1.lower(), city2.lower()))

# prolog.assertz("connected(X, Y) :- directly_connected(X, Y)")
# prolog.assertz("connected(X, Y) :- directly_connected(Y, X)")
prolog.assertz("tour(X, Y, Z) :- directly_connected(X, Y), directly_connected(Y, Z)")
            

if __name__ == "__main__":
    app = App()
    app.start()
