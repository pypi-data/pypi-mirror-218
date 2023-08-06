import pandas as pd
from datasets import Dataset, concatenate_datasets
import pyarrow as pa
import pyarrow.parquet as pq
from tqdm import tqdm
from ntpath import basename
import os
import json
from typing import Callable

def get_file_type(file_path):
    _, file_extension = os.path.splitext(file_path)
    return file_extension[1:].lower()  # Remove the dot and convert to lowercase

def get_all_files(directory):
    """
    Get a list of all files from all directories within the specified directory.

    Args:
        directory (str): The directory containing multiple directories.

    Returns:
        list: A list of file paths from all directories within the specified directory.
    """
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list

def get_remaining_files(read_directory, write_directory):
    """
    For resuming an incomplete process. Get a list of files in the
    read directory that are absent from the write directory.

    Args:
        read_directory: Source of datasets to be processed.
        write_directory: Destination of datasets to be processed.

    Returns:
        list: A list of file paths to be processed.
    """
    read_files = get_all_files(read_directory)
    write_files = get_all_files(write_directory)
    
    base = lambda file_path: basename(file_path).split(".")[0]

    remaining_files = [file for file in read_files if base(file) not in [base(file2) for file2 in write_files]]
    return remaining_files

def get_smallest_files(file_paths, num_files=1):
    """
    Given a batch of files, return n files with the smallest file size.
    """
    smallest_files = []

    for file_path in file_paths:
        file_size = os.path.getsize(file_path)

        if len(smallest_files) < num_files:
            smallest_files.append((file_path, file_size))
            smallest_files.sort(key=lambda x: x[1])
        else:
            smallest_files.sort(key=lambda x: x[1], reverse=True)

            if file_size < smallest_files[0][1]:
                smallest_files[0] = (file_path, file_size)
                smallest_files.sort(key=lambda x: x[1])

    return [file_path for file_path, _ in smallest_files]

def load_parquet(file_path: str, output_type: str = "pd", columns=None):
    """
    Load a data structure of the selected type from a parquet file.

    Args:
        file_path (str): Path to the parquet file.
        output_type (str, defaults to "pd"): Type of the output data structure. Either "pd" for pandas DataFrame or "Dataset" for custom Dataset.
        columns (str or list, optional): Columns to load. If provided, only load the specified columns.

    Returns:
        object: Loaded data structure.
    """
    if output_type == "pd":
        if columns:
            dataset = pd.read_parquet(file_path, columns=columns)
        else:
            dataset = pd.read_parquet(file_path)
    elif output_type == "Dataset":
        if columns:
            table = pq.read_table(file_path, columns=columns)
        else:
            table = pq.read_table(file_path)
        dataset = Dataset(table)
    else:
        raise ValueError("Please input a valid output type. Either 'pd' or 'Dataset'.")

    return dataset

def load_dataset(file_path: str, output_type: str = "pd", columns=None, masks=None):
    """
    Load a data structure of the selected type from a parquet file and apply optional masking.

    Args:
        file_path (str): Path to the parquet file.
        output_type (str, defaults to "pd"): Type of the output data structure. Either "pd" for pandas DataFrame or "Dataset" for custom Dataset.
        columns (str or list, optional): Columns to load. If provided, only load the specified columns.
        masks (str or list, optional): Mask column(s) to apply and remove rows where the mask is True.

    Returns:
        object: Loaded data structure.
    """
    dataset = load_parquet(file_path, output_type, columns)

    if masks is not None:
        if isinstance(masks, str):
            masks = [masks]
        
        if output_type == "pd":
            for mask in masks:
                dataset = dataset[~dataset[mask]]
        elif output_type == "Dataset":
            for mask in masks:
                dataset = dataset.filter(~dataset[mask])
        else:
            raise ValueError("Please input a valid output type. Either 'pd' or 'Dataset'.")

    return dataset

import pandas as pd
import pyarrow.parquet as pq

def concat_dataset(file_paths, output_type="pd", columns=None, masks=None):
    """
    Concatenate multiple datasets from parquet files and apply optional masking.

    Args:
        file_paths (list[str]): Paths to the parquet files.
        output_type (str, defaults to "pd"): Type of the output data structure. Either "pd" for pandas DataFrame or "Dataset" for custom Dataset.
        columns (str or list[str], optional): Columns to load. If provided, only load the specified columns.
        masks (str or list[str], optional): Mask column(s) to apply and remove rows where the mask is True.

    Returns:
        object: Concatenated and optionally masked data structure.
    """
    datasets = []
    
    for file_path in tqdm(file_paths, desc = "Loading dataset"):
        dataset = load_parquet(file_path, output_type, columns)
        datasets.append(dataset)
    
    concatenated = pd.concat(datasets) if output_type == "pd" else datasets[0].concatenate(datasets[1:])
    
    if masks is not None:
        if isinstance(masks, str):
            masks = [masks]
        
        if output_type == "pd":
            for mask in masks:
                concatenated = concatenated[~concatenated[mask]]
        elif output_type == "Dataset":
            for mask in masks:
                concatenated = concatenated.filter(~concatenated[mask])
        else:
            raise ValueError("Please input a valid output type. Either 'pd' or 'Dataset'.")
    
    return concatenated

def get_output_path(file_path:str, output_dir:str, file_type:str=""):
    """
    Generate a new file path for transforming data from one filetype to another.

    Given the original file path and the destination folder, generate a new file path
    with the destination folder and the specified file type.

    Args:
        file_path (str): The original file path.
        output_dir (str): The destination folder where the transformed file will be saved.
        file_type (str, Optional): The desired file type for the transformed file.

    Returns:
        str: The new file path with the destination folder and file type.
    """
    if file_type:
        file = basename(file_path).split(".")[0]
        ouput_path = f"{output_dir}/{file}.{file_type}"
    else:
        file = basename(file_path)
        ouput_path = f"{output_dir}/{file}"
    return ouput_path

def save_to_parquet(data, file_path):
    if isinstance(data, pd.DataFrame):
        data.to_parquet(file_path)
    elif isinstance(data, Dataset):
        data_frame = pd.DataFrame(data)
        data_frame.to_parquet(file_path)
    else:
        raise ValueError("Data must be either a pd.DataFrame or a HuggingFace Dataset.")
    
def save_dict(dict:dict, save_path: str):
    """
    Save a dictionary to the JSON file format.

    Args:
        dict (dict): Dictionary to be saved.
        save_path (str): Path where the JSON file will be saved.
    """
    with open(save_path, 'w', encoding="utf-8") as f:
        json.dump(dict, f, ensure_ascii=False, indent=2)
        return
    
def load_dict(path_to_dict):
    with open(path_to_dict, "r", encoding="utf-8") as f:
        return json.load(f)

    
def mod_column(dataset: Dataset, column: str, function: Callable):
    """
    Modify a column in a HuggingFace dataset with a specified function.

    Args:
        dataset (Dataset): Dataset to modify.
        column (str): Column in the dataset to modify.
        function (Callable): Function with which to modify elements in the column.
    """

    def modify(example):
        example[column] = function(example[column])
        return example

    new_dataset = dataset.map(modify)
    return new_dataset




