from juliacall import Main as jl

cmd = 'import Pkg;' + 'Pkg.add("HMatrices");' + 'using HMatrices;'
jl.seval(cmd)

hmatrices_jl = jl.HMatrices


