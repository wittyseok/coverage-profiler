from test_pcov import *

def test_example4_statement_1():
    output = run_pcov("examples/example4.py")
    stmt_covered, stmt_total, stmt_missing, _, _, _ = get_coverage(output)
    assert stmt_covered == 7
    assert stmt_total == 22

def test_example4_statement_verbose_1():
    output = run_pcov_verbose("examples/example4.py")
    stmt_covered, stmt_total, stmt_missing, _, _, _ = get_coverage(output)
    assert stmt_covered == 7
    assert stmt_total == 22
    assert stmt_missing == {5, 6, 9, 12, 13, 14, 15, 16, 17, 18, 19, 24, 25, 26, 28}

def test_example4_branch_1():
    output = run_pcov("examples/example4.py")
    _, _, _, branch_covered, branch_total, branch_missing = get_coverage(output)
    assert branch_covered == 1
    assert branch_total == 12

def test_example4_branch_verbose_1():
    output = run_pcov_verbose("examples/example4.py")
    _, _, _, branch_covered, branch_total, branch_missing = get_coverage(output)
    assert branch_covered == 1
    assert branch_total == 12
    assert branch_missing == {'12->13', '12->14', '14->15', '14->16', '16->17', '16->18', '18->-11', '18->19', '23->24', '25->26', '25->28'}

def test_example4_statement_2():
    output = run_pcov("examples/example4.py", "dog")
    stmt_covered, stmt_total, stmt_missing, _, _, _ = get_coverage(output)
    assert stmt_covered == 15
    assert stmt_total == 22

def test_example4_statement_verbose_2():
    output = run_pcov_verbose("examples/example4.py", "dog")
    stmt_covered, stmt_total, stmt_missing, _, _, _ = get_coverage(output)
    assert stmt_covered == 15
    assert stmt_total == 22
    assert stmt_missing == {14, 15, 16, 17, 18, 19, 26}

def test_example4_branch_2():
    output = run_pcov("examples/example4.py", "dog")
    _, _, _, branch_covered, branch_total, branch_missing = get_coverage(output)
    assert branch_covered == 4
    assert branch_total == 12

def test_example4_branch_verbose_2():
    output = run_pcov_verbose("examples/example4.py", "dog")
    _, _, _, branch_covered, branch_total, branch_missing = get_coverage(output)
    assert branch_covered == 4
    assert branch_total == 12
    assert branch_missing == {'12->14', '14->15', '14->16', '16->17', '16->18', '18->-11', '18->19', '25->26'}


def test_example4_statement_3():
    output = run_pcov("examples/example4.py", "dog", "cat")
    stmt_covered, stmt_total, stmt_missing, _, _, _ = get_coverage(output)
    assert stmt_covered == 17
    assert stmt_total == 22

def test_example4_statement_verbose_3():
    output = run_pcov_verbose("examples/example4.py", "dog", "cat")
    stmt_covered, stmt_total, stmt_missing, _, _, _ = get_coverage(output)
    assert stmt_covered == 17
    assert stmt_total == 22
    assert stmt_missing == {16, 17, 18, 19, 26}

def test_example4_branch_3():
    output = run_pcov("examples/example4.py", "dog", "cat")
    _, _, _, branch_covered, branch_total, branch_missing = get_coverage(output)
    assert branch_covered == 6
    assert branch_total == 12

def test_example4_branch_verbose_3():
    output = run_pcov_verbose("examples/example4.py", "dog", "cat")
    _, _, _, branch_covered, branch_total, branch_missing = get_coverage(output)
    assert branch_covered == 6
    assert branch_total == 12
    assert branch_missing == {'14->16', '16->17', '16->18', '18->-11', '18->19', '25->26'}

def test_example4_statement_4():
    output = run_pcov("examples/example4.py", "dog", "wolf", "cat")
    stmt_covered, stmt_total, stmt_missing, _, _, _ = get_coverage(output)
    assert stmt_covered == 16
    assert stmt_total == 22

def test_example4_statement_verbose_4():
    output = run_pcov_verbose("examples/example4.py", "dog", "wolf", "cat")
    stmt_covered, stmt_total, stmt_missing, _, _, _ = get_coverage(output)
    assert stmt_covered == 16
    assert stmt_total == 22
    assert stmt_missing == {14, 15, 16, 17, 18, 19}

def test_example4_branch_4():
    output = run_pcov("examples/example4.py", "dog", "wolf", "cat")
    _, _, _, branch_covered, branch_total, branch_missing = get_coverage(output)
    assert branch_covered == 4
    assert branch_total == 12

def test_example4_branch_verbose_4():
    output = run_pcov_verbose("examples/example4.py", "dog", "wolf", "cat")
    _, _, _, branch_covered, branch_total, branch_missing = get_coverage(output)
    assert branch_covered == 4
    assert branch_total == 12
    assert branch_missing == {'12->14', '14->15', '14->16', '16->17', '16->18', '18->-11', '18->19', '23->-1'}


