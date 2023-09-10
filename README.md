
# Biomass_Prediction

This program (Solution.py) takes forecasted values from Solution3.csv and uses genetic algorithm to predict the best possible placements for Refineries and Depots based on given Distance Matrix. 

The forecasted values of year 2018-19 in Solution3.csv are based on the data given in Biomass_History.csv. The forecasting part was done by my partner.

## How to run it:
The program only needs 2 python libraries to run i.e. Numpy and Pandas.

To install these libraries run this command in the terminal:

```terminal
pip install numpy pandas
```

You would also need to download _Biomass_History.csv, solution3.csv, Distance_Matrix.csv_ from [here](https://drive.google.com/drive/folders/1we520Wx2HUydIVXW_Lxrfdk_13jE7epq?usp=sharing)

>*Make sure to have all the files in the same folder*

### Test.py
This file is used to genrate a _solution.csv_ in the format appropriate for uploading as the final solution in the hackathon. you would need to copy the locations genrated by _Solution.py_ and paste in the ``soln`` variable before running the file.
