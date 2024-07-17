from test_pcov import *

def test_example1_statement():
    output = run_pcov("examples/example1.py")
    stmt_covered, stmt_total, stmt_missing, _, _, _ = get_coverage(output)
    assert stmt_covered == 3
    assert stmt_total == 3
    assert len(stmt_missing) == 0

def test_example1_statement_verbose():
    output = run_pcov_verbose("examples/example1.py")
    stmt_covered, stmt_total, stmt_missing, _, _, _ = get_coverage(output)
    assert stmt_covered == 3
    assert stmt_total == 3
    assert len(stmt_missing) == 0

def test_example1_branch():
    output = run_pcov("examples/example1.py")
    _, _, _, branch_covered, branch_total, branch_missing = get_coverage(output)
    assert branch_covered == 1
    assert branch_total == 2

def test_example1_branch_verbose():
    output = run_pcov_verbose("examples/example1.py")
    _, _, _, branch_covered, branch_total, branch_missing = get_coverage(output)
    assert branch_covered == 1
    assert branch_total == 2
    assert set(branch_missing) == {"3->-1"}