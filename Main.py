from flask import Flask, render_template, request
from gurobipy import Model, GRB

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('Main.html')

@app.route('/task_optimizer')
def task_optimizer():
    return render_template('TaskOptimizer.html')

@app.route('/solve_task_optimizer', methods=['POST'])
def solve_task_optimizer():
    try:
        num_nodes = len([key for key in request.form.keys() if key.startswith('capacity_')])
        num_tasks = len([key for key in request.form.keys() if key.startswith('requirements_')])
        tasks_costs = []
        capacities = []
        activation_costs = []
        max_loads = []
        requirements = []

        for i in range(1, num_nodes + 1):
            row_costs = [float(request.form[f'task_costs_{j}_{i}']) for j in range(1, num_tasks + 1)]
            tasks_costs.append(row_costs)
            capacities.append(float(request.form[f'capacity_{i}']))
            activation_costs.append(float(request.form[f'activation_cost_{i}']))
            max_loads.append(float(request.form[f'max_load_{i}']))

        for j in range(1, num_tasks + 1):
            requirements.append(float(request.form[f'requirements_{j}']))

        # Create the Gurobi model
        model = Model("Task Allocation")

        # Decision variables
        x = {(i, j): model.addVar(vtype=GRB.BINARY, name=f"x_{i}_{j}")
             for i in range(num_nodes) for j in range(num_tasks)}

        y = {i: model.addVar(vtype=GRB.BINARY, name=f"y_{i}")
             for i in range(num_nodes)}

        # Each task must be assigned to exactly one node
        for j in range(num_tasks):
            model.addConstr(sum(x[i, j] for i in range(num_nodes)) == 1,
                            name=f"task_assignment_{j}")

        # Resource capacity constraints
        for i in range(num_nodes):
            model.addConstr(
                sum(requirements[j] * x[i, j] for j in range(num_tasks)) <= capacities[i] * y[i],
                name=f"capacity_{i}")

        # Maximum load constraints
        for i in range(num_nodes):
            model.addConstr(
                sum(x[i, j] for j in range(num_tasks)) <= max_loads[i] * y[i],
                name=f"max_load_{i}")

        # Node activation constraints
        for i in range(num_nodes):
            for j in range(num_tasks):
                model.addConstr(x[i, j] <= y[i], name=f"activation_{i}_{j}")

        # Objective function
        obj = (sum(tasks_costs[i][j] * x[i, j]
                   for i in range(num_nodes)
                   for j in range(num_tasks)) +
               sum(activation_costs[i] * y[i]
                   for i in range(num_nodes)))

        model.setObjective(obj, GRB.MINIMIZE)

        # Set some solver parameters
        model.setParam('TimeLimit', 60)  # 60 second time limit
        model.setParam('MIPGap', 0.01)   # 1% optimality gap

        # Solve the model
        model.optimize()

        if model.status == GRB.OPTIMAL:
            # Collect results
            result_msg = "Optimization complete"
            x_values = {f"{i},{j}": x[i, j].X for i in range(num_nodes) for j in range(num_tasks)}
            y_values = {i: y[i].X for i in range(num_nodes)}

            # Format results
            allocation_results = []
            for i in range(num_nodes):
                tasks = [f"Task {j + 1}" for j in range(num_tasks) if x[i, j].X > 0.5]
                if tasks:
                    allocation_results.append(f"Node {i + 1}: {', '.join(tasks)}")

            # Store results in session
            results = {
                'num_nodes': num_nodes,
                'num_tasks': num_tasks,
                'x_values': x_values,
                'y_values': y_values,
                'allocation_results': allocation_results,
                'obj_value': model.objVal 
            }

            return render_template('ResultTaskOptimizer.html', results=results)

    except Exception as e:
        return str(e)

    return "Optimization complete"


@app.route('/ressource_optimizer')
def ressource_optimizer():
    return render_template('RessourceOptimizer.html')

if __name__ == '__main__':
    app.run(debug=True)