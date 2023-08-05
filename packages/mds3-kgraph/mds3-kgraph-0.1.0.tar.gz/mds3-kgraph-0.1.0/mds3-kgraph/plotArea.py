import tkinter as tk
from PIL import Image, ImageTk
import pandas as pd
import os
import numpy as np
from io import BytesIO
import networkx as nx
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



class App:
    """An application for visualizing and analyzing crystallite AFM data.

        This application provides a graphical user interface (GUI) for visualizing and analyzing data related to
        crystallite structures. It allows users to view images, graphs, and features associated with different time points
        in the data. Users can explore the data, select features of interest, and perform analysis on the selected features.

        Attributes:
            master (tk.Tk): The root Tkinter window.
            csv_file (str): The path to the CSV file containing the data.
            nodes_file (str): The path to the CSV file containing the nodes data.
            edges_file (str): The path to the CSV file containing the edges data.
            df (pd.DataFrame): The DataFrame representing the main data.
            nodes_df (pd.DataFrame): The DataFrame representing the nodes data.
            edges_df (pd.DataFrame): The DataFrame representing the edges data.
            current_time (int): The current time point in the data.
            current_row (int): The index of the current row in the data.
            time_range (tuple): The range of time values to filter the data.
            selected_features (list): The list of selected features.
            feature_checkbuttons (dict): A dictionary mapping feature paths to their corresponding checkbuttons.
            table (ttk.Treeview): The table for displaying feature data.
            large_crystallite_figure (Figure): The figure for displaying the large crystallite graph.
            large_crystallite_canvas (FigureCanvasTkAgg): The canvas for displaying the large crystallite graph.
            pause (bool): A flag indicating whether the auto-play functionality is paused.
            exp_frame (tk.Frame): The frame for displaying experimental data.

        """

    def __init__(self, master, csv_file,nodes_file, edges_file):
        self.master = master
        self.csv_file = csv_file
        self.df = pd.read_csv(csv_file)
        self.nodes_df = pd.read_csv(nodes_file)
        self.edges_df = pd.read_csv(edges_file)
        self.current_time = 0
        self.current_row = 0
        self.time_range=0
        self.selected_features = []
        self.feature_checkbuttons = {}
        self.table = None

        self.large_crystallite_figure = None
        self.large_crystallite_canvas = None
        self.crystallite_close_figure = None
        self.crystallite_close_canvas = None
        self.pause = False  # 新增pause属性
        self.exp_frame = tk.Frame(self.master)

        self.create_widgets()
        self.create_scene_graph()

    def update_scene_graph(self):
        """Update and redraw the scene graph based on the current time."""
        G = self.create_scene_graph(area_threshold=0.03)
        self.draw_scene_graph(G, self.large_crystallite_figure, "Large Crystallite Graph")
        self.large_crystallite_canvas.draw()

    def create_scene_graph(self, area_threshold=0.03):
        """Create a scene graph based on the data from CSV files.

        Args:
            area_threshold (float): Minimum area threshold for nodes to be included in the graph.

        Returns:
            nx.Graph: The created scene graph.

        """
        G = nx.Graph()

        filtered_nodes = self.nodes_df[
            (self.nodes_df['area'] > area_threshold) & (self.nodes_df['time'] == self.current_time)].drop_duplicates(
            subset='id')
        current_edges = self.edges_df[self.edges_df['time'] == self.current_time]

        for index, row in filtered_nodes.iterrows():
            G.add_node(row['id'], area=row['area'])
            print(self.nodes_df['id'].is_unique)

        for index, row in current_edges.iterrows():
            if row['source'] in G.nodes() and row['target'] in G.nodes():
                G.add_edge(row['source'], row['target'], weight=row['nnd_val'], label=row['label'])

        return G

    def draw_scene_graph(self, G, figure, title):
        """Visualize the graph using matplotlib and update the figure in the GUI.

        Args:
            G (nx.Graph): The graph to visualize.
            figure (matplotlib.figure.Figure): The figure to update.
            title (str): The title of the graph.

        """
        figure.clf()
        pos = nx.circular_layout(sorted(G.nodes()))
        ax = figure.add_subplot(111)
        ax.set_title(title)

        colors = plt.cm.rainbow(np.linspace(0, 1, len(G.nodes())))
        nx.draw(G, pos, node_size=[G.nodes[node]['area']*5000 for node in G], node_color=colors, ax=ax)
        nx.draw_networkx_labels(G, pos, labels={node: node for node in G.nodes()}, font_size=8, ax=ax)

        edge_labels = {(u, v): d['label'] for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, ax=ax)

    def create_widgets(self):
        """Create all the GUI widgets for the application."""

        # Set window size
        self.master.geometry("2000x2000")

        # Create image label
        self.image_label = tk.Label(self.master)
        self.image_label.place(x=10, y=10)

        # Create graph label
        self.graph_label = tk.Label(self.master)
        self.graph_label.place(x=320, y=10)

        # Create feature label
        self.feature_frame = tk.Frame(self.master)
        self.feature_frame.place(x=320, y=360)

        time_search_frame = tk.Frame(self.master)
        time_search_frame.place(x=320, y=320)


        time_label = tk.Label(time_search_frame, text="Time:")
        time_label.pack(side="left")

        self.time_entry = tk.Entry(time_search_frame)
        self.time_entry.pack(side="left")

        time_search_button = tk.Button(time_search_frame, text="Search", command=self.search_time)
        time_search_button.pack(side="left")
        self.analysis_button = tk.Button(time_search_frame, text="Analysis", command=self.perform_analysis)
        self.analysis_button.pack(side="left", padx=2)

        # Create time scale and progress bar
        time_frame = tk.Frame(self.master)
        time_frame.place(x=10, y=320)

        self.progressbar = ttk.Progressbar(time_frame, orient="horizontal", length=50, mode="determinate")
        self.progressbar.pack(side="left", padx=10)

        self.time_scale = tk.Scale(time_frame, from_=0, to=len(self.df) - 1, orient="horizontal", length=200,
                                   command=self.scale_update,showvalue=False)
        self.time_scale.pack(side="left")

        # Create play/stop buttons
        buttons_frame = tk.Frame(self.master)
        buttons_frame.place(x=5, y=360)

        prev_time_button = tk.Button(buttons_frame, text="Prev", command=self.prev_time)
        prev_time_button.pack(side="left")



        play_button = tk.Button(buttons_frame, text="Play", command=self.auto_play)
        self.play_button = play_button
        play_button.pack(side="left", padx=2)

        stop_button = tk.Button(buttons_frame, text="Stop", command=self.pause_play)
        self.stop_button = stop_button
        stop_button.pack(side="left")

        next_time_button = tk.Button(buttons_frame, text="Next", command=self.next_time)
        next_time_button.pack(side="left", padx=2)

        self.data_display_frame = tk.Frame(self.master)
        self.data_display_frame.place(x=10, y=300)



        self.data_display_featureinfo = tk.Frame(self.master)
        self.data_display_featureinfo.place(x=310, y=420)
        #back_button = tk.Button(self.data_display_featureinfo, text="Back", command=self.display_feature_selection)
        #back_button.pack(side="bottom", pady=10)

        if not self.table:
            self.columns = list(self.df.columns)
            self.columns.remove('feature')
            self.table = ttk.Treeview(self.data_display_featureinfo, columns=self.columns, show='headings')
            for col in self.columns:
                self.table.column(col, width=40, minwidth=10, anchor='center')
                self.table.heading(col, text=col, anchor='center')

        # Create data label
        self.data_label = tk.Label(self.data_display_frame, text="")
        self.data_label.pack()

        # Display initial data
        self.display_data()
        self.display_images()


        self.exp_frame = tk.Frame(self.master)
        self.exp_frame.place(x=10, y=400)

        # Create scene graph figures and canvases

    # Create scene graph figures and canvases
        self.large_crystallite_figure = Figure(figsize=(3, 3), dpi=100)
        self.large_crystallite_canvas = FigureCanvasTkAgg(self.large_crystallite_figure, master=self.master)
        self.large_crystallite_canvas.get_tk_widget().place(x=920, y=10)


        G = self.create_scene_graph()
        self.draw_scene_graph(G, self.large_crystallite_figure, "Scene Graph")
        self.large_crystallite_canvas.draw()

        # Add a Combobox for selecting graph type
        self.graph_type = tk.StringVar()
        self.graph_type_combobox = ttk.Combobox(self.master, textvariable=self.graph_type, state="readonly")
        self.graph_type_combobox["values"] = ("Large Objects", "Close Crystallites")
        self.graph_type_combobox.current(0)  # Set default selection to "Large Objects"
        self.graph_type_combobox.bind("<<ComboboxSelected>>", self.on_graph_type_selected)
        self.graph_type_combobox.place(x=910, y=320)

    def on_graph_type_selected(self, event):
        """Handle the event when the user selects a different graph type from the combobox.

        Args:
            event (tk.Event): The event object.

        """
        selected_option = self.graph_type_combobox.get()

        if selected_option == "Large Objects":
            G = self.create_scene_graph(area_threshold=10000)
        elif selected_option == "Close Crystallites":
            G = self.create_close_crystallites_scene_graph(nnd_val_threshold=100)

        self.draw_scene_graph(G, self.large_crystallite_figure, "Scene Graph")
        self.large_crystallite_canvas.draw()

    def create_close_crystallites_scene_graph(self, nnd_val_threshold=1000):
        """Create a graph based on close crystallites with a given threshold for the nearest neighbor distance.

        Args:
            nnd_val_threshold (int): Threshold for the nearest neighbor distance.

        Returns:
            nx.Graph: The created scene graph.

        """
        G = nx.Graph()

        filtered_nodes = self.nodes_df[(self.nodes_df['time'] == self.current_time)].drop_duplicates(subset='id')
        current_edges = self.edges_df[
            (self.edges_df['time'] == self.current_time) & (self.edges_df['nnd_val'] < nnd_val_threshold)]

        for index, row in filtered_nodes.iterrows():
            G.add_node(row['id'], area=row['area'])

        for index, row in current_edges.iterrows():
            if row['source'] in G.nodes() and row['target'] in G.nodes():
                G.add_edge(row['source'], row['target'], weight=row['nnd_val'], label=row['label'])

        return G

    def perform_analysis(self):
        # Clear previous information
        """Clear previous information and display information for selected features."""

        for widget in self.feature_frame.winfo_children():
            widget.destroy()

        self.display_images()
        self.display_data()

        # Display information for selected features
        for feature in self.selected_features:
            feature_data = self.df.loc[self.df['feature'] == feature].to_dict(orient='records')[0]
            feature_label = tk.Label(self.feature_frame, text=f"{feature_data['Id']} - {feature_data['area']}")
            feature_label.pack(side="top", padx=5, pady=5)

        # Refresh the plot
        if hasattr(self, 'canvas_ref'):
            self.canvas_ref.get_tk_widget().destroy()
            del self.canvas_ref

        if self.time_range:
            start_time, end_time = self.time_range
            area_data = self.df.loc[
                (self.df['time'] >= start_time) & (self.df['time'] <= end_time) & (
                    self.df['feature'].isin(self.selected_features)),
                ['Id', 'time', 'area']]
        else:
            area_data = self.df.loc[self.df['feature'].isin(self.selected_features), ['Id', 'time', 'area']]

        fig = plt.figure(figsize=(3, 3), dpi=100)
        fig.subplots_adjust(left=0.2, bottom=0.2, right=0.6, top=0.8)
        ax = fig.add_subplot(1, 1, 1)
        for feature_id, group in area_data.groupby('Id'):
            group.plot(x='time', y='area', ax=ax, label=f'{feature_id}')
        ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1))
        ax.set_title('Crystallite Area vs Time')
        ax.set_xlabel('Time sequence')
        ax.set_ylabel('Normalized crystalline area')
        # Create plot frame and canvas
        plot_frame = tk.Frame(self.master)
        plot_frame.place(x=630, y=10)
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
        self.canvas_ref = canvas


        self.show_feature_data(self.selected_features)

    def auto_play(self):
        """Start automatically playing through the data."""
        if self.pause:  # 修改代码
            return

        self.next_time()
        self.master.after(500, self.auto_play)

    def pause_play(self):
        """Pause or resume the auto-play function."""
        self.pause = True
        self.stop_button.configure(state=tk.DISABLED)
        self.play_button.configure(state=tk.NORMAL)

    def prev_time(self):
        """Move to the previous time in the data."""
        # Find previous time in the data
        previous_time_rows = self.df[self.df['time'] < self.current_time].sort_values(by='time', ascending=False)
        if not previous_time_rows.empty:
            self.current_time = previous_time_rows.iloc[0]['time']
            self.current_row = previous_time_rows.index[-1]
            self.display_images()
            self.display_data()
            self.update_scene_graph()

    def show_feature_data(self, feature):
        """Display the data for a selected feature.

        Args:
            feature (str): The selected feature.

        """
        if feature in self.selected_features:
            self.selected_features.remove(feature)
        else:
            self.selected_features.append(feature)

        self.display_data()
        self.display_images()

    def next_time(self):
        """Find the next time in the data and update the GUI elements."""
        # Find next time in the data
        next_time_rows = self.df[self.df['time'] > self.current_time].sort_values(by='time')
        if not next_time_rows.empty:
            self.current_time = next_time_rows.iloc[0]['time']
            self.current_row = next_time_rows.index[0]
            self.display_images()
            self.display_data()
            self.update_scene_graph()

    def display_images(self):
        """Display the images for the current time and update GUI elements."""
        # Update progressbar and scale value
        self.progressbar['value'] = self.current_row
        self.time_scale.set(self.current_row)

        # Display image
        img_path = self.df.loc[self.current_row, 'img']
        if os.path.exists(img_path):
            img = Image.open(img_path)
            img = img.resize((300, 300))
            img_tk = ImageTk.PhotoImage(img)
            self.image_label.configure(image=img_tk)
            self.image_label.image = img_tk

        # Display graph
        graph_path = self.df.loc[self.current_row, 'graph']
        if os.path.exists(graph_path):
            graph = Image.open(graph_path)
            graph = graph.resize((300, 300))
            graph_tk = ImageTk.PhotoImage(graph)
            self.graph_label.configure(image=graph_tk)
            self.graph_label.image = graph_tk

        # Display feature images
        features = self.df.loc[self.df['time'] == self.current_time, 'feature']

        for widget in self.feature_frame.winfo_children():
            widget.destroy()

        for feature in features:
            if os.path.exists(feature):
                feature_img = Image.open(feature)
                feature_img = feature_img.resize((50, 50))
                feature_img_tk = ImageTk.PhotoImage(feature_img)

                feature_checkbutton = tk.Checkbutton(self.feature_frame, image=feature_img_tk,
                                                     command=lambda f=feature: self.toggle_feature_selection(f))
                feature_checkbutton.image = feature_img_tk
                feature_checkbutton.pack(side="left", padx=5)
                self.feature_checkbuttons[feature] = feature_checkbutton

        # Update canvas with new plot
        if hasattr(self, 'canvas_ref'):
            self.canvas_ref.get_tk_widget().destroy()
            del self.canvas_ref

        if self.time_range:
            start_time, end_time = self.time_range
            area_data = self.df.loc[
                (self.df['time'] >= start_time) & (self.df['time'] <= end_time), ['Id', 'time', 'area']]
        else:
            area_data = self.df.loc[:self.current_row, ['Id', 'time', 'area']]
        fig = plt.figure(figsize=(3, 3), dpi=100)
        fig.subplots_adjust(left=0.2, bottom=0.2, right=0.7, top=0.8)
        ax = fig.add_subplot(1, 1, 1)
        for feature_id, group in area_data.groupby('Id'):
            group.plot(x='time', y='area', ax=ax, label=f'{feature_id}')
        ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1))
        ax.set_title('Crystallite Area vs Time')
        ax.set_xlabel('Time sequence')
        ax.set_ylabel('Normalized crystalline area')
        # Create plot frame and canvas
        plot_frame = tk.Frame(self.master)
        plot_frame.place(x=630, y=10)
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
        self.canvas_ref = canvas

        time_label = tk.Label(self.master, text=f"Current time: {self.current_time}")
        time_label.place(x=725, y=325)



    def toggle_feature_selection(self, feature_path):
        """Toggle the selection of a feature.

        Args:
            feature_path (str): The path of the feature.

        """
        if feature_path in self.selected_features:
            self.selected_features.remove(feature_path)
        else:
            self.selected_features.append(feature_path)

    def show_feature_data(self, selected_features):
        """Display the data for the selected features.

        Args:
            selected_features (list): List of selected features.

        """
        if hasattr(self, 'canvas_ref'):
            self.canvas_ref.get_tk_widget().destroy()
            del self.canvas_ref

        fig = plt.figure(figsize=(3, 3), dpi=100)
        fig.subplots_adjust(left=0.2, bottom=0.2, right=0.9, top=0.9)
        ax = fig.add_subplot(1, 1, 1)

        for feature_path in selected_features:
            feature_id = self.df.loc[self.df['feature'] == feature_path, 'Id'].iloc[0]
            current_time = self.df.loc[self.current_row, 'time']
            area_data = self.df.loc[(self.df['Id'] == feature_id) & (self.df['time'] <= current_time), ['time', 'area']]
            area_data.plot(x='time', y='area', ax=ax, label=f'Id {feature_id}')

        ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1))
        ax.set_title('Crystallite normalize Area vs Time')

        # Create plot frame and canvas
        plot_frame = tk.Frame(self.master)
        plot_frame.place(x=630, y=10)
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
        self.canvas_ref = canvas


    def scale_update(self, value):
        """Update the current row and time based on the scale position.

        Args:
            value (float): The value of the scale.

        """
        self.current_row = int(value)
        self.current_time = self.df.loc[self.current_row, 'time']
        self.display_images()
        self.display_data()
        self.update_scene_graph()

    def prev_feature(self):
        """Find the previous feature in the data and update the GUI elements."""
        # Find previous feature in the data
        previous_feature_rows = self.df[(self.df['time'] == self.current_time) & (self.df.index < self.current_row) & (self.df['feature'] != '')].sort_index(
            ascending=False)
        if not previous_feature_rows.empty:
            self.current_row = previous_feature_rows.index[-1]
            self.display_images()
            self.show_feature_data(self.df.loc[self.current_row, 'feature'])

    def next_feature(self):
        """Find the next feature in the data and update the GUI elements."""
        # Find next feature in the data
        next_feature_rows = self.df[(self.df['time'] == self.current_time) & (self.df.index > self.current_row) & (self.df['feature'] != '')].sort_index()
        if not next_feature_rows.empty:
            self.current_row = next_feature_rows.index[0]
            self.display_images()
            self.show_feature_data(self.df.loc[self.current_row, 'feature'])

    def display_data(self):
        """Display the data for the current time and update GUI elements."""
        # Save current state of application
        if hasattr(self, 'canvas_ref'):
            self.canvas_ref.get_tk_widget().destroy()
            del self.canvas_ref
        self.prev_state = {
            'current_row': self.current_row,
            'current_time': self.current_time,
            'image_path': self.df.loc[self.current_row, 'img'],
            'graph_path': self.df.loc[self.current_row, 'graph']
        }

        # Clear data_display_frame
        for widget in self.data_display_frame.winfo_children():
            widget.destroy()

        # Create the table with headings
        if not hasattr(self, 'table'):
            self.columns = list(self.df.columns)
            self.columns.remove('feature')
            self.table = ttk.Treeview(self.data_display_featureinfo, columns=self.columns, show='headings')
            for col in self.columns:
                self.table.column(col, width=100, minwidth=100, anchor='center')
                self.table.heading(col, text=col, anchor='center')

        # Add rows for the selected features to the table
        self.table.delete(*self.table.get_children())
        for feature in self.selected_features:
            feature_data = self.df.loc[self.df['feature'] == feature].iloc[0]
            row_values = list(feature_data[self.columns])
            self.table.insert('', 'end', values=row_values)

        # Create the back button if it hasn't already been created
        if not hasattr(self, 'back_button'):
            self.back_button = tk.Button(self.data_display_featureinfo, text='Back',
                                         command=self.back_to_feature_selection)

        # Pack the table and back button
        self.table.pack(side='top', pady=10)
        self.back_button.pack(side='bottom', pady=10)

        self.current_row = self.prev_state['current_row']
        self.current_time = self.prev_state['current_time']
        self.display_images()
        exp_data = pd.read_csv('experimental.csv').to_dict('records')[0]
        for col_name, col_value in exp_data.items():
            exp_label = tk.Label(self.exp_frame, text=f"{col_name}: {col_value}")
            exp_label.pack(side="top", padx=0.5, pady=0.01)



    def back_to_feature_selection(self):
        """Clear the table and return to feature selection."""
        # Clear the table and return to feature selection
        self.selected_features = []
        for feature, checkbox in self.feature_checkbuttons.items():
            if checkbox.winfo_exists():  # Add a check for existence of checkbox
                checkbox.deselect()
        self.back_button.pack_forget()
        self.display_data()
    def auto_play(self):
        """Start or stop the auto-play functionality."""
        if self.pause:  # 修改代码
            self.stop_play()  # 新增代码
            return

        self.next_time()
        self.master.after(100, self.auto_play)

    def search_time(self):
        """Search for a specific time range and update the GUI elements."""
        # Get time value from entry
        time_str = self.time_entry.get()

        if '-' in time_str:
            start_time, end_time = map(int, time_str.split('-'))
            self.time_range = (start_time, end_time)

            time_range_rows = self.df[(self.df['time'] >= start_time) & (self.df['time'] <= end_time)]

            # Set current time and row to the end of the time range
            self.current_time = end_time
            self.current_row = time_range_rows.index[-1]
        else:
            self.time_range = None

            try:
                time_value = int(time_str)
            except ValueError:
                print("Invalid time value.")
                return

            # Find nearest time in the data
            time_rows = self.df['time'].sub(time_value).abs().sort_values()
            nearest_time = time_rows.index[0]
            self.current_time = self.df.loc[nearest_time, 'time']
            self.current_row = nearest_time

        self.display_images()
        self.display_data()

    def stop_play(self):  # 新增方法
        """Stop the auto-play functionality and enable the play button."""
        self.pause = True
        self.stop_button.configure(state=tk.DISABLED)
        self.play_button.configure(state=tk.NORMAL)

if __name__ == '__main__':
    csv_file = "all.csv"
    node="updatednode.csv"
    edge="dataframe with timesteps-160.csv"
    root = tk.Tk()
    app = App(root, csv_file,node,edge)
    root.mainloop()

