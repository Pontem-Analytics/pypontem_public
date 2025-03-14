"""
TPL parser functionality
"""

import warnings

# temporary to remove pandas 3.0 deprecationwarning about pyarrow from printing
warnings.filterwarnings("ignore", category=DeprecationWarning)

import pandas as pd
import argparse
import re
from functools import reduce
from pathlib import Path
import os
import sys
import math
import yaml


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
        filter_conditions.append(df["varname"].str.upper() == var_name.upper())
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
    #     additional_filters = [col for col in result_df.columns if col not in locator_types and col != "varname" and col != "out_unit" and col != "Description"]
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


class tplParser:
    """
    Class which holds the tpl parser functions

    Functions:
        1. metadata: to extract metadata from a tpl file
        2. branch_names: to extract branch names from a tpl file
        3. branch_profiles: to extract branch profile information from a tpl file
        4. parse_number_of_variables: to extract the number of variables present in a tpl file
        5. extract_catalog: to extract the catalog information from a tpl file
        6. search_catalog: to extract the information from the catalog of the variable specified
        7. extract_trend: to extract trends in a tpl file
        8. calc_average: to compute the average of trends extracted in a tpl file	
    """


    def __init__(self, filepath):
        """
        Initializes an instance of the class by loading file data and unit definitions.
        Arguments:
            - filepath (str): The path to the file to be loaded.
        Returns:
            - None
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
        
        Parameters:
        - None
        
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
        Extracts branch names from the content stored in the object.
        
        Arguments:
            - None.
        
        Returns:
            - list: A list of extracted branch names as strings.
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
            - None.
        
        Returns:
            - Pandas.Dataframe: a dataframe containing the profiles of the specified branch.
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
            - pandas.DataFrame: A DataFrame containing the extracted variable information.
        """

        return self._extract_catalog()

    def _extract_catalog(self):
        pattern = re.compile(
            r"""
            (?P<varname>\S+)        # Variable name (A, B, C, etc.)
            \s*(?:'BOUNDARY:'|'SECTION:')?
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
                    "varname": match.group("varname"),
                    "out_unit": match.group("unit"),
                    "Description": match.group("description")
                }

                # Capture and process locator types
                locator_type = match.group("locator_type")
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
        
        # Define the final column order (varname, locator_types, extras, out_unit, description)
        # First column is 'varname', last two are 'out_unit' and 'Description', the rest are dynamic locators and extras.
        final_columns = ["varname"] + [col for col in df.columns if col not in ["varname", "out_unit", "Description"]] + ["out_unit", "Description"]

        # Rearrange the columns in the DataFrame
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
            
            return result_df

    def extract_trend(self, input_matrix: pd.DataFrame):
        """
        Extract trends dynamically based on user-specified variable names, locator types, and positions.

        Arguments:
            - input_matrix (pd.DataFrame): The matrix containing variable names, locator types (e.g., Choke, Position), 
            output units, and time units.

        Returns:
            - pandas.DataFrame: A DataFrame containing extracted trend data.
        """
        self.time, self.trends, self.time_unit = self._extract_time_series_data()
        self.trends.reset_index(drop=True, inplace=True)
        df = pd.concat([self._extract_catalog(), self.trends], axis=1)
        result_dfs = []
        
        for _, row in input_matrix.iterrows():
            var_name = row["varname"]
            if not isinstance(var_name, str):
                raise ValueError(f"No variable name specified in row {_ + 1}")
            
            out_unit = row.get("out_unit", None)
            time_unit = row.get("time_unit", None)
            # Identify which locator type is specified
            locators = {col: row[col] for col in input_matrix.columns if col not in ["varname", "out_unit", "time_unit"]}
            locators = {key: value for key, value in locators.items() if pd.notna(value)}  # Remove None values
            if not locators:
                raise ValueError(f"No locator specified for variable '{var_name}' in row {_ + 1}")
            search_args = {"var_name": var_name, **locators}
            result_df = search(df, **search_args) if search_args else pd.DataFrame()
            if result_df.empty:
                raise ValueError(f"No data found for variable '{var_name}' with locators {list(locators.keys())}")
            elif len(result_df) > 1:
                additional_filters = [col for col in result_df.columns if col not in locators and col != "varname" and col != "out_unit" and col != "Description" and col != "variable_output"]
                if additional_filters:
                    raise ValueError(
                        f"Multiple results found for variable '{var_name}'. "
                        f"Consider adding one of the following filters to refine the search: {additional_filters}"
                    )
                else:
                    raise ValueError(
                        f"Multiple results found for variable '{var_name}', but no additional filtering columns are available."
                    )
            
            for _, result_row in result_df.iterrows():
                unit = result_row["out_unit"].replace("(", "").replace(")", "").lower()
                if "-" in unit:
                    unit = unit.replace("-", "")
                if pd.isna(out_unit):
                    unit = unit.replace("/", "_")
                    out_unit = unit
                
                var = result_row["varname"]
                unit_class = self.unitsdb["OLGA_vars"].get(var)
                
                if unit_class is None:
                    for k, v in self.unitsdb["OLGA_startswith"].items():
                        if str(var).startswith(k):
                            unit_class = v
                
                variable_outputs = result_row.filter(like="variable_output").dropna()
                locator_str = "_".join([f"{key}_{value}" for key, value in locators.items()])
                heading = f"{var}_{unit}_{locator_str}" if locator_str else f"{var}_{unit}"

                if pd.isna(time_unit):
                    time_unit = self.time_unit
                    self.time = [round(value, 4) for value in self.time]
                elif pd.notna(time_unit) and self.time_unit in unit_map:
                    self.time = list(dict.fromkeys(self.time))
                    self.time_unit = unit_map[self.time_unit]
                    value_tagged = getattr(UnitConversion, "Time")(self.time, self.time_unit)
                    values = value_tagged.convert(to_unit=time_unit)
                    self.time = [round(value, 2) for value in values] if time_unit in ["hour", "minute", "second", "min", "s", "h"] else values
                # else:
                #     time_unit = self.time_unit 
                data = {
                    f"Time_({str(time_unit).lower()})": self.time,
                    heading: variable_outputs,
                }
                trend_df = pd.DataFrame(data)
                trend_df.set_index(f"Time_({str(time_unit).lower()})", inplace=True)

                converted_vals = []
                for _, row in trend_df.iterrows():
                    value = row[heading]
                    value_tagged = getattr(UnitConversion, unit_class)(value, unit)
                    conv_val = value_tagged.convert(to_unit=out_unit)
                    converted_vals.append(round(conv_val, 3))
                
                trend_df.drop(columns=trend_df.columns, inplace=True)
                trend_df[str(heading).replace(str(unit), str(out_unit))] = converted_vals
                result_dfs.append(trend_df)

        if result_dfs:
            return pd.concat(result_dfs, axis=1)
            
        else:
            print("No data found.")
            return None

    def calc_average(
        self,
        input_matrix: pd.DataFrame,
        start_index=None,
        end_index=None,
        n_rows=None,
        n_timeunits=None,
    ):
        """
        Calculate the average of values in the DataFrame between the specified start and end indices.
        
        Arguments:
            - input_matrix (pd.DataFrame): The matrix containing variable names, branch names, and pipe names. This is a required argument
            - start_index (int, optional): The starting index from which the average will be calculated. Defaults to None.
            - end_index (int, optional): The ending index up to which the average will be calculated. Defaults to None.
            - n_rows (int, optional): Number of rows to consider for calculating the average. If provided, start_index and end_index are ignored. Defaults to None.
        
        Returns:
            - pandas.DataFrame: DataFrame containing the calculated averages.
        """

        data_df = self.extract_trend(input_matrix)

        if start_index is not None and end_index is not None:
            # Calculate the average between start_index and end_index
            if (
                start_index >= 0
                and end_index >= 0
                and start_index <= end_index < len(data_df)
            ):
                sliced_df = data_df.iloc[start_index - 1 : end_index]
                average = sliced_df.mean()
                return average
            else:
                raise ValueError("One of the indices is out of range")

        elif n_rows is not None:
            # Calculate the average of number of rows specified
            length = len(data_df)

            if n_rows >= 0:
                if n_rows >= length:
                    raise ValueError("Index out of range.")
                sliced_df = data_df.iloc[:n_rows]
                average = sliced_df.mean()
            else:
                n_rows = abs(n_rows)
                if n_rows > length:
                    raise ValueError("Number of rows exceeds DataFrame length.")
                last_n_values = data_df.iloc[-n_rows:]
                average = last_n_values.mean()
            return average

        elif n_timeunits is not None:

            def hours_to_seconds(hours):
                return hours * 3600

            def hours_to_minutes(hours):
                return hours * 60

            def hours_to_hours(hours):
                return hours

            def hours_to_days(hours):
                return hours / 24

            def hours_to_weeks(hours):
                return hours / 168

            def hours_to_months(hours):
                return hours / 730

            def hours_to_years(hours):
                return hours / 8760

            if n_timeunits >= 0:
                if "second" in data_df.index.name or "s" in data_df.index.name:
                    sliced_df = data_df.loc[
                        data_df.index <= hours_to_seconds(n_timeunits)
                    ]
                elif "minute" in data_df.index.name or "min" in data_df.index.name:
                    sliced_df = data_df.loc[
                        data_df.index <= hours_to_minutes(n_timeunits)
                    ]
                elif "hour" in data_df.index.name or "h" in data_df.index.name:
                    sliced_df = data_df.loc[
                        data_df.index <= hours_to_hours(n_timeunits)
                    ]
                elif "day" in data_df.index.name or "d" in data_df.index.name:
                    sliced_df = data_df.loc[data_df.index <= hours_to_days(n_timeunits)]
                elif "week" in data_df.index.name or "w" in data_df.index.name:
                    sliced_df = data_df.loc[
                        data_df.index <= hours_to_weeks(n_timeunits)
                    ]
                elif "month" in data_df.index.name or "m" in data_df.index.name:
                    sliced_df = data_df.loc[
                        data_df.index <= hours_to_months(n_timeunits)
                    ]
                elif "year" in data_df.index.name or "y" in data_df.index.name:
                    sliced_df = data_df.loc[
                        data_df.index <= hours_to_years(n_timeunits)
                    ]
                average = sliced_df.mean()

            elif n_timeunits < 0:
                total_hours = data_df.index[-1]
                end_hour = total_hours
                if "second" in data_df.index.name or "s" in data_df.index.name:
                    start_hour = total_hours + hours_to_seconds(n_timeunits)
                elif "minute" in data_df.index.name or "min" in data_df.index.name:
                    start_hour = total_hours + hours_to_minutes(n_timeunits)
                elif "hour" in data_df.index.name or "h" in data_df.index.name:
                    start_hour = total_hours + hours_to_hours(n_timeunits)
                elif "day" in data_df.index.name or "d" in data_df.index.name:
                    start_hour = total_hours + hours_to_days(n_timeunits)
                elif "week" in data_df.index.name or "w" in data_df.index.name:
                    start_hour = total_hours + hours_to_weeks(n_timeunits)
                elif "month" in data_df.index.name or "m" in data_df.index.name:
                    start_hour = total_hours + hours_to_months(n_timeunits)
                elif "year" in data_df.index.name or "y" in data_df.index.name:
                    start_hour = total_hours + hours_to_years(n_timeunits)

                sliced_df = data_df.loc[
                    (data_df.index >= start_hour) & (data_df.index <= end_hour)
                ]
                average = sliced_df.mean()

            else:
                raise ValueError("Invalid value for n_timeunits.")
            return average
        else:
            raise ValueError(
                "Invalid input provided. Please specify either start_index and end_index or n_rows along with input_matrix."
            )

    def _extract_time_series_data(self):
        """
        Process time series data from the tpl file.
        
        Arguments:
            - None
        
        Returns:
            - pandas.Series: Time information.
            - pandas.DataFrame: DataFrame containing time series variable outputs.
        """

        i = 0
        data = []
        time_series_header = None
        with open(self.filepath, "r") as file:
            for line in file:
                i += 1
                if "TIME SERIES" in line.strip():
                    match = re.search(r"TIME\sSERIES\s+'\s?\((\w)\)\s*'", line)
                    time_unit = match.group(1)
                    time_series_header = line.strip()
                elif time_series_header:
                    data.append(line.split())

        if data:
            time_unit = time_unit
            df_outputs = pd.DataFrame(data)
            df_outputs = df_outputs.T
            df_outputs = df_outputs.apply(pd.to_numeric)
            time = df_outputs.iloc[0]
            df_outputs = df_outputs.iloc[1:]
            df_outputs.columns = ["variable_output"] * len(df_outputs.columns)
            return time, df_outputs, time_unit
        else:
            return pd.Series(), pd.DataFrame()


class tplBatchParser:
    """
    Class to handle batches of tpl files
    
    Functions:
        1. extract_trends: to extract trends from a list of tpl files
        2. calc_averages: to compute averages of trends extracted from a list of tpl files
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
        self.files = [tplParser(file) for file in list_of_files]

    def extract_trends(self, input_matrix: pd.DataFrame):
        """
        Function to extract trends from a batch of tpl files
        
        Arguments:
            - Input_matrix (pd.DataFrame): The matrix containing variable names, branch names, and pipe names. This is a required argument
        
        Returns
            - pandas.DataFrame: DataFrame containing extracted trends from tpl files
        
        """

        # create suffixes for distinguishing between columns
        suffixes = ["_" + str(os.path.basename(file)) for file in self.list_of_files]
        list_of_dfs = [file.extract_trend(input_matrix) for file in self.files]
        # attaching suffixes to dataframes
        for i in range(len(list_of_dfs)):
            list_of_dfs[i] = list_of_dfs[i].add_suffix(suffixes[i])
        # merging final dataframe
        final_df = reduce(
            lambda x, y: pd.merge(x, y, left_index=True, right_index=True, how="outer"),
            list_of_dfs,
        )
        return final_df

    def calc_averages(
        self,
        input_matrix: pd.DataFrame,
        start_index=None,
        end_index=None,
        n_rows=None,
        n_timeunits=None,
    ):
        """
        Calculate the average of values in the DataFrame up to the specified index or of the last n values.

        Arguments:
            - input_matrix (pd.DataFrame): The matrix containing variable names, branch names, and pipe names. This is a required argument
            - start_index (int, optional): The starting index from which the average will be calculated. Defaults to None.
            - end_index (int, optional): The ending index up to which the average will be calculated. Defaults to None.
            - n_rows (int, optional): Number of rows to consider for calculating the average. If provided, start_index and end_index are ignored. Defaults to None.

        Returns:
            - pandas.DataFrame: DataFrame containing the calculated averages.
        """
        suffixes = ["_" + str(os.path.basename(file)) for file in self.list_of_files]
        list_of_dfs = [
            file.calc_average(input_matrix, start_index, end_index, n_rows, n_timeunits)
            .to_frame()
            .T
            for file in self.files
        ]
        for i in range(len(list_of_dfs)):
            list_of_dfs[i] = list_of_dfs[i].add_suffix(suffixes[i])

        final_df = reduce(
            lambda x, y: pd.merge(x, y, left_index=True, right_index=True, how="outer"),
            list_of_dfs,
        )
        final_df = final_df.T
        final_df.columns = ["Average"]
        return final_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="parse arguments for obtaining variables from catalog"
    )

    parser.add_argument("-f", "--filepath", type=str, help="enter the path to tpl file")
    parser.add_argument(
        "-v",
        "--varname",
        type=str,
        help="enter the name of the tpl variable",
        required=False,
        default=None,
    )
    parser.add_argument(
        "-l",
        "--loc",
        type=str,
        help="enter the name of the tpl branch",
        required=False,
        default=None,  # to ensure all variable time series output is pulled if no branch is provided
    )
    parser.add_argument(
        "-p",
        "--pipe",
        type=str,
        help="enter the name of the tpl pipe",
        required=False,
        default=None,  # to ensure all variable time series output is pulled if no pipe is provided
    )

    parser.add_argument(
        "-is",
        "--start_index",
        type=int,
        help="enter the start index to calculate average for trend",
        required=False,
        default=None,
    )
    parser.add_argument(
        "-ie",
        "--end_index",
        type=int,
        help="enter the last index to calculate average for trend",
        required=False,
        default=None,
    )
    parser.add_argument(
        "-n",
        "--n_rows",
        type=int,
        help="enter the number of rows to calculate average for trend",
        required=False,
        default=None,
    )
    parser.add_argument(
        "-nt",
        "--n_timeunits",
        type=int,
        help="enter the number of hours to calculate average for trend",
        required=False,
        default=None,
    )

    parser.add_argument(
        "-c",
        "--csv_file",
        type=str,
        help="Path to the CSV file containing variable names, branch names, and pipe names",
    )

    args = parser.parse_args()
    args.filepath = args.filepath.replace("\\", "/")
    tplparser = tplParser(args.filepath)
    input_matrix = pd.read_csv(args.csv_file)
    data = tplparser.extract_trend(input_matrix)
    # data1 = tplparser.calc_average(
    #     input_matrix=input_matrix, n_timeunits=args.n_timeunits
    # )
    # data = tplparser.search_catalog(var_name="PT")
    print(data.head())
