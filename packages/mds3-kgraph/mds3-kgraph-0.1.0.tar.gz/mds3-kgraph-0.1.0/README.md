# MDS3-KGraph

This MDS3-KGraph GUI application provides a user-friendly interface for visualizing and analyzing data related to crystallite structures package developed by the SDLE Research Center at Case Western Reserve University in Cleveland OH. It allows users to explore images, graphs, and features associated with different time points in the data. The application enables users to select features of interest, perform analysis on the selected features, and view experimental data.

## Features

- Image and graph display: View images and graphs associated with each time point in the data.
- Feature selection: Select specific features of interest for further analysis.
- Feature data visualization: Visualize the data for selected features over time.
- Scene graph creation: Generate a scene graph based on the data, representing relationships between nodes.
- Scene graph visualization: View and analyze the scene graph to gain insights into the structure.
- Time range filtering: Filter the data based on a specific time range.
- Auto-play functionality: Automatically advance through the time points in the data.
- Experimental data display: View experimental data alongside the visualizations.

## Requirements

- Python 3.x
- Tkinter
- pandas
- matplotlib
- networkx
- Pillow

## Usage

1. Clone the repository or download the source code.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Prepare the data: Place the CSV file containing the data in the same directory as the application.
4. Launch the GUI application by running `python main.py`.
5. Explore the visualizations, select features, and perform analysis using the provided controls.
6. Use the menu options and buttons to navigate through different functionalities.
7. Adjust the time scale, search for specific time ranges, and use the auto-play feature as desired.

## Folder Structure

- `main.py`: The main application file to run the GUI.
- `data.csv`: The CSV file containing the main data.
- `nodes.csv`: The CSV file containing nodes data for the scene graph.
- `edges.csv`: The CSV file containing edges data for the scene graph.
- `README.md`: The README file providing information about the application.

## Funding Acknowledgements:

## Author

Mingjian Lu

