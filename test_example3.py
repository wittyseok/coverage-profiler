from test_pcov import *

def test_example3_statement_1():
    output = run_pcov("examples/example3.py", "1")
    stmt_covered, stmt_total, stmt_missing, _, _, _ = get_coverage(output)
    assert stmt_covered == 4
    assert stmt_total == 4

def test_example3_statement_1_verbose():
    output = run_pcov_verbose("examples/example3.py", "1")
    stmt_covered, stmt_total, stmt_missing, _, _, _ = get_coverage(output)
    assert stmt_covered == 4
    assert stmt_total == 4
    assert len(stmt_missing) == 0

def test_example3_statement_2():
    output = run_pcov("examples/example3.py", "0")
    stmt_covered, stmt_total, stmt_missing, _, _, _ = get_coverage(output)
    assert stmt_covered == 2
    assert stmt_total == 4

def test_example3_statement_2_verbose():
    output = run_pcov_verbose("examples/example3.py", "0")
    stmt_covered, stmt_total, stmt_missing, _, _, _ = get_coverage(output)
    assert stmt_covered == 2
    assert stmt_total == 4
    assert set(stmt_missing) == {4, 5}

def test_example3_branch_1():
    output = run_pcov("examples/example3.py", "1")
    _, _, _, branch_covered, branch_total, branch_missing = get_coverage(output)
    assert branch_covered == 3
    assert branch_total == 4

def test_example3_branch_1_verbose():
    output = run_pcov_verbose("examples/example3.py", "1")
    _, _, _, branch_covered, branch_total, branch_missing = get_coverage(output)
    assert branch_covered == 3
    assert branch_total == 4
    assert branch_missing == {"4->3"}

def test_example3_branch_2():
    output = run_pcov("examples/example3.py", "0")
    _, _, _, branch_covered, branch_total, branch_missing = get_coverage(output)
    assert branch_covered == 1
    assert branch_total == 4

def test_example3_branch_2_verbose():
    output = run_pcov_verbose("examples/example3.py", "0")
    _, _, _, branch_covered, branch_total, branch_missing = get_coverage(output)
    assert branch_covered == 1
    assert branch_total == 4
    assert set(branch_missing) == {'3->4', '4->3', '4->5'}

