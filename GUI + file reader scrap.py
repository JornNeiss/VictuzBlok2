import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import pandas as pd


class CsvViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1024x768")
        self.root.title("Open CSV-bestand Viewer")

        # Maak een frame voor elke pagina
        self.home_frame = tk.Frame(self.root)
        self.csv_frame = tk.Frame(self.root)

        # Plaats de frames in het hoofdvenster
        self.home_frame.grid(row = 0, column = 0, sticky = "nsew")
        self.csv_frame.grid(row = 0, column = 0, sticky = "nsew")

        # Maak de GUI elementen voor beide pagina's aan
        self.create_home_widgets()
        self.create_csv_widgets()

    def create_home_widgets(self):
        # Knop voor naar de CSV pagina te gaan
        self.button_open_csv = tk.Button(self.home_frame, text = "Open CSV-bestand", command = self.show_csv_page)
        self.button_open_csv.pack(pady = 10)

    def create_csv_widgets(self):
        # Knop voor terug naar het home menu te gaan
        self.button_home = tk.Button(self.csv_frame, text = "Terug naar Home", command = self.show_home_page)
        self.button_home.pack(pady = 10)

        # Knop om een CSV-bestand te openen
        self.button_open_file = tk.Button(self.csv_frame, text = "Open CSV-bestand", command = self.open_file_explorer)
        self.button_open_file.pack(pady = 10)

        # Treeview widget om de CSV data weer te geven
        self.treeview = ttk.Treeview(self.csv_frame, show = "headings")
        self.treeview.pack(pady = 10, fill = "both", expand = True)

    def open_file_explorer(self):
        # Open de bestandsverkenner om een CSV-bestand te selecteren
        file_path = filedialog.askopenfilename(title = "Selecteer een CSV-bestand",
                                               filetypes = [("CSV-bestanden", "*.csv")])

        if file_path:
            # Laad het CSV-bestand in een Pandas DataFrame
            csv_processor = CsvProcessor(file_path)
            dataframe = csv_processor.load_csv()

            # Toon de data in de Treeview
            table_viewer = TableViewer(self.treeview, dataframe)
            table_viewer.display_data()

    def show_csv_page(self):
        self.home_frame.grid_forget()  # Verberg de homepagina
        self.csv_frame.grid(row = 0, column = 0, sticky = "nsew")  # Toon de CSV pagina

    def show_home_page(self):
        self.csv_frame.grid_forget()  # Verberg de CSV pagina
        self.home_frame.grid(row = 0, column = 0, sticky = "nsew")  # Toon de homepagina


class CsvProcessor:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_csv(self):
        # Laad het CSV-bestand in een DataFrame
        print(f"Geselecteerd bestand: {self.file_path}")
        return pd.read_csv(self.file_path, delimiter = ";")


class TableViewer:
    def __init__(self, treeview, dataframe):
        self.treeview = treeview
        self.dataframe = dataframe

    def display_data(self):
        # Verwijder oude data in de Treeview
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        # Voeg kolomnamen toe
        self.treeview["columns"] = list(self.dataframe.columns)

        # Maak de kolommen in de Treeview en pas breedte en uitlijning aan
        for col in self.dataframe.columns:
            self.treeview.heading(col, text = col, anchor = "w")  # Kolomtitels links uitgelijnd
            self.treeview.column(col, anchor = "w", width = 150)  # Celinhoud links uitgelijnd en vaste breedte

        # Voeg de rijen toe aan de Treeview
        for index, row in self.dataframe.iterrows():
            self.treeview.insert("", "end", values = list(row))

        # Pas de kolombreedte handmatig aan (indien gewenst)
        self.adjust_column_width()

    def adjust_column_width(self):
        # Stel een vaste breedte in voor de kolommen
        for col in self.treeview["columns"]:
            self.treeview.column(col, width = 200, anchor = "w")


if __name__ == "__main__":
    root = tk.Tk()
    app = CsvViewerApp(root)
    root.mainloop()
