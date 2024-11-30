import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import pandas as pd 

class CsvViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1024x768")
        self.root.title("Open CSV-bestand Viewer")
        
        # Maak de GUI elementen aan
        self.create_widgets()

    def create_widgets(self):
        # Knop om een CSV-bestand te openen
        self.button = tk.Button(self.root, text="Open CSV-bestand", command=self.open_file_explorer)
        self.button.pack(pady=10)

        # Treeview widget om de CSV data weer te geven
        self.treeview = ttk.Treeview(self.root, show="headings")
        self.treeview.pack(pady=10, fill="both", expand=True)

    def open_file_explorer(self):
        # Open de bestandsverkenner om een CSV-bestand te selecteren
        file_path = filedialog.askopenfilename(title="Selecteer een CSV-bestand", 
                                               filetypes=[("CSV-bestanden", "*.csv")])
        
        if file_path:
            # Laad het CSV-bestand in een Pandas DataFrame (gebruik ; als scheidingsteken)
            csv_processor = CsvProcessor(file_path)
            dataframe = csv_processor.load_csv()

            # Toon de data in de Treeview
            table_viewer = TableViewer(self.treeview, dataframe)
            table_viewer.display_data()

class CsvProcessor:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_csv(self):
        # Laad het CSV-bestand in een DataFrame
        print(f"Geselecteerd bestand: {self.file_path}")
        return pd.read_csv(self.file_path, delimiter=";")

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
            self.treeview.heading(col, text=col, anchor="w")  # Kolomtitels links uitgelijnd
            self.treeview.column(col, anchor="w", width=150)  # Celinhoud links uitgelijnd en vaste breedte

        # Voeg de rijen toe aan de Treeview
        for index, row in self.dataframe.iterrows():
            self.treeview.insert("", "end", values=list(row))

        # Pas de kolombreedte handmatig aan (indien gewenst)
        self.adjust_column_width()

    def adjust_column_width(self):
        # Stel een vaste breedte in voor de kolommen
        for col in self.treeview["columns"]:
            self.treeview.column(col, width=200, anchor="w")

if __name__ == "__main__":
    root = tk.Tk()
    app = CsvViewerApp(root)
    root.mainloop()

