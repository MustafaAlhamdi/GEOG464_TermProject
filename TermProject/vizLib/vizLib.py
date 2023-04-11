from typing import Optional, Tuple, Any, Dict
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import folium


from typing import Optional
import pandas as pd
import geopandas as gpd



def generate_population_choropleth(merged_population: gpd.GeoDataFrame, columns: Dict[str, Any]) -> plt.Figure:
    """
    Generate a 2x2 grid of choropleth subplots of selected columns from a GeoDataFrame of population data.
    
    Args:
    - merged_population (gpd.GeoDataFrame): GeoDataFrame of merged population data.
    - columns (dict): Dictionary with plot titles to be plotted as keys and column names to be plotted as values.
        Example: {'Average age of the population': 'YlGn', 'Total_percent_pop_65': 'OrRd', 
                  'Total_percent_pop_15_64': 'BuPu', 'age dependency ratio': 'YlOrBr'}
    
    Returns:
    - fig (plt.Figure): The generated matplotlib figure object.
    """
        # create a 2x2 grid of subplots
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10,10))

    # plot age distribution chloropleth in the first subplot
    merged_population.plot(column=columns['Average age of the population'], cmap='YlGn', legend=True, ax=axes[0,0])
    axes[0,0].set_title("Age Distribution")

    # plot potential healthcare needs chloropleth in the second subplot
    merged_population.plot(column=columns['Total_percent_pop_65'], cmap='OrRd', legend=True, ax=axes[0,1])
    axes[0,1].set_title("Potential Healthcare Needs")

    # plot potential workforce chloropleth in the third subplot
    merged_population.plot(column=columns['Total_percent_pop_15_64'], cmap='BuPu', legend=True, ax=axes[1,0])
    axes[1,0].set_title("Potential Workforce")

    # plot age dependency ratio chloropleth in the fourth subplot
    merged_population.plot(column=columns['age dependency ratio'], cmap='YlOrBr', legend=True, ax=axes[1,1])
    axes[1,1].set_title("Age Dependency Ratio")

    plt.tight_layout()
    plt.show()








def plot_language_choropleth(merged_languages: gpd.GeoDataFrame, columns: Dict[str, Any]) -> plt.Figure:
    """
    Create a 2x2 grid of subplots of chloropleth maps of language data.

    Parameters:
    merged_languages (geopandas.GeoDataFrame): A geopandas GeoDataFrame containing the language knowledge data for a certain population
    language_columns (dict): A dictionary of language column names and corresponding titles for each subplot
    
    Returns:
    matplotlib.figure.Figure: The generated matplotlib figure
    """
    # create a 2x2 grid of subplots
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10,10))

    # plot age distribution chloropleth in the first subplot
    merged_languages.plot(column=columns['Population who know English'], cmap='YlGn', legend=True, ax=axes[0,0])
    axes[0,0].set_title("Population who know English")

    # plot potential healthcare needs chloropleth in the second subplot
    merged_languages.plot(column=columns['Population who know French'], cmap='OrRd', legend=True, ax=axes[0,1])
    axes[0,1].set_title("Population who know French")

    # plot potential workforce chloropleth in the third subplot
    merged_languages.plot(column=columns['Population who know both English and French'], cmap='BuPu', legend=True, ax=axes[1,0])
    axes[1,0].set_title("Population who know both English and French")

    # plot age dependency ratio chloropleth in the fourth subplot
    merged_languages.plot(column=columns['Population who know neither English nor French'], cmap='YlOrBr', legend=True, ax=axes[1,1])
    axes[1,1].set_title("Population who know neither English nor French")

    plt.tight_layout()
    plt.show()

    return fig



def plot_mother_tongue_ratio(merged_languages: gpd.GeoDataFrame, columns: Dict[str, Any]) -> tuple:
  """
  Plots a choropleth map of the ratio of population with official and non-official languages as mother tongue.
  Args:
  merged_languages (GeoDataFrame): A GeoDataFrame containing the merged data.
  columns (dict): A dictionary containing the column names of the data to be plotted.

  Returns:
  fig, axes (matplotlib.figure.Figure, ndarray of AxesSubplot): The figure and axes of the plot.
  """

  fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15,8))

  # Plot the chloropleth map of people with official language as mother tongue
  merged_languages.plot(column=columns['Ratio - Population with Official Language as mother tongue'], cmap='YlGnBu', edgecolor='grey', legend=True, ax=axes[0])
  axes[0].set_title('Ratio - Population with Official Language as mother tongue')

  # Plot the chloropleth map of people with non-official language as mother tongue
  merged_languages.plot(column=columns['Ratio - Population with Un-official Language as mother tongue'], cmap='YlGnBu', edgecolor='grey', legend=True, ax=axes[1])
  axes[1].set_title('Ratio - Population with Un-official Language as mother tongue')

  plt.tight_layout()

  plt.show()

  return fig, axes



def generate_population_map(merged_population: gpd.GeoDataFrame) -> folium.Map:

  """
  Creates an interactive population map of Canada using the Folium library. This function expects a geodataframe with following columns
  ['DAUID', 'Average age of the population', 'Total_percent_pop_65', 'Total_percent_pop_15_64', 'age dependency ratio'] along with the geometry 

  Parameters:
      dataframe (pandas.DataFrame): A pandas DataFrame containing the population data for the Canadian provinces and territories.

  Returns:
      folium.Map: An interactive map displaying the age distribution, potential healthcare needs, potential workforce, and age dependency ratio for each Canadian province and territory.

  Raises:
      ValueError: If the input dataframe is empty or does not contain the necessary columns.

  """

  required_columns = ['DAUID', 'Average age of the population', 'Total_percent_pop_65', 'Total_percent_pop_15_64', 'age dependency ratio']
  if(merged_population.empty or not set(required_columns).issubset(set(merged_population.columns))):
      raise ValueError("Input dataframe must contain non-empty data with columns: 'DAUID', 'Average age of the population', 'Total_percent_pop_65', 'Total_percent_pop_15_64', and 'age dependency ratio'.")

  geo_data=merged_population.to_crs(epsg='4326')

  # Create the interactive map
  m = folium.Map(location=[geo_data.centroid.y.mean(), geo_data.centroid.x.mean()], zoom_start=8)

  # Add the age distribution layer to the map
  folium.Choropleth(
      geo_data=geo_data,
      data=merged_population,
      columns=['DAUID', 'Average age of the population'],
      key_on='feature.properties.DAUID',
      fill_color='YlGn',
      fill_opacity=0.7,
      line_opacity=0.2,
      legend_name='Average age of the population',
      name='Age Distribution'
  ).add_to(m)

  # Add the potential healthcare needs layer to the map
  folium.Choropleth(
      geo_data=geo_data,
      data=merged_population,
      columns=['DAUID', 'Total_percent_pop_65'],
      key_on='feature.properties.DAUID',
      fill_color='YlGnBu',
      fill_opacity=0.7,
      line_opacity=0.2,
      legend_name='Percentage of population over 65',
      name='Potential Healthcare Needs'
  ).add_to(m)

  # Add the potential workforce layer to the map
  folium.Choropleth(
      geo_data=geo_data,
      data=merged_population,
      columns=['DAUID', 'Total_percent_pop_15_64'],
      key_on='feature.properties.DAUID',
      fill_color='YlOrBr',
      fill_opacity=0.7,
      line_opacity=0.2,
      legend_name='Percentage of population aged 15-64',
      name='Potential Workforce'
  ).add_to(m)

  # Add the age dependency ratio layer to the map
  folium.Choropleth(
      geo_data=geo_data,
      data=merged_population,
      columns=['DAUID', 'age dependency ratio'],
      key_on='feature.properties.DAUID',
      fill_color='YlOrRd',
      fill_opacity=0.7,
      line_opacity=0.2,
      legend_name='Age dependency ratio',
      name='Age Dependency Ratio'
  ).add_to(m)

  # Add a layer control to the map
  folium.LayerControl().add_to(m)
    
  return m







def create_education_levels_map(gdf: gpd.GeoDataFrame, no_certificate_col: str, secondary_col: str, postsecondary_col: str, population_col: str) -> folium.folium.Map:
    """
    Creates an interactive leaflet map that shows the ratio of total_no_certificate, total_secondary, 
    and total_post_secondary to the total population for each DAUID in the input geodataframe.

    Args:
        gdf (geopandas.GeoDataFrame): The input geodataframe containing the data to be plotted.
        no_certificate_col (str): The name of the column containing the total number of people without 
                                  a certificate in each DAUID.
        secondary_col (str): The name of the column containing the total number of people with a secondary 
                             education in each DAUID.
        postsecondary_col (str): The name of the column containing the total number of people with a 
                                 post-secondary education in each DAUID.
        population_col (str): The name of the column containing the total population in each DAUID.

    Returns:
        folium.Map: A folium Map object containing the plotted data.
    """
    # Calculate the ratio columns
    gdf['no_certificate_col'] = gdf[no_certificate_col] / gdf[population_col]
    gdf['secondary_ratio'] = gdf[secondary_col] / gdf[population_col]
    gdf['postsecondary_ratio'] = gdf[postsecondary_col] / gdf[population_col]

    # Create the map
    gdf=gdf.to_crs(epsg='4326')
    center_lat = gdf['geometry'].centroid.y.mean()
    center_lon = gdf['geometry'].centroid.x.mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=10)

    # Add the choropleth layer for each ratio
    folium.Choropleth(
        geo_data=gdf,
        name='No Certificate Ratio',
        data=gdf,
        columns=['DAUID', 'no_certificate_col'],
        key_on='feature.properties.DAUID',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='No Certificate Ratio',
        highlight=True,
        overlay=True
    ).add_to(m)

    folium.Choropleth(
        geo_data=gdf,
        name='Secondary Ratio',
        data=gdf,
        columns=['DAUID', 'secondary_ratio'],
        key_on='feature.properties.DAUID',
        fill_color='YlGn',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Secondary Ratio',
        highlight=True,
        overlay=True
    ).add_to(m)

    folium.Choropleth(
        geo_data=gdf,
        name='Postsecondary Ratio',
        data=gdf,
        columns=['DAUID', 'postsecondary_ratio'],
        key_on='feature.properties.DAUID',
        fill_color='PuBu',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Postsecondary Ratio',
        highlight=True,
        overlay=True
    ).add_to(m)

    # Add layer control
    folium.LayerControl().add_to(m)

    return m

def plot_birth_density_maps(gdf):
    """
    Plots an interactive density map of count of births in different regions for each DAUID with separate layers for each birth place.

    Args:
    diversity (GeoDataFrame): A GeoDataFrame containing birth data for different regions.

    Returns:
    folium.Map: The interactive density map.
    """
    # Create a map centered on Montreal
    gdf=gdf.to_crs(epsg='4326')
    center_lat = gdf['geometry'].centroid.y.mean()
    center_lon = gdf['geometry'].centroid.x.mean()
    birth_map = folium.Map(location=[center_lat, center_lon], zoom_start=10)

    # Define the birth place layers
    birth_places = ['birth_Americas', 'birth_Europe', 'birth_Africa', 'birth_Asia', 'birth_Oceania_and_other']
    fill_colors = ['OrRd','OrRd', 'BuPu', 'YlOrBr', 'YlGn']

    # Add a Choropleth layer for each birth place
    for i, place in enumerate(birth_places):
        choropleth = folium.Choropleth(
            geo_data=gdf,
            data=gdf,
            columns=['DAUID', place],
            key_on='feature.properties.DAUID',
            fill_color=fill_colors[i],
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Births in ' + place,
            name=place
        ).add_to(birth_map)

    # Add layer control to toggle between birth place layers
    folium.LayerControl().add_to(birth_map)

    return birth_map

