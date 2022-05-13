
class DFA:
    def __init__(self):
        self.states = set()
        self.alphabet = set()
        self.transitions = {}
        self.initial_state = ""
        self.final_states = set()
        self.no_transitions = 0
        self.no_states = 0
        self.partitions = []
        self.matrix = {}

    def read(self, filename):
        file_in = open(filename, "r")
        first_line = file_in.readline().split()
        self.no_states = int(first_line[0])
        self.no_transitions = int(first_line[1])

        for index_transition in range(self.no_transitions):
            line = file_in.readline().split()
            if line[0] in self.transitions.keys():
                self.transitions[line[0]][line[2]] = line[1]
            else:
                self.transitions[line[0]] = {line[2]: line[1]}
            self.states.add(line[0])
            self.states.add(line[1])
            self.alphabet.add(line[2])

        self.initial_state = file_in.readline()
        last_line = file_in.readline().split()
        no_final_states = int(last_line[0])
        for index in range(no_final_states):
            self.final_states.add(last_line[index+1])

    def set_initial_state(self, value):
        self.initial_state = value

    def complete(self):
        #graph completion
        # firstly, I check if the graph is NOT already completed
        no_letters = len(self.alphabet)

        if self.no_transitions != self.no_states * no_letters:
            # ONLY if the graph is NOT completed, I add a new non-final state
            if self.initial_state.isnumeric():  # check if states are numbers
                new_state = sorted(self.alphabet)[-1] + 1  # add new state with value next num
            else:  # if states are chars
                new_state = chr(ord(sorted(self.states)[-1]) + 1)  # then add new state with next char in ascii table
            # print(new_state)
            self.states.add(new_state)
            self.transitions[new_state] = {}
            for start_state in self.states:
                if start_state in self.transitions:  # check if a state is a first state for a transition
                    current_transitions = set(self.transitions[start_state].keys())
                else:                               # if not, I add it to the transitions dict
                    current_transitions = set()
                    self.transitions[start_state] = {}
                transitions_to_do = self.alphabet - current_transitions
                for transition in transitions_to_do:
                    self.transitions[start_state][transition] = new_state

    def partition(self, changed):
        if changed:
            changed = False
            for line in self.matrix:
                for column in self.matrix[line]:
                    for letter in self.alphabet:
                        letter_transitions = [self.transitions[line][letter], self.transitions[column][letter]]
                        if letter_transitions[1] != letter_transitions[0] and not self.matrix[line][column]:
                            letter_transitions.sort()
                            if self.matrix[letter_transitions[1]][letter_transitions[0]]:
                                self.matrix[line][column] = self.matrix[letter_transitions[1]][letter_transitions[0]]
                                changed = True
            self.partition(changed)
        else:
            return

    def minimize(self):
        self.complete()  # to minimize DFA, it has to be completed

        sorted_states = sorted(self.states)
        for index in range(self.no_states):
            self.matrix[sorted_states[index]] = {}
            for state2 in sorted_states[:index]:
                if (sorted_states[index] in self.final_states) ^ (state2 in self.final_states):
                    self.matrix[sorted_states[index]][state2] = 1
                else:
                    self.matrix[sorted_states[index]][state2] = 0



        # print(self.matrix, sep="\n")

        self.partition(True)


        # print(self.matrix, sep="\n")
        self.partitions = []
        for line in self.matrix:
            for column in self.matrix[line]:
                if not self.matrix[line][column]:
                    for i in range(len(self.partitions)):
                        if line in self.partitions[i] or column in self.partitions[i]:
                            self.partitions[i].add(line)
                            self.partitions[i].add(column)
                            break
                    else:
                        self.partitions.append({line, column})

        # print(self.partitions)
        partition_union = set()
        for partition in self.partitions:
            partition_union |= partition
        # print(partition_union)

        self.partitions.extend({state} for state in self.states-partition_union)
        # print(self.partitions)
        min_dfa = DFA()
        min_dfa.states = set("".join(sorted(state)) for state in self.partitions)
        # print(min_dfa.states)
        min_dfa.transitions = {}
        for state in min_dfa.states:
            min_dfa.transitions[state]={}
            for transition in self.transitions[state[0]].items():
                for new_state in min_dfa.states:
                    if transition[1] in new_state:
                        min_dfa.transitions[state][transition[0]] = new_state
                        break
        # print(min_dfa.states)

        for new_state in min_dfa.states:
            if set(sorted(new_state)) & self.final_states != set():
                min_dfa.final_states.add(new_state)
            if set(sorted(new_state)) & set(self.initial_state) != set():
                min_dfa.initial_state = new_state



        # print("finals", min_dfa.final_states)

        return min_dfa















