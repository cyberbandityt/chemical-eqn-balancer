#</> by Ayush (cyber bandit)
import sympy
import re

ELEMENT_CLAUSE = re.compile("([A-Z][a-z]?)([0-9]*)")

def parse_compound(compound):
    """
    Given a chemical compound like Na2SO4,
    return a dict of element counts like {"Na":2, "S":1, "O":4}
    """
    assert "(" not in compound, "This parser doesn't grok subclauses"
    return {el: (int(num) if num else 1) for el, num in ELEMENT_CLAUSE.findall(compound)}

def main():
    print("\nPlease enter left-hand list of compounds, separated by spaces:")
    lhs_strings = input().split()
    lhs_compounds = [parse_compound(compound) for compound in lhs_strings]

    print("\nPlease enter right-hand list of compounds, separated by spaces:")
    rhs_strings = input().split()
    rhs_compounds = [parse_compound(compound) for compound in rhs_strings]

    # Get canonical list of elements
    els = sorted(set().union(*lhs_compounds, *rhs_compounds))
    els_index = dict(zip(els, range(len(els))))

    # Build matrix to solve
    w = len(lhs_compounds) + len(rhs_compounds)
    h = len(els)
    A = [[0] * w for _ in range(h)]
    # load with element coefficients
    for col, compound in enumerate(lhs_compounds):
        for el, num in compound.items():
            row = els_index[el]
            A[row][col] = num
    for col, compound in enumerate(rhs_compounds, len(lhs_compounds)):
        for el, num in compound.items():
            row = els_index[el]
            A[row][col] = -num   # invert coefficients for RHS

    # Solve using Sympy for absolute-precision math
    A = sympy.Matrix(A)    
    # find first basis vector == primary solution
    coeffs = A.nullspace()[0]    
    # find least common denominator, multiply through to convert to integer solution
    coeffs *= sympy.lcm([term.q for term in coeffs])

    # Display result
    lhs = " + ".join(["{} {}".format(coeffs[i], s) for i, s in enumerate(lhs_strings)])
    rhs = " + ".join(["{} {}".format(coeffs[i], s) for i, s in enumerate(rhs_strings, len(lhs_strings))])
    print("\nBalanced solution:")
    print("{} -> {}".format(lhs, rhs))

if __name__ == "__main__":
    main()
