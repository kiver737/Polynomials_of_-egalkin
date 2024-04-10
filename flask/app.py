from flask import Flask, render_template, request


app = Flask(__name__)


def zhegalkin_polynomial(k, f_vec):
    ans = ""
    target = build_pascal_triangle(pow(2, k), f_vec)
    for i in range(len(target)):
        if i == 0:
            if target[i] == '1':
                ans += '1' + " \u2295 "
        if int(target[i]) == 1:
            args_input = str(bin(i))[2:].zfill(k)
            conjuction = ""
            for j in range(len(args_input)):
                if int(args_input[j]) == 1:
                    conjuction += "x{}".format(j + 1)
            ans += conjuction
            if conjuction != "":
                ans += " \u2295 "
    ans = ans[:len(ans) - 2]
    args = ""
    for i in range(k):
        if i == k - 1:
            args += "x{}".format(i + 1)
            break
        args += "x{}, ".format(i + 1)
    return ans, args


def build_truth_table(k, f_vec):
    truth_table = ""
    for i in range(k):
        truth_table += "x{} ".format(i + 1)
    truth_table += "| f \n"
    truth_table += '-' * 3 * (k + 1) + '\n'
    for i in range(pow(2, k)):
        truth_table += "{} ".format("  ".join(str(bin(i))[2:].zfill(k)))
        truth_table += " | {} ".format(f_vec[i])
        truth_table += "\n"
    return truth_table


def build_pascal_triangle(l0, f_vec):
    pascal_triangle = ""

    def build_line(l, pasc, vec):
        line = ""
        if l == 0:
            return ""
        else:
            for i in range(l - 1):
                line += str((int(vec[i]) + int(vec[i + 1])) % 2)
            v = line
            line = " " * (l0 - l + 1) + " ".join(line) + " " * (l0 - l + 1) + '\n'
            return line + build_line(l - 1, pasc, v)

    pascal_triangle = " ".join(f_vec) + '\n' + build_line(l0, pascal_triangle, f_vec)
    target = ""
    lines = pascal_triangle.split('\n')
    for line in lines:
        if line.lstrip() != "":
            target += line.lstrip()[0]
    return target


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=['POST'])
def result():
    k = int(request.form['num_variables'])
    f_vec = request.form['function_vector']

    # Проверка, что длина вектора f_vec равна 2^k
    if len(f_vec) != pow(2, k):
        error_message = "Длина вектора и количество переменных не совпадают."
        return render_template('index.html', error_message=error_message)

    args = ""
    for i in range(k):
        if i == k - 1:
            args += "x{}".format(i + 1)
            break
        args += "x{}, ".format(i + 1)

    truth_table = build_truth_table(k, f_vec)
    zhegalkin, args = zhegalkin_polynomial(k, f_vec)
    return render_template('result.html', num_variables=k, function_vector=f_vec, args=args, truth_table=truth_table,
                           zhegalkin=zhegalkin)


if __name__ == '__main__':
    app.run(debug=True)
