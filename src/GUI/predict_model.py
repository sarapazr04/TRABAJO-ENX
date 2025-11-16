def _from_col_to_val(entry_cols, entry_vals):
    result_list = []
    for col in entry_cols:
        tmp = [col]
        tmp.append(entry_vals.pop(0))
        result_list.append(tmp)
    print("Res list:", result_list)
    return result_list


def predict_result(entry_cols, entry_vals, formula):
    print("Cols:", entry_cols, "Vals:", entry_vals)
    values = _from_col_to_val(entry_cols, entry_vals)
    salida, tmp = formula.split(" = ")
    for [entry, val] in values:
        tmp = tmp.replace(entry, val)

    result = eval(tmp)
    return salida + " = " + str(result)


# print(predict_result(list("pepino"), list("676967"), "noseq = 1 * p + 2* e + 0 * p + 1 * i + 2* n + 3 * o"))
