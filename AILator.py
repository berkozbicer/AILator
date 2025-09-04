# ---------------------------
# AI Destekli Hesap Makinesi
# ---------------------------

import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

# Değişken tanımla
x = sp.symbols('x')

def compute_and_explain(expr):
    """
    Sembolik hesaplama ve adım adım açıklama
    """
    explanation = ""
    try:
        # 1️⃣ Sembolik çözüm
        sonuc = sp.sympify(expr)

        # 2️⃣ Adım adım açıklama (basitleştirilmiş)
        if isinstance(sonuc, sp.Integral):
            explanation += f"Integral alınacak: {sonuc}\n"
            sonuc = sp.integrate(sonuc.expr, (x, 0, 1)) # örnek limit
            explanation += f"0-1 aralığında sonucu: {sonuc}\n"
        elif isinstance(sonuc, sp.Expr):
            explanation += f"İfade çözümlendi: {sonuc}\n"
        return sonuc, explanation
    except Exception as e:
        return None, f"Hata: {e}"

def plot_expression(expr):
    """
    Basit 2D grafik çizimi
    """
    f = sp.lambdify(x, expr, 'numpy')
    xs = np.linspace(-10, 10, 400)
    ys = f(xs)
    plt.plot(xs, ys)
    plt.title(f"Grafik: {expr}")
    plt.grid(True)
    plt.show()

# ---------------------------
# Kullanıcı arayüzü
# ---------------------------

while True:
    user_input = input("İşlem girin (çıkmak için boş bırakın): ")
    if not user_input:
        break

    # Hesapla ve açıklama ver
    sonuc, explanation = compute_and_explain(user_input)
    print("Sonuç:", sonuc)
    print("Adım Adım Açıklama:\n", explanation)

    # Grafik çiz (opsiyonel)
    plot_graph = input("Grafik çizmek ister misiniz? (e/h): ")
    if plot_graph.lower() == 'e' and sonuc is not None:
        plot_expression(sp.sympify(user_input))
