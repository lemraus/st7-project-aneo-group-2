def cost_func(array, graph):

    total_cost = 0

    # Params
    COST = 0.1 # Cost per second
    BOOTING_TIME = 5*60

    # Array of finishing times of the last task of a given machine
    time_machine = [0] * len(array)

    # Array of finishing time of a given task
    time_task = [0] * len(array)

    for task, machine in array:
        last_task_ending_time = time_machine[machine]
        starting_time = last_task_ending_time
        duration = graph.nodes[task]['data']
        for key in graph.predecessors(task):
            starting_time = max(starting_time, time_task[key]) # task cannot start while its dependencies are not finished
        finishing_time = starting_time + duration
        time_machine[machine] = finishing_time
        time_task[task] = finishing_time
        if last_task_ending_time == 0 and starting_time < BOOTING_TIME: # We have to boot the machine
            time_machine[machine] += BOOTING_TIME
            time_task[task] += BOOTING_TIME
            total_cost += COST*(BOOTING_TIME + duration)
        elif starting_time - last_task_ending_time > BOOTING_TIME: # We have to reboot the machine
            total_cost += COST*(BOOTING_TIME + duration)
        else: # The machine stays on
            total_cost += COST*(last_task_ending_time + finishing_time)
        print(f'Tâche {task}: coût de {total_cost}.')
    
    return (total_cost, max(time_machine))
