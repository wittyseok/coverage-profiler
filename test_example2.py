from test_pcov import *

def test_example2_statement():
    output = run_pcov("examples/example2.py", "10", "1")
    stmt_covered, stmt_total, stmt_missing, _, _, _ = get_coverage(output)
    assert stmt_covered == 6
    assert stmt_total == 8

def test_example2_statement_verbose():
    output = run_pcov_verbose("examples/example2.py", "10", "1")
    stmt_covered, stmt_total, stmt_missing, _, _, _ = get_coverage(output)
    assert stmt_covered == 6
    assert stmt_total == 8
    assert {7, 11} == set(stmt_missing)

def test_example2_branch():
    output = run_pcov("examples/example2.py", "10", "1")
    _, _, _, branch_covered, branch_total, branch_missing = get_coverage(output)
    assert branch_covered == 2
    assert branch_total == 4

def test_example2_branch_verbose():
    output = run_pcov_verbose("examples/example2.py", "10", "1")
    _, _, _, branch_covered, branch_total, branch_missing = get_coverage(output)
    assert branch_covered == 2
    assert branch_total == 4
    assert {"6->7", "8->11"} == set(branch_missing)

