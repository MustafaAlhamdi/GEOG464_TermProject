# GEOG464_TermProject

Canadian Census Data Visualization Library
------------------------------------------

The Canadian Census Data Visualization Library is a Python library consisting of two files: `utils.py` and `vizLib.py`. It provides a set of functions for visualizing Canadian Census data in various formats, including choropleth maps and interactive maps. More function parameters and return variables information can be found in the function definitions in the library.

### Functions in `utils.py`

#### `load_dataframes`

Loads the Canadian Census data into two GeoDataFrames: one for population data and one for language data. Takes as input the file paths for the population and language data CSV files.


`def load_dataframes(population_data_path: str, language_data_path: str) -> Tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]:`

#### `merge_dataframes`

Merges the population and language GeoDataFrames on their common column `DAUID`, which is a unique identifier for each region in Canada.


`def merge_dataframes(population_df: gpd.GeoDataFrame, language_df: gpd.GeoDataFrame) -> gpd.GeoDataFrame:`

#### `calculate_language_ratios`

Calculates the ratios of population language knowledge based on specified columns in a dictionary.


`def calculate_language_ratios(dataframe: pd.DataFrame, columns_dict: dict) -> pd.DataFrame:`

#### `get_highest_education_ratio`

Computes the ratio of the total population in age 24 to 65 with a provided level of education to the total population in age 24 to 65 for each DAUID, and returns the DAUID and the education level that has the highest ratio.


`def get_highest_education_ratio(df: pd.DataFrame, population_col: str, education_level_col: str) -> Tuple[float, str, str]:`

### Functions in `vizLib.py`

#### `generate_population_choropleth`

Generates a 2x2 grid of choropleth subplots of selected columns from a GeoDataFrame of population data.


`def generate_population_choropleth(merged_population: gpd.GeoDataFrame, columns: Dict[str, Any]) -> plt.Figure:`

#### `plot_language_choropleth`

Creates a 2x2 grid of subplots of chloropleth maps of language data.


`def plot_language_choropleth(merged_languages: gpd.GeoDataFrame, columns: Dict[str, Any]) -> plt.Figure:`

#### `plot_mother_tongue_ratio`

Plots a choropleth map of the ratio of population with official and non-official languages as mother tongue.


`def plot_mother_tongue_ratio(merged_languages: gpd.GeoDataFrame, columns: Dict[str, Any]) -> tuple:`

#### `generate_population_map`

Creates an interactive population map of Canada using the Folium library.


`def generate_population_map(merged_population: gpd.GeoDataFrame) -> folium.Map:`

#### `create_education_levels_map`

Creates an interactive leaflet map that shows the ratio of total_no_certificate, total_secondary, and total_post_secondary to the total population for each DAUID in the input geodataframe.


`def create_education_levels_map(gdf: gpd.GeoDataFrame, no_certificate_col: str, secondary_col: str, postsecondary_col: str, population_col: str) -> folium.folium.Map:`

#### `plot_birth_density_map`

Plots an interactive density map of count of births in different regions for each DAUID with separate layers for each birth place.


`def plot_birth_density_map(gdf: gpd.GeoDataFrame) -> folium.Map:`

### Download files from Dropbox

Kindly note that I had to clear the outputs of the functions in `project.ipynb` and that I was unable to upload the required files for the project to this repository due to the size limit. Please download the full TermProject folder (and not each file individually) from [Dropbox](https://www.dropbox.com/scl/fo/ii7teuyk2x2fxw66h793a/h?dl=0&rlkey=lf6xv5173p0zdmqzux4y9t1ek) to successfully run the functions.

Please make sure to rename the file names according to your necessity.
