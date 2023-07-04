# README
## Master Thesis:
## Creation of a process for scientific visualization development based on the example of the new ZHAW protein source database
### Christina Köck
### FH Kufstein, Tirol, Austria
### July 2023

This GitHub repository contains the code and resources for the Streamlit app developed as part of my Master's thesis titled "Creation of a process for scientific visualization development based on the example of the new ZHAW protein source database". The app is designed to show the interactive functions of the designed visualizations for the database. The data used are a small part from the draft of the [DaPRO database](https://www.zhaw.ch/en/research/research-database/project-detailview/projektid/5789/) and stored in the repo as .xlsx - files.

### Content
 - Data and images for the streamlit app are in the folder "Code".
 - The streamlit.py and all pages are in the subfolder "Streamlit".
 - Jupyter Notebooks with the different stages of the visualization development can be found in the folder "Code" as well. These files are named **PageX_NameofSection_IterationY** and contain loading of data, data preprocessing, and several versions and drafts of visualizations. Most data needed to be stored as .xlsx - files since the database is connected to different sources via ontologies. The corresponding owl-files are not contained in the repo and therefore the data cannot and should not be directely read from the database draft.



### Usage of the Streamlit app
 - Clone the repository to your local machine (with code, data and images).
 - Enter the following command from the main folder (MA) on the command line: `streamlit run "Code\Streamlit\app.py"`.
 - The app will open in the web browser if there are no conflicts with the firewall.
 - If there are conflicts with different package versions, please open the folder in a virtual environment and reinstall the packages according to [requirements](https://github.com/TinyTen/MA/blob/main/Code/requirements.txt).

 Alternatively, the app can be run via following [link](https://tinyten-ma-codestreamlitapp-lpn1aq.streamlit.app/).


  Use Cases/separate pages:

 - Page0_Overview: Display of missing values and a scatte plot of all data points.
 - Page1_SearchForIngredients: Single food items can be compared in a matrix or a bar plot.
 - Page2_EvaluateRecipe: A recipe can be created. The composition of the recipe in regard to the chosen parameters is shown as a bar plot. The amino acid composition is shown as a rose chart.
 - Page3_StudyResults: Study results of new protein sources (e.g., insects) can be compared in a bar plot. 

 The app is self-explanatory. Food items and parameters can be chosen for each use case. Visualizations with the chosen variables are shown.

### Data Sources
The ZHAW protein source database serves as the main data source for the app. The database contains comprehensive information on protein-rich foods, including nutritional data, sustainability measures, and processing details.


### Acknowledgments
I would like to express my gratitude to the ZHAW project team for their collaboration and the possibility to use the data.
