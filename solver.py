# ---------------------------
# solver.py
# AI Destekli Hesap Makinesi - Hesaplama Fonksiyonları
# ---------------------------

from sympy import sympify, Symbol, simplify, diff, integrate

def evaluate_expression(expr: str):
    """
    Matematiksel ifadeyi değerlendirir ve sonucu döndürür.
    Ayrıca basit bir açıklama string'i döndürür.
    """
    explanation = ""
    try:
        result = sympify(expr)
        explanation = f"İfade çözümlendi: {result}"
        return result, explanation
    except Exception as e:
        return None, f"Hata: {e}"


def derivative(expr: str, variable: str = 'x'):
    """
    Verilen ifadenin türevini alır.
    """
    try:
        x = Symbol(variable)
        return diff(sympify(expr), x)
    except Exception as e:
        return f"Hata: {e}"


def integral(expr: str, variable: str = 'x'):
    """
    Verilen ifadenin integrali.
    """
    try:
        x = Symbol(variable)
        return integrate(sympify(expr), x)
    except Exception as e:
        return f"Hata: {e}"


def simplify_expression(expr: str):
    """
    Verilen ifadeyi sadeleştirir.
    """
    try:
        return simplify(sympify(expr))
    except Exception as e:
        return f"Hata: {e}"
