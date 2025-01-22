# Download the new version:
## Go to https://github.com/Pontem-Analytics/PyPontem
- Press tags
- Download the latest version
- Extract to working folder
- Open the Anaconda promt

- to view the list of all your environments

    ```sh
    conda conda env list
    ```

- next, delete the previous pypontem version

    ```sh
    conda env remove -n pypontem
    ```
- next, navigate to your extracted pypontem folder and copy the path and paste it  

    ```sh
    conda filepath 
    ```

- next, navigate to the directory where environment is located

    ```sh
    conda env create -f environment.yml
    ```

- next, activate pypontem environment

    ```sh
    conda activate pypontem
    ```

- then, add the xlwings addin in the pypontem environment created

    ```sh
    conda xlwings addin install
    ```
- In the UDF Module box,  where we now have `tpl.xlwings_parser`put a semicolon `;` and paste `ppl.xlwings_parser`.
- Click import functions to load the script.
- The `pplparser` and `tplparser` functionalities should now be available to use within excel as functions.
