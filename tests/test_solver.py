# test_solver.py
import pytest
import sys
import os
import sympy as sp

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ailator.solver import evaluate_expression, derivative, integral

x = sp.Symbol('x')

def test_evaluate_expression_basic():
    result, _ = evaluate_expression("2 + 3")
    assert result == 5

def test_evaluate_expression_symbolic():
    result, _ = evaluate_expression("x + x")
    assert result.equals(2*x)
    
    result, _ = evaluate_expression("x**2 + 2*x")
    assert result.equals(x**2 + 2*x)  # matematiksel eşitlik

def test_derivative_basic():
    assert derivative("x**2") == 2*x
    assert derivative("x**3 + x") == 3*x**2 + 1

def test_integral_basic():
    assert integral("2*x") == x**2
    assert integral("3*x**2") == x**3

def test_invalid_expression():
    result, explanation = evaluate_expression("2//")  # Hatalı ifade
    assert result is None
    assert "Hata" in explanation
