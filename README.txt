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