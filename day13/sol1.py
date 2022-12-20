from functools import reduce, cmp_to_key

def compare(left, right) -> bool:
    print(f"Compare {left} vs {right}")
    if type(left) == int:
        if type(right) != int:
            print(f"Upgrading {left} to [{left}]")
            return compare([left], right)
        else:
            if left == right:
                return None
            else:
                if left < right:
                    print("Left smaller, true\n\n")
                    return True
                else:
                    print("Right smaller, false\n\n")
                    return False
    else:
        if type(right) != int:
            for i in range(max(len(left), len(right))):  
                if i >= len(left):
                    return True
                if i >= len(right):
                    return False                  
                state = compare(left[i], right[i])
                if state == None:
                    continue
                else:
                    return state
            return None
        else:
            print(f"Upgrading {right} to [{right}]")
            return compare(left, [right])

lines = []
with open("input.txt", 'r') as file:
    lines = list(map(lambda x: eval(x), filter(lambda x: x != '',map(lambda x: x.strip(), file.readlines()))))
    lines_pairs = [(lines[i], lines[i+1]) for i in range(len(lines)) if (i < len(lines) - 1) and i%2 == 0]

lines_sol = enumerate([compare(i[0], i[1]) for i in lines_pairs])
print(reduce(lambda x, y: (x[0]+y[0]+1, True) if y[1] else (x[0], True), lines_sol, (0, True))[0])

sol2 = (1 + sum(1 for i in lines if compare(i, [[2]]))) * (2 + sum(1 for i in lines if compare(i, [[6]])))
print(sol2)