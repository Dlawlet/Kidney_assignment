How to use: 

the project has 3 main files:
1. solve_kidney_exchange.py - this file contains the main algorithm to solve the kidney exchange problem
2. draw_donation_cycle.py - conttain functions to draw cycle 
3. kidney_functions.py - contain functions needed to run the algorithm in solve_kidney_exchange.py
4. Project_NOTEBOOK.ipynb - this is a notebook that contains call to  solve_kidney_exchange.py and draw_donation_cycle.py 
    * IN case of error restart the kernel and clear all output and run all cells again
    * Note : the notebook is not needed to run the algorithm, it is just a way to visualize the results and goes with the report. 



Instance Structure

First line is of the form

    n;m;M

where
    n is the number of patient-donor pairs (p_i, d_i),
    m is the  number of compatibilities (d_i, p_j),
    M is the maximum number of exchanges per cycle of transplants.

The remaining lines indicate the compatibility matrix and are of the form

    i;j;c

where
    i is the index of the donor d_i,
    j is the index of the patient p_j,
    c is the compatibility corresponding to the exchange (d_i, p_j).

NB: All indices start at 0.