from iminuit import Minuit
import pytest

tab = pytest.importorskip("tabulate")


def framed(s):
    return "\n" + str(s) + "\n"


def test_params():
    m = Minuit(
        lambda x, y: x ** 2 + (y / 2) ** 2 + 1,
        x=0,
        y=0,
        limit_y=(-1, 1),
        fix_x=True,
        errordef=1,
    )
    m.migrad()
    m.minos()
    assert (
        framed(tab.tabulate(*m.params.to_table()))
        == """
  pos  name      value    error  error-    error+    limit-    limit+    fixed
-----  ------  -------  -------  --------  --------  --------  --------  -------
    0  x             0      0.1                                          yes
    1  y             0      1.5  -1.0      1.0       -1.0      1.0
"""
    )


def test_matrix():
    m = Minuit(lambda x, y: x ** 2 + (y / 2) ** 2 + 1, x=0, y=0, errordef=1)
    m.migrad()
    assert (
        framed(tab.tabulate(*m.matrix().to_table()))
        == """
      x    y
--  ---  ---
x     1   -0
y    -0    4
"""
    )
