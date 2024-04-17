from collections import deque, OrderedDict
import copy
from sudoku_constraints4x4 import CSP4x4
from sudoku_constraints9x9 import domain9x9, var9x9, constraint9x9, CSP9x9
from sudoku_test_ex import puzzle1_4x4, puzzle1_9x9, puzzle2_9x9, puzzle3_9x9, puzzle4_9x9, puzzle5_9x9
from flask import Flask, jsonify, request, render_template, Response

app = Flask(__name__)
@app.route('/')
def main_render():
    return render_template('template.html')

#for testing!!
#function that takes in a CSP and a problem and modifies the CSP to reflect the initial assignments in the problem
def modify_domains(CSP, problem):
    for var in CSP[0]:
        row = int(var[1]) - 1
        col = int(var[2]) - 1
        if problem[row][col] != 0:
            CSP[1][var] = [problem[row][col]]

#make CSP from the dictionary returned from requests.form
def make_csp(ui_dict):
    domain_csp = domain9x9
    for key, value in ui_dict.items():
        if value != '':
            domain_csp[key] = [int(value)]
    UI_CSP = [var9x9, domain_csp, constraint9x9]
    return UI_CSP

# print(CSP9x9[1])
# modify_domains(CSP9x9, puzzle1_9x9)
# print("-------------------------------------------------------------------")
# print("-------------------------------------------------------------------")
# print("-------------------------------------------------------------------")
# print(CSP9x9[1])

#part 2: revise that takes a CSP and the names of two variables as input and modifies the CSP, removing any value in the
#first variable’s domain where there isn’t a corresponding value in the other variable’s domain that
#satisfies the constraint between the variables. return a boolean indicating whether or not any values were removed.
def revise(CSP, Cx, Cy):
    order = 0
    if (Cx, Cy) in CSP[2]:
        constraintArr = CSP[2][(Cx, Cy)]
        order = 1
    elif (Cy, Cx) in CSP[2]:
        constraintArr = CSP[2][(Cy, Cx)]
        order = 2
    else:
        return False
    revised = False
    removed_from_domain = []
    for x in CSP[1][Cx]:
        consistent_with_y = False
        for y in CSP[1][Cy]:
            if order == 1:
                if [x, y] in constraintArr:
                    consistent_with_y = True
                    break
            elif order == 2:
                if [y, x] in constraintArr:
                    consistent_with_y = True
                    break
        if not consistent_with_y:
            revised = True
            removed_from_domain.append(x)
    if revised == True:
        # print("removed from domain", Cx,  removed_from_domain)
        CSP[1][Cx] = list(set(CSP[1][Cx]) - set(removed_from_domain))
        # print("CSP: ", CSP[1])
    return revised

# modify_domains(CSP4x4, puzzle1_4x4)
# print(revise(CSP4x4, 'C12', 'C11'))
# print(CSP4x4[1])
# print("-------------------------------------------------------------------")

#helper function that takes in Xi and the CSP and returns the neighbors of Xi
def get_neighbors(CSP, Xi):
    neighbors = set()
    for (Cx, Cy) in CSP[2]:
        if Cx == Xi:
            neighbors.add(Cy)
        elif Cy == Xi:
            neighbors.add(Cx)
    return neighbors


#part 3: AC-3 algorithm that takes a CSP as input and  modifies it such that any inconsistent values across all domains are removed. 
#The function should return a boolean indicating whether or not all variables have at least one value left in their domains
#use a python deque to implement the queue: https://docs.python.org/3/library/collections.html#collections.deque. appendleft(), pop()
def AC3(CSP):
    queue = deque((Xi, Xj) for (Xi, Xj) in CSP[2])
    # print("queue", queue)
    while queue:
        Xi, Xj = queue.pop()
        neighbors = get_neighbors(CSP, Xi)
        result1 = revise(CSP, Xi, Xj)
        result2 = revise(CSP, Xj, Xi)
        # print("result", result1, result2)
        if result1:
            if len(CSP[1][Xi]) == 0:
                return False
            for n in neighbors - {Xj}:
                if n not in queue:
                    queue.appendleft((n, Xi))
        if result2:
            if len(CSP[1][Xj]) == 0:
                return False
            for n in neighbors - {Xi}:
                if n not in queue:
                    queue.appendleft((n, Xj))
        # print("queue", queue)
    return True

# modify_domains(CSP4x4, puzzle1_4x4)
# print(AC3(CSP4x4))
# print(CSP4x4[1])
# print("-------------------------------------------------------------------")

# Write a function minimum-remaining-values that takes a CSP and a set of variable assignments
# as input, and returns the variable with the fewest values in its domain among the unassigned
# variables in the CSP. (unassigned = domain > 1). assignments is {C11: 1, C12: 2, C13: 9, C14: 6} - assigned dictionary
def minimum_remaining_values(CSP, assignments):
    unassigned_variables = []
    for var in CSP[0]:
        if var not in assignments:
            unassigned_variables.append(var)
    min_domain_size = float('inf')
    min_variable = None
    for var in unassigned_variables:
        domain_size = len(CSP[1][var])
        if domain_size < min_domain_size:
            min_domain_size = domain_size
            min_variable = var
    return min_variable

#part 5: Implement a backtracking search which takes a CSP and finds a valid assignment for all the variables in the CSP, if one exists. It should leverage your AC-3 implementation to maintain
# arc consistency. When Choosing a variable to assign, it should use your minimum remaining values heuristic implementation. Along with the solution to the CSP, your search should return
# the order in which it assigned the variables, and the domains of the remaining unassigned variables after each assignment. You can test your code on the small problem you specified in
# Part 1, as well as the puzzles from the Example Puzzles section below
def backtracking_search(CSP):
    assignments = OrderedDict()
    for key, val in CSP[1].items():
        if len(val) == 1:
            assignments[key] = val[0]
    # print("assignments: ", assignments)
    #make initial puzzle by removing constraints associated with the initial assignments
    AC3(CSP)
    # print("initial CSP: ", CSP[1])
    order = []
    backtracks = OrderedDict()
    backtrack_count = OrderedDict()
    return backtrack(CSP, assignments, order, backtracks, backtrack_count)

#select-unassigned-var = minimum-remaining-values, inference = ac3
def backtrack(CSP, assignments, order, backtracks, backtrack_count):
    if set(assignments.keys()) == set(CSP[0]):
        return assignments, order, backtracks, backtrack_count
    var = minimum_remaining_values(CSP, assignments)
    for value in CSP[1][var]:
        # print("value: " , value)
        CSP2 = [CSP[0], copy.deepcopy(CSP[1]), CSP[2]] #deep copying the domain
        assignments[var] = value
        # print("assignments: ", assignments)
        old_domain = CSP2[1][var]
        CSP2[1][var] = [value]
        order.append(var)
        inferences = AC3(CSP2)
        # print("ac3=", inferences)
        # print("CSP2: ", CSP2[1])
        if inferences == True:
            result = backtrack(CSP2, assignments, order, backtracks, backtrack_count)
            # print("result: ",result)
            if result != None:
                return result
        else:
            if backtracks.get(var) == None:
                backtracks[var] = []
                backtrack_count[var] = 0
            backtracks[var].append(value)
            backtrack_count[var] += 1
        CSP2[1][var] = old_domain
        del assignments[var]
        order.pop()
    return None

# modify_domains(CSP9x9, puzzle4_9x9)
# assignments, order, backtracks, backtrack_count = backtracking_search(CSP9x9)
# print("solution: ", assignments)
# print("-----------------------")
# print("backtracks: ", backtracks)
# print("--------------------------")
# print("backtrack count: ", backtrack_count)
# # print(backtracking_search(CSP4x4))
# print("CSP: ", CSP4x4[1])

@app.route('/backtracking_search', methods=['POST'])
def getting_solution():
    ui_csp = make_csp(request.form)
    assignments, order, backtracks, backtrack_count = backtracking_search(ui_csp)
    
    # Generate the step-by-step solution HTML
    def generate_solution():
        current_solution = {}
        initial_solution = []
        for already_assigned in ui_csp[1]:
            if len(ui_csp[1][already_assigned]) == 1:
                current_solution[already_assigned] = ui_csp[1][already_assigned][0]
                initial_solution.append(already_assigned)
        print(initial_solution)
        for var in order:
            current_solution[var] = assignments[var]
            with app.app_context():
                yield render_template('solution.html', puzzle=ui_csp[1], solution=current_solution, initial_assignments=initial_solution)

    # Use the generator to stream the HTML content back to the client
    return Response(generate_solution(), content_type='text/html')

    # #for advanced UI
    # ui_csp = make_csp(request.form)
    # assignments, order, backtracks, backtrack_count = backtracking_search(ui_csp)
    # return jsonify(assignments)


if __name__ == '__main__':
    app.run(host='localhost', port=5000)