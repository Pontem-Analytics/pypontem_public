# PPL Parser Functionality Documentation

## Introduction

This document provides an overview of the PPL (Profile Plots) parser functionality. The PPL parser is a Python script designed to extract and process data from PPL files used in the oil and gas industry for pipeline simulation.

## Purpose
The PPL parser script serves the following purposes:
- Extract metadata information from PPL files.
- Extract branch names, profiles, and time series data from PPL files.
- Search for specific variables within PPL files based on various criteria.
- Extract trends from PPL files.
- Extracting and Joining nodes for specific branches from PPL files

## Overview

`pplParser`: Class holding the PPL parser functionality.

- Methods:
    - `_extract_metadata`:
    This function is responsible for extracting metadata from a given PPL file. It parses specific metadata tags within the file, such as version, input file, date, project, title, author, and geometry, and stores them in a dictionary.
    
        - Arguments: 
            - `None` (It accesses the PPL file content internally).

        - Returns:
            - A pandas dataframe containing the metadata 

    - `_extract_branch_profiles`:
    This function extracts and displays elevation profiles for specific branches or all branches in the PPL file. It searches for the "BRANCH" sections in the file, extracts the lengths and elevations data for each branch, and creates a DataFrame to represent the profiles.
        - Arguments: 
            - `target_branch (optional)`: The specific branch for which the profile data will be extracted. If not provided, profiles for all branches are extracted.
        - Returns:
            - A pandas dataframe containing branch profiles

    - `search_catalog`:
    This function searches for variables within the catalog based on specified criteria such as variable name, locator name, and pipe name. It uses the search function internally to perform the search operation on the catalog DataFrame.
        - Arguments:
            - `var_name`: The keyword to search for in variable names.
            - `loc_name`: The keyword to search for in locator names.
            - `pipe_name` (optional): The keyword to search for in pipe names.
        - Returns:
            - A pandas dataframe containing search results from the catalog

    - `extract_trend`:
    This function extracts trend data for a specified variable and location from the PPL file. It searches for the variable in the catalog, retrieves the corresponding time series data, applies necessary unit conversions, and returns a DataFrame containing the trend data.

        - Arguments:
            - `input_matrix (pd.DataFrame)`: DataFrame specifying the variables and locations for trend extraction. Includes columns like (varname, locname, pipename, row_number, out_unit, and time_unit.)
        - Returns:
            - A pandas DataFrame containing the time trend for the chosen variable, with units managed according to the UnitConversion class and units.yaml file.

    - `extract_trends_join_nodes`:
    This function joins different branches specified in the branch_matrix. It extracts trend data for a specific variable and location using the extract_trend function and then computes the join nodes of the extracted data by joinning branches which are outputted by the extract_trends function and are specified in the branch_matrix by the user.

        - Arguments:
            -  `input_matrix (pd.DataFrame)`: The DataFrame containing the trend data.
            - `branch_matrix (pd.DataFrame)`: The DataFrame containing the order at which the user wants the branches to be joined.
        - Returns:
             - A pandas DataFrame containing the time trend and profiles trends for the specified branches, with units managed according to the UnitConversion class and units.yaml file

`pplBatchParser`: Class for Batch PPL File Parsing
- Methods:
    - `extract_trends`:
    This function performs batch extraction of trend data for multiple PPL files based on the input matrix. It processes each PPL file, extracts the specified trends, and combines the results into a single DataFrame.

        - Arguments:
            - `input_matrix (pd.DataFrame)`: DataFrame specifying the PPL files and variables to extract trends from. 
        - Returns:
            - A pandas DataFrame containing the combined trend data from all specified PPL files.

    - `join_batch_nodes`:
    This function performs the extract_trends_join_nodes method to multiple PPL files.

        - Arguments:
            - `input_matrix (pd.DataFrame)`: DataFrame specifying the PPL files and variables for which averages will be calculated. 
            - `branch_matrix (pd.DataFrame)`: The DataFrame containing the order at which the user wants the branches to be joined.
        - Returns:
            - A pandas DataFrame containing the time trend and profiles trends for the specified files and branches, with units managed according to the UnitConversion class and units.yaml file.

# Input Matrix format

In version 0.3 we introduced an input matrix when processing tpl files by extracting trends of multiple variables in multiple positions. This enables flexible input specification to fetch all variables in one go. The required format is provided below:

![alt text](img/input_matrix.png)

If you are using the python API in a Jupyter notebook, this could be setup in a csv file which can be read as a dataframe. If you are using the xlwings add-in, you can specify this in a range in Excel.

As of version 0.3.1, the column names should be as given in the example above. The different columns are
- `varname` : Name of variable as specified in OLGA file
- `branchname` : Location name for the variable. This could be a branch name or position name
- `out_unit` : The output unit you desire. If you leave this blank, default units within the OLGA file will be used. `NOTE`: The list of compatible units, the syntax and whether they are tested is provided in `docs/units_tested_logbook.csv`. We are actively testing more unit conversions, but as of Version 0.2 most common unit conversions have been tested. If you do not use the syntax provided, there will be errors.
- `out_unit_profile`: The unit of profiles you want your outputs in. 
- `time_unit` : The unit of time you desire the outputs in. 
- `start_time` : The starting time of the timestamp range you want to extract trends 
- `end_time` : the ending time of the timestamp range you want to extract trends

# Branch Matrix

With the join nodes functionality, we introduced an branch matrix when processing ppl files by joinning branches of multiple variables and multiple branches. This enables flexible input specification to join all branches specified in one go. The required format is provided below:

If you are using the python API in a Jupyter notebook, this could be setup in a csv file which can be read as a dataframe. If you are using the xlwings add-in, you can specify this in a range in Excel.

The different columns are:
- `branch_in` : Name of starting branches.
- `branch_out` : Name of ending branches.

![Branch Matrix](img/branch_matrix.png)
