# TPL Parser Functionality Documentation

## Introduction

This document provides an overview of the TPL (Transient Pipeline) parser functionality. The TPL parser is a Python script designed to extract and process data from TPL files used in the oil and gas industry for pipeline simulation.

## Purpose
The TPL parser script serves the following purposes:
- Extract metadata information from TPL files.
- Extract branch names, profiles, and time series data from TPL files.
- Search for specific variables within TPL files based on various criteria.
- Calculate the average of variable values over time.

## Overview

`tplParser`: Class holding the TPL parser functionality.

- Methods:
    - `_extract_metadata`:
    This function is responsible for extracting metadata from a given TPL file. It parses specific metadata tags within the file, such as version, input file, date, project, title, author, and geometry, and stores them in a dictionary.
    
        - Arguments: 
            - `None` (It accesses the TPL file content internally).

        - Returns:
            - A pandas dataframe containing the metadata 

    - `_extract_branch_profiles`:
    This function extracts and displays elevation profiles for specific branches or all branches in the TPL file. It searches for the "BRANCH" sections in the file, extracts the lengths and elevations data for each branch, and creates a DataFrame to represent the profiles.
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
    This function extracts trend data for a specified variable and location from the TPL file. It searches for the variable in the catalog, retrieves the corresponding time series data, applies necessary unit conversions, and returns a DataFrame containing the trend data.

        - Arguments:
            - `input_matrix (pd.DataFrame)`: DataFrame specifying the variables and locations for trend extraction. Includes columns like (varname, locname, pipename, row_number, out_unit, and time_unit.)
        - Returns:
            - A pandas DataFrame containing the time trend for the chosen variable, with units managed according to the UnitConversion class and units.yaml file.

    - `calc_average`:
    This function calculates the average of values in the DataFrame up to the specified index or of the last n values. It extracts trend data for a specific variable and location using the extract_trend function and then computes the average of the extracted data.

        - Arguments:
            -  `input_matrix (pd.DataFrame)`: The DataFrame containing the trend data.
            - `start_index (int, optional)`: The starting index for the average calculation.
            - `end_index (int, optional)`: The ending index for the average calculation.
            - `n_rows (int, optional)`: Number of rows to consider from the end for averaging.
            - `n_timeunits (float, optional)`: Number of time units to consider for     averaging. Note : The time unit used will be the time unit specified in the input matrix.
        - Returns:
             - A float value representing the average

`tplBatchParser`: Class for Batch TPL File Parsing
- Methods:
    - `extract_trends`:
    This function performs batch extraction of trend data for multiple TPL files based on the input matrix. It processes each TPL file, extracts the specified trends, and combines the results into a single DataFrame.

        - Arguments:
            - `input_matrix (pd.DataFrame)`: DataFrame specifying the TPL files and variables to extract trends from. 
        - Returns:
            - A pandas DataFrame containing the combined trend data from all specified TPL files.
    - `calc_averages`:
    This function calculates the average values for multiple TPL files based on specified criteria. It processes each TPL file, extracts the trends, and computes the averages as specified in the input matrix.

        - Arguments:
            - `input_matrix (pd.DataFrame)`: DataFrame specifying the TPL files and variables for which averages will be calculated. 
            - `start_index (int, optional)`: The starting index for the average calculation.
            - `end_index (int, optional)`: The ending index for the average calculation.
            - `n_rows (int, optional)`: Number of rows to consider from the end for averaging.
            - `n_timeunits (float, optional)`: Number of time units to consider for averaging. Note : The time unit used will be the time unit specified in the input matrix.
        - Returns:
            - A pandas DataFrame containing the average values for each specified variable across the TPL files.

# Input Matrix format

In version 0.2 we introduced an input matrix when processing tpl files by extracting trends of multiple variables in multiple positions. This enables flexible input specification to fetch all variables in one go. The required format is provided below:

![alt text](img/input_matrixTPL.png)

If you are using the python API in a Jupyter notebook, this could be setup in a csv file which can be read as a dataframe. If you are using the xlwings add-in, you can specify this in a range in Excel.

As of version 0.2, the column names should be as given in the example above. The different columns are
- `varname` : Name of variable as specified in OLGA file
- `locname` : Location name for the variable. This could be a branch name or position name
- `pipename` : The name of the pipe. Some variables may not need this, in which case it can be left blank
- `row_number` : The number of rows you want in the output for `extract_trend`
- `out_unit` : The output unit you desire. If you leave this blank, default units within the OLGA file will be used. `NOTE`: The list of compatible units, the syntax and whether they are tested is provided in `docs/units_tested_logbook.csv`. We are actively testing more unit conversions, but as of Version 0.2 most common unit conversions have been tested. If you do not use the syntax provided, there will be errors 
- `time_unit` : The unit of time you desire the outputs in. 
