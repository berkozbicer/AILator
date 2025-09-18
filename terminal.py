# ---------------------------
# AI Destekli Hesap Makinesi - Gelişmiş Sürüm
# ---------------------------

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from sympy import Symbol
from colorama import init, Fore
import os
import time
import json

# ---------------------------
# Başlangıç ayarları
# ---------------------------
init(autoreset=True)
x = sp.Symbol('x')
HISTORY_FILE = "history.json"

def save_history(entry):
    """Hesaplama geçmişini dosyaya kaydet"""
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
        else:
            history = []

        history.append(entry)
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(Fore.RED + f"Geçmiş kaydedilemedi: {e}")


def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []


# ---------------------------
# Matematiksel İşlemler
# ---------------------------
def evaluate_expression(expr: str):
    """Genel matematiksel ifade"""
    try:
        result = sp.sympify(expr)
        explanation = f"İfade çözümlendi: {result}"
        save_history({"type": "evaluate", "expr": expr, "result": str(result)})
        return result, explanation
    except Exception as e:
        return None, f"Hata: {e}"


def derivative(expr: str, var='x'):
    try:
        var_sym = sp.Symbol(var)
        result = sp.diff(sp.sympify(expr), var_sym)
        save_history({"type": "derivative", "expr": expr, "result": str(result)})
        return result
    except Exception as e:
        return f"Hata: {e}"


def integral(expr: str, var='x'):
    try:
        var_sym = sp.Symbol(var)
        result = sp.integrate(sp.sympify(expr), var_sym)
        save_history({"type": "integral", "expr": expr, "result": str(result)})
        return result
    except Exception as e:
        return f"Hata: {e}"


def limit(expr: str, point=0, var='x'):
    try:
        var_sym = sp.Symbol(var)
        result = sp.limit(sp.sympify(expr), var_sym, point)
        save_history({"type": "limit", "expr": expr, "point": point, "result": str(result)})
        return result
    except Exception as e:
        return f"Hata: {e}"


def taylor_series(expr: str, var='x', x0=0, n=5):
    try:
        var_sym = sp.Symbol(var)
        result = sp.series(sp.sympify(expr), var_sym, x0, n).removeO()
        save_history({"type": "taylor", "expr": expr, "x0": x0, "n": n, "result": str(result)})
        return result
    except Exception as e:
        return f"Hata: {e}"


def solve_equation(expr: str, var='x'):
    try:
        var_sym = sp.Symbol(var)
        result = sp.solve(sp.sympify(expr), var_sym)
        save_history({"type": "solve", "expr": expr, "result": [str(r) for r in result]})
        return result
    except Exception as e:
        return f"Hata: {e}"


def simplify_expression(expr: str):
    try:
        result = sp.simplify(sp.sympify(expr))
        save_history({"type": "simplify", "expr": expr, "result": str(result)})
        return result
    except Exception as e:
        return f"Hata: {e}"


# ---------------------------
# ASCII Grafik Fonksiyonları
# ---------------------------
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def plot_expression_ascii(expr, x_min=-10, x_max=10, width=50, height=15, char='█', color=Fore.BLUE):
    try:
        f = sp.lambdify(x, expr, 'numpy')
        xs = np.linspace(x_min, x_max, width)
        ys = f(xs)
        y_min, y_max = np.min(ys), np.max(ys)
        y_range = y_max - y_min if y_max != y_min else 1
        lines = []
        for i in range(height, 0, -1):
            threshold = y_min + (y_range * i / height)
            line = ''.join([char if y_val >= threshold else ' ' for y_val in ys])
            lines.append(line)
        print(Fore.CYAN + "+" + "-"*width + "+")
        for line in lines:
            print(color + "|" + line + "|")
        print(Fore.CYAN + "+" + "-"*width + "+")
        print(Fore.YELLOW + f"x: {x_min} → {x_max}, y: {y_min:.2f} → {y_max:.2f}")
    except Exception as e:
        print(Fore.RED + f"ASCII grafik çizilemedi: {e}")


def plot_multiple_ascii(func_list, x_min=-10, x_max=10, width=50, height=15, chars=None, colors=None):
    if chars is None:
        chars = ['█', '▓', '▒', '░']
    if colors is None:
        colors = [Fore.BLUE, Fore.GREEN, Fore.MAGENTA, Fore.CYAN]

    xs = np.linspace(x_min, x_max, width)
    ys_list = []
    for expr in func_list:
        f = sp.lambdify(x, expr, 'numpy')
        ys_list.append(f(xs))

    all_ys = np.concatenate(ys_list)
    y_min, y_max = np.min(all_ys), np.max(all_ys)
    y_range = y_max - y_min if y_max != y_min else 1

    lines = ['' for _ in range(height)]
    for i in range(height, 0, -1):
        threshold = y_min + (y_range * i / height)
        line = ''
        for j in range(width):
            char_printed = False
            for k, ys in enumerate(ys_list):
                if ys[j] >= threshold:
                    line += colors[k % len(colors)] + chars[k % len(chars)]
                    char_printed = True
                    break
            if not char_printed:
                line += ' '
        lines[height-i] = line

    print(Fore.CYAN + "+" + "-"*width + "+")
    for line in lines:
        print(line)
    print(Fore.CYAN + "+" + "-"*width + "+")
    print(Fore.YELLOW + f"x: {x_min} → {x_max}, y: {y_min:.2f} → {y_max:.2f}")


def plot_expression_matplotlib(expr, x_min=-10, x_max=10, points=400, color='blue', ax=None):
    try:
        f = sp.lambdify(x, expr, 'numpy')
        xs = np.linspace(x_min, x_max, points)
        ys = f(xs)
        if ax is None:
            plt.ion()
            fig, ax = plt.subplots()
        ax.plot(xs, ys, color=color)
        ax.set_title(f"Grafik: {expr}")
        ax.grid(True)
        plt.show(block=False)
        return ax
    except Exception as e:
        print(Fore.RED + f"Matplotlib grafik çizilemedi: {e}")
        return None


# ---------------------------
# Terminal Menü ve Arayüz
# ---------------------------
def print_header(title):
    print(Fore.CYAN + "+" + "-"*50 + "+")
    print(Fore.CYAN + "|{:^50}|".format(title))
    print(Fore.CYAN + "+" + "-"*50 + "+")


def print_menu():
    print(Fore.CYAN + "+" + "-"*50 + "+")
    print(Fore.YELLOW + "| 1. İfade hesapla{:>33}|")
    print(Fore.YELLOW + "| 2. Türev al{:>38}|")
    print(Fore.YELLOW + "| 3. İntegral al{:>35}|")
    print(Fore.YELLOW + "| 4. Limit hesapla{:>30}|")
    print(Fore.YELLOW + "| 5. Taylor serisi{:>31}|")
    print(Fore.YELLOW + "| 6. Denklem çöz{:>33}|")
    print(Fore.YELLOW + "| 7. Çoklu fonksiyon ASCII grafik{:>22}|")
    print(Fore.YELLOW + "| 0. Çıkış{:>42}|")
    print(Fore.CYAN + "+" + "-"*50 + "+")


def print_message(msg, msg_type="info"):
    color = Fore.WHITE
    if msg_type == "error":
        color = Fore.RED
    elif msg_type == "success":
        color = Fore.GREEN
    border = "+" + "-"*(len(msg)+2) + "+"
    print(color + border)
    print(color + "| " + msg + " |")
    print(color + border)


# ---------------------------
# Ana Döngü
# ---------------------------
if __name__ == "__main__":
    print_header("AI Destekli Hesap Makinesi - Gelişmiş")

    ax_main = None  # Matplotlib ana eksen (dinamik güncelleme)

    while True:
        print_menu()
        choice = input(Fore.YELLOW + "Seçiminiz: ").strip()
        if choice == '0':
            print_message("Programdan çıkılıyor...", "info")
            break

        expr_input = input(Fore.YELLOW + "İşlemi girin: ").strip()
        try:
            if choice == '1':
                result, explanation = evaluate_expression(expr_input)
            elif choice == '2':
                result = derivative(expr_input)
                explanation = f"Türev alındı: {result}"
            elif choice == '3':
                result = integral(expr_input)
                explanation = f"İntegral alındı: {result}"
            elif choice == '4':
                point = float(input(Fore.YELLOW + "Limit noktası (default 0): ") or 0)
                result = limit(expr_input, point)
                explanation = f"{point} noktasındaki limit: {result}"
            elif choice == '5':
                x0 = float(input(Fore.YELLOW + "Taylor noktası x0 (default 0): ") or 0)
                n = int(input(Fore.YELLOW + "Terim sayısı n (default 5): ") or 5)
                result = taylor_series(expr_input, x0=x0, n=n)
                explanation = f"Taylor serisi ({n} terim): {result}"
            elif choice == '6':
                result = solve_equation(expr_input)
                explanation = f"Denklem çözüldü: {result}"
            elif choice == '7':
                func_count = int(input(Fore.YELLOW + "Kaç fonksiyon çizeceksiniz? (2-4): "))
                func_list = []
                for i in range(func_count):
                    fexpr = input(Fore.YELLOW + f"{i+1}. fonksiyon: ").strip()
                    func_list.append(sp.sympify(fexpr))
                plot_multiple_ascii(func_list)
                continue
            else:
                print_message("Geçersiz seçenek! Tekrar deneyin.", "error")
                continue

            if result is not None:
                print_message(f"Sonuç: {result}", "success")
                print_message(f"Adım Adım Açıklama: {explanation}", "info")
            else:
                print_message(f"Hata: {explanation}", "error")
                continue

            plot_graph = input(Fore.YELLOW + "ASCII veya Matplotlib grafiği çizilsin mi? (e/h): ").strip().lower()
            if plot_graph == 'e':
                x_min = float(input(Fore.YELLOW + "x_min (default -10): ") or -10)
                x_max = float(input(Fore.YELLOW + "x_max (default 10): ") or 10)
                width = int(input(Fore.YELLOW + "ASCII genişliği (default 50): ") or 50)
                height = int(input(Fore.YELLOW + "ASCII yüksekliği (default 15): ") or 15)
                char = input(Fore.YELLOW + "ASCII karakteri (default █): ") or '█'
                color = Fore.BLUE
                matplotlib_color = input(Fore.YELLOW + "Matplotlib çizgi rengi (default blue): ") or 'blue'

                # ASCII grafiği
                plot_expression_ascii(sp.sympify(expr_input), x_min=x_min, x_max=x_max,
                                      width=width, height=height, char=char, color=color)
                # Matplotlib grafiği (dinamik güncelleme)
                ax_main = plot_expression_matplotlib(sp.sympify(expr_input), x_min=x_min, x_max=x_max,
                                                     color=matplotlib_color, ax=ax_main)

        except Exception as e:
            print_message(f"Hata oluştu: {e}", "error")
