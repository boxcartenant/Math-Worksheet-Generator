import tkinter as tk
import random
import os
import tempfile

FONT_SIZE = 10  # Constant for font size, adjust as needed
PROBLEMS_PER_ROW_SIMPLE = 4
PROBLEMS_PER_ROW_LONG = 4
COLUMN_PADDING = 5  # Spaces between columns

class BaseProblem:
    name = ""
    is_simple = True
    extra_blank_lines = 0

    def generate(self):
        pass

class SimpleAddition(BaseProblem):
    name = "simple add"
    is_simple = True

    def generate(self):
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        return f"{a}+{b}="

class SimpleSubtraction(BaseProblem):
    name = "simple subtract"
    is_simple = True

    def generate(self):
        a = random.randint(2, 20)
        b = random.randint(1, a - 1)
        return f"{a}-{b}="

class SimpleMultiplication(BaseProblem):
    name = "simple multiply"
    is_simple = True

    def generate(self):
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        return f"{a}*{b}="

class SimpleDivision(BaseProblem):
    name = "simple divide"
    is_simple = True

    def generate(self):
        b = random.randint(2, 20)
        q = random.randint(1, 20)
        a = b * q
        return f"{a}/{b}="

class LongAddition(BaseProblem):
    name = "long add"
    is_simple = False

    def generate(self):
        a = random.randint(100, 999999)
        b = random.randint(100, 999999)
        sa = str(a)
        sb = str(b)
        width = max(len(sa), len(sb)) + 2  # Extra space for carry/alignment
        sa = sa.rjust(width)
        sb = sb.rjust(width)
        line = '-' * width
        return f" {sa}\n+{sb}\n {line}\n"

class LongSubtraction(BaseProblem):
    name = "long subtract"
    is_simple = False

    def generate(self):
        a = random.randint(100, 999999)
        b = random.randint(100, a - 1)
        sa = str(a)
        sb = str(b)
        width = max(len(sa), len(sb)) + 2  # Extra space for borrow/alignment
        sa = sa.rjust(width)
        sb = sb.rjust(width)
        line = '-' * width
        return f" {sa}\n-{sb}\n {line}\n"

class LongMultiplication(BaseProblem):
    name = "long multiply"
    is_simple = False
    extra_blank_lines = 8  # More space for partial products and sum

    def generate(self):
        a = random.randint(100, 9999)
        b = random.randint(10, 999)
        sa = str(a)
        sb = str(b)
        width = len(sa) + len(sb)
        sa = sa.rjust(width)
        sb = sb.rjust(width)
        line = '-' * width
        return f" {sa}\n*{sb}\n {line}\n"

class LongDivision(BaseProblem):
    name = "long divide"
    is_simple = False
    extra_blank_lines = 5  # Space for division steps

    def generate(self):
        divisor = random.randint(10, 999)
        quot = random.randint(10, 9999)
        dividend = divisor * quot
        sdiv = str(divisor)
        sdivd = str(dividend)
        space = ' ' * (len(sdiv) + 2)  # For ' )'
        line = '_' * len(sdivd)
        header_line = space + line
        div_line = sdiv + ' )' + sdivd
        return header_line + '\n' + div_line + '\n'

# List of problem types for extensibility
problem_types = [
    SimpleAddition,
    SimpleSubtraction,
    SimpleMultiplication,
    SimpleDivision,
    LongAddition,
    LongSubtraction,
    LongMultiplication,
    LongDivision
]

# UI Setup
root = tk.Tk()
root.title("Math Worksheet Generator")
root.geometry("800x600")

tk.Label(root, text="Total problems:").pack()
total_entry = tk.Entry(root)
total_entry.pack()

check_vars = []
check_buttons = []
for pt in problem_types:
    var = tk.IntVar()
    check = tk.Checkbutton(root, text=pt.name, variable=var)
    check.pack(anchor='w')
    check_vars.append(var)
    check_buttons.append(check)



def generate_worksheet(print_it=False):
    try:
        total = int(total_entry.get())
        if total <= 0:
            raise ValueError
    except:
        preview_text.delete(1.0, tk.END)
        preview_text.insert(tk.END, "Invalid total problems.")
        return

    selected_indices = [i for i in range(len(problem_types)) if check_vars[i].get()]
    if not selected_indices:
        preview_text.delete(1.0, tk.END)
        preview_text.insert(tk.END, "No problem types selected.")
        return

    selected = [problem_types[i] for i in selected_indices]
    num_types = len(selected)
    per_type = total // num_types
    extras = total % num_types

    worksheet = "Name: ____________________ Date: ____________\n\n"

    for i, typ_cls in enumerate(selected):
        typ = typ_cls()
        num = per_type + (1 if i < extras else 0)
        if num == 0:
            continue
        problems = [typ.generate() for _ in range(num)]

        worksheet += typ.name.capitalize() + ":\n\n"

        if typ.is_simple:
            # Horizontal, space them out
            max_len = max(len(p) for p in problems) + COLUMN_PADDING
            row = []
            for j, p in enumerate(problems):
                row.append(p)
                if len(row) == PROBLEMS_PER_ROW_SIMPLE or j == len(problems) - 1:
                    line = ""
                    for item in row:
                        line += item.ljust(max_len)
                    worksheet += line.rstrip() + "\n\n"  # Double space
                    row = []
            worksheet += "\n"
        else:
            # Vertical, side by side in rows
            for start in range(0, num, PROBLEMS_PER_ROW_LONG):
                group = problems[start:start + PROBLEMS_PER_ROW_LONG]
                group_lines = [p.splitlines() for p in group]
                # Add extra blank lines to each problem
                for lines in group_lines:
                    lines.extend([""] * typ.extra_blank_lines)
                max_height = max(len(lines) for lines in group_lines)
                # Pad shorter ones
                for lines in group_lines:
                    while len(lines) < max_height:
                        lines.append("")
                col_widths = [max(len(l) for l in lines) + COLUMN_PADDING for lines in group_lines]
                for k in range(max_height):
                    row_line = ""
                    for m in range(len(group_lines)):
                        row_line += group_lines[m][k].ljust(col_widths[m])
                    worksheet += row_line.rstrip() + "\n"
                worksheet += "\n"  # Double space between rows
            worksheet += "\n"

    if print_it:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.txt', mode='w') as f:
                f.write(worksheet)
                path = f.name
            #os.startfile(path, "open")
            os.startfile(path, "print")
        except Exception as e:
            preview_text.delete(1.0, tk.END)
            preview_text.insert(tk.END, f"Printing failed: {str(e)}")
    return worksheet

def preview():
    ws = generate_worksheet(print_it=False)
    if ws:
        preview_text.delete(1.0, tk.END)
        preview_text.insert(tk.END, ws)

preview_btn = tk.Button(root, text="Preview Sample", command=preview)
preview_btn.pack()

print_btn = tk.Button(root, text="Print Worksheet", command=lambda: generate_worksheet(print_it=True))
print_btn.pack()

preview_text = tk.Text(root, height=30, width=80, font=("Courier", FONT_SIZE))
preview_text.pack(side="bottom", fill="both", expand=True)

root.mainloop()
