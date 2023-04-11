from typing import Optional, Tuple, Any, Dict
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import folium


from typing import Optional
import pandas as pd
import geopandas as gpd

def read_data(shp_path: str, data_path: str, header_path: Optional[str] = None,
              split_char: Optional[str] = None, fillna_val: Optional[float] = None) -> tuple:

    """
    Load shapefile and data file, and rename data columns using header file.

    Args:
    shapefile_path (str): File path to shapefile.
    data_path (str): File path to data file.
    header_path (str): File path to header file.
    split_char (str): Character to split header file.
    fillna_value: Value to use when filling NaN values.

    Returns:
    tuple: A tuple containing:
            - gdf (geopandas.GeoDataFrame): A GeoDataFrame containing the shapefile data.
            - df (pandas.DataFrame): A DataFrame containing the data file data.
    """

    # read in shapefile and data file
    gdf = gpd.read_file(shp_path)
    demo_data = pd.read_csv(data_path)
    
    # fill missing values
    demo_data = demo_data.fillna(fillna_val)
    
    # read in header file (if applicable) and rename columns (if applicable)
    if header_path and split_char:
        header_dict = {}
        with open(header_path) as f:
            for line in f:
                cols = line.strip().split(split_char)
                header_dict[cols[0]] = cols[1]
        demo_data = demo_data.rename(columns=header_dict)
    
    return gdf, demo_data



def merge_dataframes(df1: gpd.GeoDataFrame, df2: pd.DataFrame, common_column: str,
                     filter_column1: Optional[str] = None, filter_value1: Optional[str] = None) -> gpd.GeoDataFrame:
    """
    Merges two dataframes based on a common column, optionally filtering one or both dataframes on a given column.

    Args:
    df1 (pd.DataFrame): The first dataframe to merge.
    df2 (pd.DataFrame): The second dataframe to merge.
    common_column (str): The name of the common column to merge on.
    filter_column1 (str): The name of a column in df1 to filter on.
    filter_value1 (str): The value to filter filter_column1 by.

    Returns:
    pd.DataFrame: The merged dataframe.
    """

    if filter_column1 is not None:
        df1 = df1[df1[filter_column1] == filter_value1]


    merged = df1.merge(df2, on=common_column)

    return merged



def calculate_language_ratios(dataframe: pd.DataFrame, columns_dict: dict)-> pd.DataFrame:
    """
    Calculate the ratios of population language knowledge based on specified columns in a dictionary
    
    Args:
    dataframe (pandas.DataFrame): the dataframe containing the language knowledge columns
    columns_dict (dict): a dictionary containing column names for the following keys:
        - 'Total_knowledge_eng'
        - 'Total_knowledge_fre'
        - 'Total_knowledge_fre_eng'
        - 'Total_knowledge_none'
        - 'Total_knowledge_languages'
        - 'Mother_tongue_official_lang'
        - 'Mother_tongue_non_official_lang'
        - 'Mother_tongue_Total'
    
    Returns:
    pandas.DataFrame: the input dataframe with additional columns for the language knowledge ratios
    """
    
    for key, column_name in columns_dict.items():
        if column_name not in dataframe.columns:
            raise ValueError(f"Column name {column_name} not found in dataframe")
    
    dataframe['ratio_eng'] = dataframe[columns_dict['Total_knowledge_eng']] / dataframe[columns_dict['Total_knowledge_languages']]
    dataframe['ratio_fre'] = dataframe[columns_dict['Total_knowledge_fre']] / dataframe[columns_dict['Total_knowledge_languages']]
    dataframe['ratio_both'] = dataframe[columns_dict['Total_knowledge_fre_eng']] / dataframe[columns_dict['Total_knowledge_languages']]
    dataframe['ratio_none'] = dataframe[columns_dict['Total_knowledge_none']] / dataframe[columns_dict['Total_knowledge_languages']]
    dataframe['ratio_mother_off'] = dataframe[columns_dict['Mother_tongue_official_lang']] / dataframe[columns_dict['Mother_tongue_Total']]
    dataframe['ratio_mother_unoff'] = dataframe[columns_dict['Mother_tongue_non_official_lang']] / dataframe[columns_dict['Mother_tongue_Total']]
    
    return dataframe

def get_highest_education_ratio(df: pd.DataFrame, population_col: str, education_level_col: str)->tuple:
    """
    This method takes in a dataframe and the names of the columns for population and education levels for each DAUID.
    It then computes the ratio of the total population in age 24 to 65 with a provided level of education to the total population
    in age 24 to 65 for each DAUID, and returns the DAUID and the education level that has the highest ratio.
    
    Parameters:
    df (pandas dataframe): The dataframe containing the population and education data for each DAUID.
    population_col (str): The name of the column for the total population for each DAUID.
    education_level_col (str): The name of the column for the total population in age 24 to 65 for each education level for each DAUID.
    
    Returns:
    highest_ratio (float): The highest ratio of the total population in age 24 to 65 with a certain level of education to
    the total population in age 24 to 65 for all DAUIDs.
    dauid_with_highest_ratio (str): The DAUID for which the highest ratio was found.
    education_level_with_highest_ratio (str): The education level that has the highest ratio of population in age 24 to 65.
    """
    
    # Calculate the ratio of the total population in age 24 to 65 with a certain level of education to
    # the total population in age 24 to 65 for each DAUID
    df['education_ratio'] = df[education_level_col] / df[population_col]
    
    # Find the maximum ratio and its corresponding DAUID and education level
    max_ratio_index = df['education_ratio'].idxmax()
    highest_ratio = df['education_ratio'][max_ratio_index]
    dauid_with_highest_ratio = df['DAUID'][max_ratio_index]
    education_level_with_highest_ratio = df.columns[df.columns.str.contains(education_level_col)][0]
    
    # Return the highest ratio, DAUID, and education level
    return highest_ratio, dauid_with_highest_ratio, education_level_with_highest_ratio