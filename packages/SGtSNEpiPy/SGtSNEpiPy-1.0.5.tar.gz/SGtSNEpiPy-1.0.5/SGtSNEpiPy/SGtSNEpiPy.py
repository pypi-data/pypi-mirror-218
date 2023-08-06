from juliacall import Main as jl
import scipy.sparse as sp
import numpy as np

# This function uses julia package SGtSNEpi within Python to process a sparse array in python
# input of the function can be any type of sparse array, namely COO,CSR or CSC
# If this function does not operate normally, find which path your downloaded juliacall, then use the corresopongding python interepter 
# We use the Conda package manager

def sgtsnepipy(CSR_matrix):
    jl.seval('using Pkg')
    jl.seval('Pkg.add("SGtSNEpi")')
    jl.seval('Pkg.status()') 
    jl.seval("using SparseArrays")
    jl.seval("using SGtSNEpi")

    row,column,value = sp.find(CSR_matrix)
    row = [x + 1 for x in row]
    column = [y + 1 for y in column]
    row_array = jl.Array(row)
    column_array = jl.Array(column)
    value_array = jl.Array(value)
    m,n = CSR_matrix.shape
    result_py = jl.SparseArrays.sparse(row_array,column_array,value_array,m,n)
    jl.result_jl = jl.sgtsnepi(result_py)
    result_py = np.array(jl.result_jl,dtype = np.float64)
    result_list = result_py.tolist()

    return result_list