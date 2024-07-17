from test_pcov import *

def test_example5_statement_1():
    output = run_pcov("examples/example5.py", "1")
    stmt_covered, stmt_total, stmt_missing, _, _, _ = get_coverage(output)
    assert stmt_covered == 11
    assert stmt_total == 14

def test_example5_statement_verbose_1():
    output = run_pcov_verbose("examples/example5.py", "1")
    stmt_covered, stmt_total, stmt_missing, _, _, _ = get_coverage(output)
    assert stmt_covered == 11
    assert stmt_total == 14
    assert stmt_missing == {7, 11, 13}

def test_example5_branch_1():
    output = run_pcov("examples/example5.py", "1")
    _, _, _, branch_covered, branch_total, branch_missing = get_coverage(output)
    assert branch_covered == 3
    assert branch_total == 6

def test_example5_branch_verbose_1():
    output = run_pcov_verbose("examples/example5.py", "1")
    _, _, _, branch_covered, branch_total, branch_missing = get_coverage(output)
    assert branch_covered == 3
    assert branch_total == 6
    assert branch_missing == {'6->7', '8->11', '12->13'}

def test_example5_statement_2():
    output = run_pcov("examples/example5.py", "0")
    stmt_covered, stmt_total, stmt_missing, _, _, _ = get_coverage(output)
    assert stmt_covered == 9
    assert stmt_total == 14

def test_example5_statement_verbose_2():
    output = run_pcov_verbose("examples/example5.py", "0")
    stmt_covered, stmt_total, stmt_missing, _, _, _ = get_coverage(output)
    assert stmt_covered == 9
    assert stmt_total == 14
    assert stmt_missing == {8, 9, 11, 14, 15}

def test_example5_branch_2():
    output = run_pcov("examples/example5.py", "0")
    _, _, _, branch_covered, branch_total, branch_missing = get_coverage(output)
    assert branch_covered == 2
    assert branch_total == 6

def test_example5_branch_verbose_2():
    output = run_pcov_verbose("examples/example5.py", "0")
    _, _, _, branch_covered, branch_total, branch_missing = get_coverage(output)
    assert branch_covered == 2
    assert branch_total == 6
    assert branch_missing == {'6->8', '8->9', '8->11', '12->14'}


