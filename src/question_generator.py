import random
import math


def generate_question(difficulty):
    q_type = random.choice(["multiple_choice", "cartesian_plane"])

    if q_type == "cartesian_plane":
        return _cartesian_question(difficulty)
    return _multiple_choice_question(difficulty)


# --- Cartesian plane questions ---

_CARTESIAN_RANGES = {
    "Facil":   (5, 5),
    "Medio":   (8, 5),
    "Dificil": (10, 7),
}


def _cartesian_question(difficulty):
    x_range, y_range = _CARTESIAN_RANGES.get(difficulty, (5, 5))
    x = random.randint(-x_range, x_range)
    y = random.randint(-y_range, y_range)
    return {
        "type": "cartesian_plane",
        "question": f"Toque no ponto ({x}, {y}).",
        "target_point": (x, y),
        "hint": "O primeiro numero e X (horizontal), o segundo e Y (vertical).",
    }


# --- Multiple choice questions ---

def _multiple_choice_question(difficulty):
    generators = {
        "Facil": _easy_question,
        "Medio": _medium_question,
        "Dificil": _hard_question,
    }
    gen = generators.get(difficulty, _easy_question)
    return gen()


def _make_distractors(correct, count=2, min_distance=1, max_distance=5):
    """Generate distractor options that are plausible (never equal to correct)."""
    distractors = set()
    attempts = 0
    while len(distractors) < count and attempts < 50:
        offset = random.randint(min_distance, max_distance)
        sign = random.choice([-1, 1])
        val = correct + sign * offset
        if val != correct:
            distractors.add(val)
        attempts += 1
    # Fallback if we couldn't generate enough
    while len(distractors) < count:
        distractors.add(correct + len(distractors) + 1)
    return list(distractors)


def _make_mc(question, correct, hint):
    correct_int = int(correct)
    distractors = _make_distractors(correct_int)
    options = [str(correct_int)] + [str(d) for d in distractors]
    random.shuffle(options)
    return {
        "type": "multiple_choice",
        "question": question,
        "options": options,
        "correct_answer": str(correct_int),
        "hint": hint,
    }


# --- Easy: addition, subtraction ---

def _easy_question():
    a, b = random.randint(1, 20), random.randint(1, 20)
    if random.choice([True, False]):
        return _make_mc(f"Quanto e {a} + {b}?", a + b,
                        "Some os dois numeros.")
    return _make_mc(f"Quanto e {a} - {b}?", a - b,
                    "Subtraia o segundo numero do primeiro.")


# --- Medium: multiplication, division, simple powers ---

def _medium_question():
    kind = random.choice(["mult", "div", "power"])
    if kind == "mult":
        a, b = random.randint(2, 12), random.randint(2, 12)
        return _make_mc(f"Quanto e {a} x {b}?", a * b,
                        "Multiplique: some o primeiro numero varias vezes.")
    elif kind == "div":
        b = random.randint(2, 12)
        a = b * random.randint(2, 12)
        return _make_mc(f"Quanto e {a} / {b}?", a // b,
                        "Divida: quantas vezes o divisor cabe no dividendo?")
    else:
        base = random.randint(2, 6)
        exp = random.randint(2, 3)
        return _make_mc(f"Quanto e {base}^{exp}?", base ** exp,
                        f"Multiplique {base} por ele mesmo {exp} vezes.")


# --- Hard: logarithms, square roots, linear equations, expressions ---

def _hard_question():
    kind = random.choice(["log", "sqrt", "equation", "expression"])

    if kind == "log":
        base = random.randint(2, 5)
        exp = random.randint(2, 5)
        result = base ** exp
        return _make_mc(
            f"log base {base} de {result} = ?", exp,
            f"Qual expoente aplicado a {base} resulta em {result}?",
        )

    elif kind == "sqrt":
        # Only include harder square roots
        num = random.choice([36, 49, 64, 81, 100, 121, 144, 169, 196, 225])
        return _make_mc(
            f"Raiz quadrada de {num} = ?", int(math.sqrt(num)),
            "Qual numero multiplicado por si mesmo da esse resultado?",
        )

    elif kind == "equation":
        # Solve for x: ax + b = c
        a = random.choice([2, 3, 4, 5, 6])
        x = random.randint(-10, 10)
        b = random.randint(-20, 20)
        c = a * x + b
        return _make_mc(
            f"Se {a}x + {b} = {c}, quanto vale x?", x,
            f"Isole x: x = ({c} - {b}) / {a}.",
        )

    else:
        # Expression with order of operations
        a = random.randint(2, 8)
        b = random.randint(1, 5)
        c = random.randint(1, 10)
        result = a * b + c
        return _make_mc(
            f"Quanto e {a} x {b} + {c}?", result,
            "Resolva a multiplicacao primeiro, depois some.",
        )
