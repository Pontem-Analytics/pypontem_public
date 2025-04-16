"""
PPL parser functionality
"""

import warnings
import cProfile
import pstats
import time as t
# temporary to remove pandas 3.0 deprecationwarning about pyarrow from printing
warnings.filterwarnings("ignore", category=DeprecationWarning)

import pandas as pd
import numpy as np
import argparse
import re
from functools import reduce
from pathlib import Path
import os
import sys
import math
import yaml
from io import StringIO


sys.path.insert(0, "src")
from pypontem.utils.unit_conversion import UnitConversion, unit_map

current_dir = os.path.dirname(os.path.abspath(__file__))
YAML_PATH = os.path.join(current_dir, "..", "utils", "units.yaml")

# YAML_PATH = "src/pypontem/utils/units.yaml"


def read_file(file_path):
    if os.path.isfile(file_path):
        with open(file_path, "r") as file:
            content = file.read()
        return content
    else:
        raise FileNotFoundError(
            f"The file specified '{file_path}' does not exist. Please verify the location of the file."
        )


def open_yaml(yaml_path):
    with open(yaml_path, "r") as file:
        unitsdb = yaml.safe_load(file)
    return unitsdb


pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", None)


def search(df, var_name=None, **locator_types):
    """
    Searches for variables in the DataFrame based on variable names, dynamically detected locator types, 
    and additional filtering conditions (pipe_name, pipe_number, wall_layer) when necessary.

    Args:
        df (pandas.DataFrame): The DataFrame to search within.
        var_name (str): Variable name.
        **locator_types (dict): Arbitrary keyword arguments for locator columns (e.g., Choke="Choke_1", Position="POS_1").
    
    Returns:
        pandas.DataFrame: Filtered DataFrame based on search criteria.
    """
    filter_conditions = []

    if var_name:
        varname_df = df[df["Variable"].str.upper() == var_name.upper()]

        # If there's only one match and its locator type is 'GLOBAL', return immediately
        if len(varname_df) == 1 and 'GLOBAL' in varname_df.columns:
            if varname_df["GLOBAL"].iloc[0]:
                return varname_df.dropna(axis=1, how='all')
            
        filter_conditions.append(df["Variable"].str.upper() == var_name.upper())

    for col, value in locator_types.items():
        if col in df.columns and value and value != "None":
            if col == "GLOBAL":
                filter_conditions.append(df[col])
            elif col == "NR" or col == "WALL LAYER":
                df[col] = df[col].astype(float)
                filter_conditions.append(df[col] == value)
            else:    
                filter_conditions.append(df[col].str.upper() == value.upper())

    if filter_conditions:
        result_df = df[reduce(lambda x, y: x & y, filter_conditions)]
    else:
        result_df = df 

    # if len(result_df) > 1:
    #     additional_filters = [col for col in result_df.columns if col not in locator_types and col != "varname" and col !="Locator Type" and col != "out_unit" and col != "Description"]
    #     if additional_filters:
    #         raise ValueError(
    #             f"Multiple results found for variable '{var_name}'. "
    #             f"Consider adding one of the following filters to refine the search: {additional_filters}"
    #         )
    #     else:
    #         raise ValueError(
    #             f"Multiple results found for variable '{var_name}', but no additional filtering columns are available."
    #         )

    if result_df.empty:
        raise ValueError(f"No matching data found for variable '{var_name}' with the specified locator filters.")
    
    result_df = result_df.dropna(axis=1, how='all')
    return result_df


class pplParser:
    """
    Class which holds the ppl parser functions
    
    Functions:
        1. metadata: to extract metadata from a ppl file
        2.branch_names: to extract branch names from a ppl file
        3.branch_profiles: to extract branch profile information from a ppl file
        4.parse_number_of_variables: to extract the number of variables present in a ppl file
        5. extract_catalog: to extract 
        6. search_catalog: to extract the information from the catalog of the variable specified
        7. extract_profile: to extract profiles in a ppl file
        8. extract_profile_join_nodes: to join nodes of branches extracted in a ppl file	
    """

    def __init__(self, filepath):
        """
        Initializes an instance of the class by loading file data and unit definitions.
        
        Arguments:
            - filepath (str): The path to the ppl file to be loaded.
        """


        # read file from path
        self.filepath = Path(filepath)
        # save content of file in memory so we don't open it repeatedly - NOTE: may need to be changed later
        self.content = read_file(self.filepath)
        # open unit yaml file
        self.unitsdb = open_yaml(YAML_PATH)

    @property
    def metadata(self):
        """
        Extracts metadata from the content stored in the object and returns it as a pandas DataFrame.
        
        Arguments:
            - file_path (str): the path to the ppl file
        
        Returns:
            - pandas.DataFrame: A DataFrame containing the extracted metadata with keys as column headers
        """
        return self._extract_metadata()

    def _extract_metadata(self):
        metadata = {}  # Dictionary to store metadata

        try:
            branch_index = self.content.index("BRANCH\n")
        except ValueError:
            branch_index = len(self.content)

        # Extract metadata before "BRANCH"
        metadata_lines = self.content[:branch_index]

        # Parsing specific metadata and storing in dictionary
        for i, line in enumerate(metadata_lines.splitlines()):
            line = line.strip()
            olga_match = re.search(r"OLGA\s+(\S+)", line)
            if olga_match:
                metadata["version"] = line.strip("'")
            elif "INPUT FILE" in line:
                metadata["Input file"] = [
                    metadata_lines.splitlines()[i + 1].strip().strip("'")
                ]
            elif "PVT FILE" in line:
                metadata["pvt"] = [
                    metadata_lines.splitlines()[i + 1].strip().strip("'")
                ]
            elif "DATE" in line:
                metadata["time"] = [
                    metadata_lines.splitlines()[i + 1].strip().strip("'")
                ]
            elif "PROJECT" in line:
                metadata["project"] = [
                    metadata_lines.splitlines()[i + 1].strip().strip("'")
                ]
            elif "TITLE" in line:
                metadata["title"] = [
                    metadata_lines.splitlines()[i + 1].strip().strip("'")
                ]
            elif "AUTHOR" in line:
                metadata["author"] = [
                    metadata_lines.splitlines()[i + 1].strip().strip("'")
                ]
            elif "GEOMETRY" in line:
                match = re.search(r"\((.*?)\)", line)
                if match:
                    metadata["geometry"] = [match.group(1)]
        return pd.DataFrame(metadata)
    
    @property
    def branch_names(self):
        """
        Extracts and prints the names of all branches in the given ppl file.
        
        Arguments:
            - None.
        
        Returns:
            - branch_names (list): A list of extracted branch names as strings.
        """

        return self._extract_branch_names()

    def _extract_branch_names(self):
        df_branch_names = []
        pattern = "(BRANCH|ANNULUS)\n(.+)"
        branch_names = re.findall(pattern, self.content)
        for branch in branch_names:
            df_branch_names.append(
                branch[1]
            )  # Accessing the second element (branch name) of each tuple
        return df_branch_names

    @property
    def branch_profiles(self):
        """
        Extracts and displays elevation for a specific branch or all branches in the file.
        
        Arguments:
            - target_branch (str, optional): The specific branch to display data for. Defaults to None.
        
        Returns:
            - pandas.Dataframe: a dataframe containing the profiles of the specified branch.
        """

        return self._extract_branch_profiles(target_branch=None)

    def _extract_branch_profiles(self, target_branch=None):
        def create_branch_table(branch_data):
            # Ensure lengths and elevations have the same length
            min_length = min(
                len(branch_data["Lengths"]), len(branch_data["Elevations"])
            )
            df = pd.DataFrame(
                {
                    "Lengths_("
                    + str(self.metadata["geometry"].values[0]).lower()
                    + ")": branch_data["Lengths"][:min_length],
                    "Elevations_("
                    + str(self.metadata["geometry"].values[0]).lower()
                    + ")": branch_data["Elevations"][:min_length],
                    "Pipe Number":num_pipes,
                }
            )
            return df

        # Define a pattern to match each 'BRANCH' section
        branch_pattern = re.compile(
            r"(BRANCH|ANNULUS)\n'(.*?)'\n(\d+)\n([\s\S]*?)(?=(BRANCH|ANNULUS)|\nCATALOG)",
            re.DOTALL,
        )

        # Find all matches
        matches = branch_pattern.findall(self.content)
        found = False  # Flag to check if the target branch is found

        branches = {}

        for match in matches:
            branch_data = {}
            branch_name = match[1]
            num_pipes = int(match[2])
            data_section = match[3].split()
            if data_section:
                midpoint = len(data_section) // 2
                lengths = [float(data) for data in data_section[:midpoint]]
                elevations = [float(data) for data in data_section[midpoint:]]
                branch_data = {
                    "Branch": branch_name,
                    "Lengths": lengths,
                    "Elevations": elevations,
                }

                # Display branch data only if it matches the target branch
                if not target_branch or branch_name == target_branch:
                    found = True  # Set found to True if the branch is found
                    profile = create_branch_table(branch_data)
                    branches[branch_name] = profile

        if (
            not found and target_branch
        ):  # Display message if branch not found and target_branch is provided
            raise ValueError(
                f"The branch '{target_branch}' does not exist in the file."
            )
        else:
            return branches
        
    @property
    def n_vars(self):
        """
        Parses the number of variables from a given file path.
        
        Arguments:
            - None
        
        Returns:
            - n_vars (int): The number of variables if found, else None.
        """

        return self._parse_number_of_variables()

    def _parse_number_of_variables(self):
        # regex pattern which finds the next line after CATALOG
        pattern = re.search(r"CATALOG[\r \n]+([^\r\n]+)", self.content)
        return int(pattern[1])

    @property
    def catalog(self):
        """
        Extract variable information from the provided content using a regular expression pattern.
        
        Arguments:
            - None.
        
        Returns:
            - pandas.DataFrame: A DataFrame containing all the catalog information available in the ppl file.

        """
        return self._extract_catalog()

    def _extract_catalog(self):
        pattern = re.compile(
            r"""
            (?P<varname>\S+)        # Variable name (A, B, C, etc.)
            \s+'(?P<location>[^']*)'
            \s*'(?P<locator_type>[^']*)'?  # CHOKE:, NODE:, BRANCH:
            \s*'(?P<locname>[^']*)'? # extracting the location names
            (?P<extras>(\s*'[^']*')*)?  # Capture all additional optional fields dynamically
            \s*'(?P<unit>[^']*)'     # Unit (e.g., (PA), (-), (C))
            \s*'(?P<description>[^']*)'  # Description
            """,
            re.VERBOSE,
        )
    
        lines = self.content.splitlines()
        data_list = []
    
        for line in lines:
            match = pattern.match(line)
            if match:
                data_entry = {
                    "Variable": match.group("varname"),
                    "Locator Type":match.group("location"),
                    "Units": match.group("unit").strip("()"),
                    "Description": match.group("description")
                }

                # Capture and process locator types
                locator_type = match.group("locator_type").capitalize()
                if locator_type:
                    locname = match.group("locname")
                    data_entry[locator_type] = locname  # Create a column with locator type value
                
                extras = match.group("extras").strip().split("' '") if match.group("extras") else []
                last_key = None
                
                for extra in extras:
                    extra = extra.strip("'")
                    if extra.endswith(":"):
                        last_key = extra.strip(":")
                        data_entry.setdefault(last_key, [])  # Initialize column as list
                    elif last_key:
                        data_entry[last_key].append(extra)
                        last_key = None  # Reset for next key-value pair
                
                # Convert list values to single values if only one item exists
                for key in data_entry:
                    if isinstance(data_entry[key], list) and len(data_entry[key]) == 1:
                        data_entry[key] = data_entry[key][0]
                
                data_list.append(data_entry)
    
        # Convert to DataFrame
        df = pd.DataFrame(data_list)
        df.columns = [col.replace(":", "") for col in df.columns]
        final_columns = ["Variable"] + [col for col in df.columns if col not in ["Variable", "Units", "Description"]] + ["Units", "Description"]
        df = df[final_columns]
        return df
    
    def search_catalog(self, var_name=None, **locators):
            """
            Searches for variables containing a keyword in their names within a DataFrame.
            
            Arguments:
                - Var_name (str): The variable name
                - Loc_name (str): The location of the variable you want to search for
                - Pipe_name (str): the pipe name of the variable name specified located at the location name provided.
            
            Returns:
                - Pandas.DataFrame: a dataframe containing catalog information of the variables specified.
    
            """
            cat = self._extract_catalog()
            locators = {key.replace("_", " "): value for key, value in locators.items()}
            result_df = search(cat, var_name, **locators)
            # if result_df.empty:
            #     raise ValueError(f"We don't have {var_name} in our catalog.")
            result_df = result_df.drop(columns=["Locator Type"])
            return result_df
    
    def _extract_time_series_data(self):
        """
        Process time series data from the ppl file.
        
        Arguments:
            - None
        
        Returns:
            - pandas.DataFrame: DataFrame containing time series variable outputs.
        """

        # Define regex pattern to extract the number of rows from CATALOG section
        data = self.content
        catalog_pattern = r'CATALOG\s+(\d+)'
        catalog_match = re.search(catalog_pattern, data)

        if catalog_match:
            number_of_rows = int(catalog_match.group(1))
        else:
            raise ValueError("Number of rows under CATALOG not found")

        # Define regex pattern to extract the TIME SERIES section
        time_series_pattern = r'TIME SERIES\s+\'\s*\(S\)\s*\'([\s\S]+?)(?=\n\n|\Z)'
        time_series_match = re.search(time_series_pattern, data)
        if time_series_match:
            time_series_section = time_series_match.group(0)
            bracket_match = re.search(r"\((.*?)\)", time_series_section)
            time_unit = bracket_match.group(1) if bracket_match else None
            time_series_data = time_series_match.group(1).strip()
        else:
            raise ValueError("TIME SERIES section not found")
        content = self._extract_catalog()
        variable_Names = content["Variable"].reset_index(drop=True)
        # branch_names = content["BRANCH"].reset_index(drop=True)
        # branch_names = [col for col in content.columns if col not in ["varname", "out_unit","Description","Locator Type"]]
        excluded_columns = {"Variable", "Units", "Description", "Locator Type"}

        # Identify the branch column dynamically
        branch_col = next(
            (col for col in content.columns if col not in excluded_columns),
            None
        )
        # Ensure a valid branch column is found
        if branch_col:
            branch_names = content[branch_col].reset_index(drop=True)  # Keep index clean
            # print("Detected branch column:", branch_col)
        else:
            raise ValueError("Branch column not found")
            
        units = content["Units"].reset_index(drop=True)
        lines = time_series_data.split('\n')
        time_dict = {}

        for line in lines:
            values = line.split()
            if len(values) == 1:
                current_time = values[0]
                time_dict[current_time] = []
            else:
                time_dict[current_time].append(values[0:])

        time_out = []
        values_out = []
        for time, values in time_dict.items():
            time_out.append(time)
            values_out.append(values)
        
        columns = []
        data = []

        for idx, time in enumerate(time_out):
            for var_name, branch_name,unit in zip(variable_Names, branch_names,units):
                columns.append(f"{branch_name}_{var_name}_time_in_{time_unit}:_{time}_{unit}")
            for row in values_out[idx]:
                data.append(row)

        # Checking that the number of columns matches the number of data points
        expected_columns = len(variable_Names) * len(time_out)
        if len(columns) != expected_columns:
            raise ValueError(f"Expected {expected_columns} columns, but got {len(columns)}")
        # Converting the  data to the correct format
        
        flattened_data = []
        for values in values_out:
            for value_set in values:
                flattened_data.append(value_set)
        if len(flattened_data) % len(columns) != 0:
            raise ValueError(f"Data length {len(flattened_data)} is not a multiple of the number of columns {len(columns)}")
         
        df = pd.DataFrame([flattened_data[i:i + len(columns)] for i in range(0, len(flattened_data), len(columns))], columns=columns)
        df1= df.values
        flattened_data = []
        max_length = max(len(sublist) for sublist in df1)
        max_length = max(len(sublist) for sublist in data)

        flattened_data_np = np.full((len(data), max_length), None, dtype=object)
        for i, sublist in enumerate(data):
            flattened_data_np[i, :len(sublist)] = sublist
        transposed_data = flattened_data_np.T

        df_final = pd.DataFrame(transposed_data, columns=columns)
        return df_final

    def extract_profile(self, input_matrix):
        """
        Extracts and processes profile data from an input matrix, performing unit conversions and time filtering.
        
        Arguments:
            - input_matrix (pd.DataFrame): The matrix file containing input data, including variable names, branches, units, and time specifications.
        
        Returns:
            - pandas.DataFrame: A combined DataFrame containing the processed trend data with converted units and filtered time ranges.
        """

        # Extract metadata and profile-related information

        if type(input_matrix) == dict:
            if all(not isinstance(v, (list, tuple, pd.Series)) for v in input_matrix.values()):
                input_matrix = pd.DataFrame([input_matrix])
            input_matrix = pd.DataFrame(input_matrix)
        elif type(input_matrix) == pd.DataFrame:
            input_matrix = input_matrix
        else:
            input_matrix = pd.read_csv(input_matrix)

        catalog = self._extract_catalog()
        profiles = self.branch_profiles
        metadata = self.metadata
        profile_unit = metadata["geometry"]
        profile_unit_cleaned = profile_unit.str.lower()
        time_series = self._extract_time_series_data()
        df_catalog = catalog.drop(columns=["Description"])
        df = pd.concat(profiles.values(), keys=profiles.keys()).reset_index(level=0).rename(columns={"level_0": "Category"})
        df.drop(columns=["Elevations_(m)"], inplace=True)

        input_matrix = input_matrix.dropna(how="all")
        variable_names = input_matrix["varname"].to_list()
        trend_df = []

        for index, row in input_matrix.iterrows():
            var_name = row["varname"]
            if not isinstance(var_name, str):
                raise ValueError(f"No variable name specified in row {index + 1}")

            out_unit = row["out_unit"]
            out_unit_profile = row["out_unit_profile"]
            out_time_unit = row["time_unit"]
            start_time = row["start_time"]
            end_time = row["end_time"]

            # Collecting all locators dynamically
            locators = {col: row[col] for col in input_matrix.columns if col not in ["varname", "out_unit", "out_unit_profile", "time_unit", "start_time", "end_time"]}
            locators = {key: value for key, value in locators.items() if pd.notna(value)}

            # if not locators:
            #     raise ValueError(f"No locator specified for variable '{var_name}' in row {index + 1}")

            # search_pattern = f'^{var_name}_'
            for key, value in locators.items():
                search_pattern = f'^{value}_{var_name}_'

            # Filter time series data using the dynamically constructed regex
            data = time_series.filter(regex=search_pattern)
            # Create a matching condition for the catalog based on the locators
            # match_condition = (df_catalog["varname"] == var_name)

            # # Dynamically add conditions for each locator column specified by the user
            for locator_column, locator_value in locators.items():
                pass
            #     match_condition &= (df_catalog[locator_column] == locator_value)

            # # Find the matching row in the catalog
            # match = df_catalog[match_condition]

            

            search_args = {"var_name": var_name, **locators}
            match = search(df_catalog, **search_args) if search_args else pd.DataFrame()
            match.reset_index(drop=True, inplace=True)

            if len(match) > 1:
                additional_filters = [col for col in match.columns if col not in locators and col != "Variable" and col !="Locator Type" and col != "Units" and col != "Description"]
                if additional_filters:
                    raise ValueError(
                        f"Multiple results found for variable '{var_name}'. "
                        f"Consider adding one of the following filters to refine the search: {additional_filters}"
                    )
                else:
                    raise ValueError(
                        f"Multiple results found for variable '{var_name}', but no additional filtering columns are available."
                    )
                
            if not match.empty:
                location = match["Locator Type"].values[0]
            else:
                raise ValueError(f"Branch '{locator_value}' not found in the catalog.")

            # Profile extraction
            # all_profiles = {}
            # for locator_column, locator_value in locators.items():
            pipe_data = df[df["Category"] == locator_value]
            profiles_data = pipe_data["Lengths_(m)"].tolist()
            if location == "BOUNDARY:":
                result = pd.DataFrame(profiles_data, columns=["Profiles"])
            else:
                result = pd.DataFrame([(profiles_data[i] + profiles_data[i + 1]) / 2 for i in range(len(profiles_data) - 1)], columns=["Profiles"])
            #     all_profiles[locator_column] = results
            # result = pd.concat(all_profiles) if all_profiles else pd.DataFrame()    
            # Converting Profiles values using UnitConversion
            con_vals = []
            unit = profile_unit_cleaned.to_string(index=False)
           
            if pd.isna(out_unit_profile):
                out_unit_profile = unit

            for value in result["Profiles"]:
                value_tagged = getattr(UnitConversion, "Length")(float(value), unit)
                con_vals.append(round(value_tagged.convert(to_unit=out_unit_profile), 3))

            col_name = f"Profiles_{locator_value}_{var_name}_{out_unit_profile}"
            result1 = pd.DataFrame(con_vals, columns=[col_name])
            
            # Process trend and time values
            final_df = data.dropna()
            unit = match["Units"].str.lower().to_string(index=False)
            
            unit_class = self.unitsdb["OLGA_vars"].get(var_name)
            # print(unit_class)
            if unit_class is None:
                for k, v in self.unitsdb["OLGA_startswith"].items():
                    if str(var_name).startswith(k):
                        unit_class = v
            converted_vals = []
            updated_column_vals = []
            for column in final_df.columns:
                time_values = re.findall(r"[-+]?\d*\.\d+e[-+]?\d+|[-+]?\d+\.\d+", column)
                for val in time_values:
                    values = float(val)
                    time_unit_match = re.search(r"in_(\w+):", column)
                    time_unit_init = time_unit_match.group(1)

                    if time_unit_init in unit_map:
                        time_unit = unit_map[time_unit_init]

                    if pd.isna(out_time_unit):
                        out_time_unit = time_unit

                    value_tagged = getattr(UnitConversion, "Time")(values, time_unit)
                    converted_time = round(value_tagged.convert(to_unit=out_time_unit), 3)

                    updated_text = column.replace(val, str(converted_time))
                    updated_text = re.sub(r"(_in_)" + time_unit_init + r"(:)", r"\1" + out_time_unit + r"\2", updated_text)
                    updated_column_vals.append(updated_text)

            final_df.columns = updated_column_vals
            
            # Filtering based on time range
            time_numeric = final_df.columns.str.extract(r"time_in_" + out_time_unit + r"[_:]*([+-]?\d*\.\d+|\d+)", expand=False).astype(float)
            time_values_series = pd.Series(time_numeric.values.flatten(), index=final_df.columns)

            if pd.notna(start_time) and pd.notna(end_time):
                if start_time > end_time:
                    raise ValueError("Start time cannot be greater than end time.")
                filtered_columns = final_df.columns[time_values_series.between(start_time, end_time)]
            elif pd.notna(end_time):
                raise ValueError("Start time is not specified.")
            elif pd.notna(start_time):
                raise ValueError("End time is not specified.")
            else:
                filtered_columns = final_df.columns

            filtered_df = final_df[filtered_columns]
            # print(filtered_df)
            # Convert trend values
            for _, row in filtered_df.iterrows():
                for column_name in filtered_df.columns:
                    value = float(row[column_name])
                    if "-" in unit:
                        unit = unit.replace("-", "")

                    if pd.isna(out_unit):
                        if unit in unit_map:
                            unit = unit_map[unit]
                        out_unit = unit
                    
                    

                    
                
                    value_tagged = getattr(UnitConversion, unit_class)(value, unit)
                    converted_vals.append(round(value_tagged.convert(to_unit=out_unit), 3))

            reshaped_values = [converted_vals[i:i + len(filtered_df.columns)] for i in range(0, len(converted_vals), len(filtered_df.columns))]
            structured_df = pd.DataFrame(reshaped_values, columns=filtered_df.columns)

            def update_brackets(column_name, new_value):
                return re.sub(r"\(.*\)", f"({new_value})", column_name)

            structured_df.columns = [update_brackets(col, out_unit) for col in structured_df.columns]

            trends = pd.concat([result1, structured_df], axis=1)
            # trends.set_index(col_name, inplace=True)
            trend_df.append(trends)
        combined_df = pd.concat(trend_df, axis=1, keys=variable_names, ignore_index=False)
        # combined_df.reset_index(inplace=True) 
        # print(combined_df.columns)
        # Sorting NaN values to the bottom
        for col in combined_df.columns:
            combined_df[col] = combined_df[col].dropna().tolist() + [np.nan] * combined_df[col].isna().sum()
        
        return combined_df
        

    def extract_profiles_join_nodes(
            self,
            input_matrix,
            branch_matrix,
    ):
        """ 
        Extracts and processes profile data for branches, combining boundary and section data. 
        
        Arguments:
            - input_matrix (pd.DataFrame): A matrix containing trend data for various branches with columns ['branchname', 'varname', 'out_unit', 'out_unit_profile', 'time_unit']. 
            - branch_matrix (pd.DataFrame): A matrix containing information about branch connections with columns ['branch_in', 'branch_out']. 
        
        Returns: 
            - pandas.DataFrame: A combined DataFrame containing processed trend data for the specified branches, including boundary and section data, with consistent units and profiles. 
        """

        data_df = self.extract_profile(input_matrix) 
        if type(branch_matrix) == dict:
            if len(branch_matrix) == 1:
                branch_matrix = pd.DataFrame([branch_matrix], [0])
            branch_matrix = pd.DataFrame(branch_matrix)

        branch_matrix = pd.DataFrame(branch_matrix)
        catalog = self._extract_catalog()
        df_catalog = catalog.drop(columns=['Description'])
        branch_profiles = self.branch_profiles
        result = {}
        for section, df in branch_profiles.items():
            result[section] = df['Pipe Number'].unique()

        # Convert the result to a DataFrame for better visualization
        result_df = pd.DataFrame.from_dict(result)
        # Select one level of the MultiIndex (e.g., level 1)
        data_df.columns = data_df.columns.get_level_values(1)

        branch_matrix['branch_in'] = branch_matrix['branch_in'].str.strip().str.upper()
        branch_matrix['branch_out'] = branch_matrix['branch_out'].str.strip().str.upper()
        locators = {
        col: input_matrix[col].astype(str).str.strip().str.upper()
        for col in input_matrix.columns
        if col not in ["varname", "out_unit", "out_unit_profile", "time_unit", "start_time", "end_time"]
        }
        
        for key, value in locators.items():
            input_branches = value.str.strip().str.upper()
        catalog_branches = set(df_catalog[key].str.strip().str.upper())
        
        # Check for branches in the branch_matrix that are not in the catalog or input matrix
        for branch in branch_matrix['branch_in'].unique():
            if branch not in catalog_branches:
                raise ValueError(f"Branch in '{branch}' in branch_matrix is not present in the catalog.")
            elif branch not in input_branches.unique():
                raise ValueError(f"Branch in '{branch}' in branch_matrix is not present in the input_matrix.")
        for branch in branch_matrix['branch_out'].unique():
            if branch not in catalog_branches:
                raise ValueError(f"Branch out '{branch}' in branch_matrix is not present in the catalog.")
            elif branch not in input_branches.unique():
                raise ValueError(f"Branch out '{branch}' in branch_matrix is not present in the input_matrix.")
        
        data_file = input_matrix
        data = branch_matrix
        first_branch = data["branch_in"]
        num_of_pipes = result_df[first_branch]
        #num = num_of_pipes.item()
        num = num_of_pipes.values.flatten()
        df_boundary = []
        df_section = []
        excluded_columns = {'Variable', 'Units', 'Locator Type', 'Description'}

# Get all columns to be used as locators dynamically
        locator_columns = [col for col in df_catalog.columns if col not in excluded_columns]
        for index, row in data.iterrows():
            branch_in = row['branch_in']
            branch_out = row['branch_out'] 
            variable_names = data_file['varname'].unique()
            for v in variable_names:
                match = df_catalog[
                    ((df_catalog['Variable'] == v) & (df_catalog[locator_columns].eq(branch_in).all(axis=1))) |
                    ((df_catalog['Variable'] == v) & (df_catalog[locator_columns].eq(branch_out).all(axis=1)))]
                match.reset_index(drop=True, inplace=True)
                if match.empty:
                    raise ValueError(f"No matching catalog entry found for branch_in '{branch_in}' or branch_out '{branch_out}' with variable '{v}'.")

                location =  match['Locator Type'].values[0]
    
                
                if location == "BOUNDARY:":
            
                    branch_in_cols = [col for col in data_df.columns if branch_in in col and v in col]
                    branch_out_cols = [col for col in data_df.columns if branch_out in col and v in col]
                    # Separating dataframe based on branch_in and Branch_out
                    # Identifying overlapping columns 
                    overlapping_cols = list(set(branch_in_cols) & set(branch_out_cols))
                    if not overlapping_cols:
                        branch_in_cols = [col for col in data_df.columns if branch_in in col and v in col]
                        branch_out_cols = [col for col in data_df.columns if branch_out in col and v in col] 
                        # Separating dataframe based on branch_in and Branch_out
                        # print(branch_in_cols)
                        df_branch_in = data_df[branch_in_cols]
                        df_branch_out = data_df[branch_out_cols]
                    else:
                        # Removing overlaps from one list and keeping them in the other
                        # Keeping overlapping columns in branch_in only
                        branch_in_cols = list(set(branch_in_cols))  # Deduplicate within each list
                        branch_out_cols = list(set(branch_out_cols) - set(overlapping_cols))
                        # Separating dataframe based on branch_in and branch_out
                        df_branch_in = data_df[branch_in_cols + overlapping_cols]  # Include overlaps here only once
                        df_branch_out = data_df[branch_out_cols]

                    def rename_columns(col):
                        profiles_match = re.match(r'Profiles_.*_(\w+)$', col)
                        if profiles_match:
                            return f'Profiles_{v}_{profiles_match.group(1)}'
                        
                        pattern = r"in_(.*?):"
                        match = re.search(pattern, col)
                        variable = match.group(1) 
                        m = re.search(rf"(time_in_{variable}:_\d+\.\d+_[^_]+(?:/[^_]+)?)", col)

                        if m:
                            return m.groups()[0]
                        return col  
                        
                    # Applying the renaming function to both columns of both branch_in and Branch_out
                    df_branch_in.columns = [rename_columns(col) for col in df_branch_in.columns]
                    df_branch_out.columns = [rename_columns(col) for col in df_branch_out.columns]
                    df_boundary.append(df_branch_in)
                    df_boundary.append(df_branch_out)
                    # print(df_boundary)
                    num_rows_to_process = [i+1 for i in num]
                    # print(len(num_rows_to_process))
                    combined_boundary_df = pd.concat(df_boundary)  
                    combined_boundary_df = combined_boundary_df.dropna()
                    prof = combined_boundary_df.filter(like="Profiles").copy()

                    for i in range(0, len(num_rows_to_process), 2):
                        start_index = num_rows_to_process[i]
                        step_count = num_rows_to_process[i + 1]
                        # print(step_count)
                        last_value = prof.iloc[start_index - 1] 
                        end_index = min(start_index + step_count, len(prof))
                        prof.iloc[start_index:end_index] += last_value 
                        last_value_added = prof.iloc[end_index - 1]
                        if end_index < len(prof):
                            prof.iloc[end_index:] += last_value_added
                    combined_boundary_df[prof.columns] = prof

                
                else:
                    branch_in_cols = [col for col in data_df.columns if branch_in in col and v in col]
                    branch_out_cols = [col for col in data_df.columns if branch_out in col and v in col]
                    # Separating dataframe based on branch_in and Branch_out
                    # Identifying overlapping columns 
                    overlapping_cols = list(set(branch_in_cols) & set(branch_out_cols))
                    if not overlapping_cols:
                        branch_in_cols = [col for col in data_df.columns if branch_in in col and v in col]
                        branch_out_cols = [col for col in data_df.columns if branch_out in col and v in col] 
                        # Separating dataframe based on branch_in and Branch_out
                        # print(branch_in_cols)
                        df_branch_in = data_df[branch_in_cols]
                        df_branch_out = data_df[branch_out_cols]
                    else:
                        # Removing overlaps from one list and keeping them in the other
                        # Keeping overlapping columns in branch_in only
                        branch_in_cols = list(set(branch_in_cols))  # Deduplicate within each list
                        branch_out_cols = list(set(branch_out_cols) - set(overlapping_cols))
                        # Separating dataframe based on branch_in and branch_out
                        df_branch_in = data_df[branch_in_cols + overlapping_cols]  # Include overlaps here only once
                        df_branch_out = data_df[branch_out_cols]
                    # Function to automate renaming based on regex patterns
                    def rename_columns(col):
                        profiles_match = re.match(r'Profiles_.*_(\w+)$', col)
                        if profiles_match:
                            return f'Profiles_{v}_{profiles_match.group(1)}'
                        
                        pattern = r"in_(.*?):"
                        # Search for the pattern in the text
                        match = re.search(pattern, col)
                        variable = match.group(1)
                        m = re.search(rf"(time_in_{variable}:_\d+\.\d+_[^_]+(?:/[^_]+)?)", col)
                        if m:
                            return m.groups()[0]
                        return col  
                        
                    # Applying the renaming function to both columns of both branch_in and Branch_out
                    df_branch_in.columns = [rename_columns(col) for col in df_branch_in.columns]
                    df_branch_out.columns = [rename_columns(col) for col in df_branch_out.columns]
                    df_section.append(df_branch_in)
                    df_section.append(df_branch_out)
                    
                    combined_section_df = pd.concat(df_section)   
                    combined_section_df = combined_section_df.drop_duplicates().dropna()
                    prof_section = combined_section_df.filter(like="Profiles").copy()
                    
                    for i in range(0, len(num), 2):
                        start_index = num[i]
                        step_count = num[i + 1]

                        last_value = prof_section.iloc[start_index - 1] 
                        end_index = min(start_index + step_count, len(prof_section))
                        prof_section.iloc[start_index:end_index] += last_value 
                        last_value_added = prof_section.iloc[end_index - 1]
                        if end_index < len(prof_section):
                            prof_section.iloc[end_index:] += last_value_added
                    combined_section_df[prof_section.columns] = prof_section

        if len(df_boundary) == 0:                
            combined_section_df = combined_section_df.reset_index(drop=True)
            return combined_section_df
        
        elif len(df_section) == 0:
            combined_boundary_df = combined_boundary_df.reset_index(drop=True)
            return combined_boundary_df
        
        else:
            combined_boundary_df = combined_boundary_df.reset_index(drop=True)
            combined_section_df = combined_section_df.reset_index(drop=True)
            max_len = max(len(combined_boundary_df), len(combined_section_df))

            combined_boundary_df = combined_boundary_df.reindex(range(max_len))
            combined_section_df = combined_section_df.reindex(range(max_len))

            final_df= pd.concat([combined_boundary_df,combined_section_df], axis=1, keys=variable_names, ignore_index=False)
        return final_df
            
    
        
class pplBatchParser:
    """
    Class to handle batches of ppl files
    
    Functions:
        1. extract_profiles: to extract profiles from a list of ppl files
        2. join_batch_nodes: to join nodes of branches extracted from a list of ppl files
    """


    def __init__(self, list_of_files):
        """
        Initializes an instance of the class by loading file data and unit definitions.
        
        Arguments:
            - filepaths (list): a list of the path to the ppl files to be loaded.
        Returns:
            - None
        """

        self.list_of_files = list_of_files
        self.files = [pplParser(file) for file in list_of_files]

    def extract_profiles(self, input_matrix):
        """
        Function to extract profiles from a batch of ppl files
        
        Arguments:
            - Input_matrix (pd.DataFrame): A matrix containing variable names, branch names, and pipe names. This is a required argument.

        Returns
            - pandas.DataFrame: DataFrame containing extracted profiles from ppl files
        """

        # create suffixes for distinguishing between columns
        suffixes = ["_" + str(os.path.basename(file)) for file in self.list_of_files]
        list_of_dfs = [file.extract_profile(input_matrix) for file in self.files]
        # attaching suffixes to dataframes
        for i in range(len(list_of_dfs)):
            list_of_dfs[i] = list_of_dfs[i].add_suffix(suffixes[i])
        # merging final dataframe
        final_df = reduce(
            lambda x, y: pd.merge(x, y, left_index=True, right_index=True, how="outer"),
            list_of_dfs,
        )
        return final_df

    def join_batch_nodes(self, input_matrix, branch_matrix):
        """
        Extracts and processes profiles data for branches, combining boundary and section data from a list of ppl files. 
        
        Arguments:
            - input_matrix (pd.DataFrame): The matrix containing trend data for various branches with columns ['branchname', 'varname', 'out_unit', 'out_unit_profile', 'time_unit']. 
            - branch_matrix (pd.DataFrame): The matrix containing information about branch connections with columns ['branch_in', 'branch_out']. 

        Returns: 
            - pandas.DataFrame: A combined DataFrame containing processed profiles data for the specified branches, including boundary and section data, with consistent units and profiles. 
        """

        # create suffixes for distinguishing between columns
        suffixes = ["_" + str(os.path.basename(file)) for file in self.list_of_files]
        list_of_dfs = [file.extract_profiles_join_nodes(input_matrix, branch_matrix) for file in self.files]
        # attaching suffixes to dataframes
        for i in range(len(list_of_dfs)):
            list_of_dfs[i] = list_of_dfs[i].add_suffix(suffixes[i])
        # merging final dataframe
        final_df = reduce(
            lambda x, y: pd.merge(x, y, left_index=True, right_index=True, how="outer"),
            list_of_dfs,
        )
        return final_df
           

if __name__ == "__main__":
    with cProfile.Profile() as profile:
        parser = argparse.ArgumentParser(
            description="parse arguments for obtaining variables from catalog"
        )

        parser.add_argument("-f", "--filepath", type=str, help="enter the path to tpl file")
        #parser.add_argument("-f", "--filepath", type=str,nargs='+', help="enter the path to tpl file")

        parser.add_argument("-v", "--varname", type=str, nargs='+',help="enter a valid variable name")
        parser.add_argument("-b", "--branchname", type=str,nargs='+', help="enter a valid branch name")
        parser.add_argument("-u", "--unitout", type=str, help="enter a valid unit")
        parser.add_argument("-pu", "--profileunit", type=str, help="enter a valid profiles unit")
        parser.add_argument("-tu", "--timeunit", type=str, help="enter a valid time unit")
        parser.add_argument(
            "-c",
            "--csv_file",
            type=str,
            help="Path to the CSV file containing variable names, branch names, and pipe names",
        )
        parser.add_argument(
            "-bm",
            "--branch_csv_file",
            type=str,
            help="Path to the CSV file containing  branch names to be sorted",
        )
        args = parser.parse_args()
        args.filepath = args.filepath.replace("\\", "/")
        #args.filepath = [fp.replace("\\", "/") for fp in args.filepath]

        input_matrix = pd.read_csv(args.csv_file)
        branch_matrix = pd.read_csv(args.branch_csv_file)
        # pplbatchparser = pplBatchParser(args.filepath)
        # trends = pplbatchparser.extract_trends(input_matrix)
        # nodes = pplbatchparser.Join_batch_nodes(input_matrix= input_matrix, branch_matrix=branch_matrix)
        # # print(trends)
        # branch_matrix = pd.read_csv(args.branch_csv_file)
        pplparser = pplParser(args.filepath)
        # time_series = pplparser._extract_time_series_data()
        # data = pplparser._extract_catalog()
        # data = pplparser.search_catalog(var_name="PT")
        # # trends = pplparser.extract_trend(var_name=args.varname)
        # profiles = pplparser._extract_branch_profiles(target_branch = args.varname)
        # data = pplparser.extract_profile(input_matrix=args.csv_file)
        data = pplparser.extract_profiles_join_nodes(input_matrix= input_matrix, branch_matrix=branch_matrix)
        print(data)
    # results = pstats.Stats(profile)
    # results.sort_stats(pstats.SortKey.TIME)
    # results.print_stats(20)