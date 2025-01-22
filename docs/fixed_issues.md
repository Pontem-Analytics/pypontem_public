# PyPontem Release Log

## Version 0.2

- `Tplparser not recognizing Annulus Branch`: fixed, now the library generates outputs from Annulus branch just fine.

- `Metadata trim PVT file relative path`:The tplparser is reading what's in the tpl file, it doesn't trim an absolute path to make it relative. It also doesn't read a full folder structure to convert a relative path to absolute. If you use an absolute path in the genkey/inp/key file, it will give you the absolute path.

- `Metadata not showing OLGA version for certain TPL file`: The codes were modified now for any tpl file you can run you get full metadata.

- `Variables in lowercase and uppercase letters`: Among the issues raised there was this one that claimed that functions did not work if variables were written in lowercase letters. Now you can either write your variable names or locations in either small or capital letters.
`Attention`: when specifying the unit which your variable is to be outputted (out_units) you can not use capital letters. The units are strictly written in small letters. please consult (PyPontem\docs\units_tested_logbook.csv) to read more about each variable's supported unit and how we write them in our script.

- `csv file for variable prompts`: Now to run our script you do not need to write each variable with its location and other required entries individually. Instead you now write all variables you want to run in a csv file that you pass to the script to extract necessary data.

- `Custom variable unit`: Now you can get your variable data in a unit of your choice. If in the file we have temperature in celsius you can choose to get it in kelvin or rankine, all you have to do is add an (out_unit)column in your csv file and you specify which unit will be outputted.

- `Time output Units`: Our enhancements did not leave out time outputs. As you know time is the index to all other variable trends, now you can choose to have time in either days,seconds, minutes, hours ...,all you need is to add a (time_unit) column in your csv file and specify your output. 
`Attention:` The specified time_unit have to be the same for all your variables, you can not say you get time in seconds for one and another in hours. It has to be either seconds or hours for all.

- `Average calculation` :On cal_average function we made it more flexible for you. 
1. You can now calculate average for certain number of rows by adding an argument (-n) on your terminal and either you put positive or negative number of rows. If you put positive it will be the first number of rows and if it is negative it will be the last number of rows.
2. You can also calculate average for x number of hours by adding argument(-nt) on your terminal with all other arguments. If you add positive x hours it will calculate average for those first hours and if it is negative the average will be for the last specified hours.
3. Apart from those two you can also calculate average by specifying start and end index for targeted values in your data set.  You simply add (-is) and (-ie) arguments on your terminal together with other arguments.

- `Rows number specification in trends`: For extract_trends function you can specify the number of rows to be outputted and opt not to get the whole data set outputted. all you have to do is add (row_number) column in your csv file. Positive number of rows means you get the first specified number and negative simply means you get the last inputted number of rows.

## Xlwings

- `Allowing to run multiple functions in one cell in xlwings`: Unfortunately it seems this is a limitation with the xlwings library where after a successful execution of a function you can't change the argument.

- `Global variables not working`: now working fine, you can extract trends of Global variables.

- `Branch profile function`: fixed, now you can use string arguments and string with single or double quotation.