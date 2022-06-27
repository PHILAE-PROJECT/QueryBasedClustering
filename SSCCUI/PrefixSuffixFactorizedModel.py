#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 08:45:05 2022

@author: Vahana Dorcis
"""
import graphviz
import tempfile
from Navigator import Navigator


class PrefixSuffixFactorizedModel(object):

    def __init__(self, build_with_loop: bool = True):
        self.root = None
        self.alphabet = dict()
        self.final_states = dict()
        self.states_orders = dict()
        self.build_with_loop = build_with_loop
        self._state_number = 0
        self._sequences = set()
    # end __init__

    def _clear(self):
        """ Clear the variables that store the states. """
        self.root = None
        self.alphabet = dict()
        self.final_states = dict()
        self.states_orders = dict()
        self._state_number = 0
    # end _clear

    # %%
    def build_prefix_tree_acceptor(self, list_of_sequences: list):
        """
        Build the Prefix Tree Acceptor using the sequences.

        Parameters
        ----------
        list_of_sequences : list
            A list holding the sequences as list.
            Example 1: [['u', 0], ['s', 0], ['s', 0], ['s', 0], ['t', 0], ['a', 0]]
            Example 2: [['u'], ['s'], ['s'], ['s'], ['t'], ['a']]

        Returns
        -------
        None

        """
        # Validate inputs
        if not self.root or isinstance(self.root, Navigator) is False:
            self.root = Navigator(name="Init", description="", is_start=True)
        # end if
        if isinstance(self.final_states, dict) is False:
            self.final_states = dict()
        # end if
        if not self.alphabet or isinstance(self.alphabet, dict) is False:
            self.alphabet = dict()
        # end if
        if not self.states_orders or isinstance(self.states_orders, dict) is False:
            self.states_orders = dict()
        # end if

        # Create the root of the application to tie in all the paths. stuttering transition
        final_states_tracker = dict()  # Keep track of the states numbers used for the final states
        for _, states in self.final_states.items():
            for s in states:
                final_states_tracker[s.number] = True
            # end for
        # end for

        for sequence in list_of_sequences:
            if isinstance(sequence, list) is False:
                raise TypeError(f"Expected list, got {type(sequence)} instead.")
            # end if
            sequence_len = len(sequence)
            state_last_added = self.root  # Holds the last added state
            # Holds a final state that was previously added and matches the final state of the current sequences
            previous_final_state = None
            merge_index = None
            reverse_inputs, modified_sequence = list(), list()
            state_numbers = set()
            loop_tracker = dict()
            was_searched = False
            # Go through and add the items in the sequence
            for index, prefix in enumerate(sequence):
                is_start = index == 0
                is_final_state = index == sequence_len - 1

                if merge_index is not None and index >= merge_index:
                    state_last_added.update_next(previous_final_state, remove=False)
                    previous_final_state.update_previous(state_last_added, remove=False)
                    modified_sequence += reverse_inputs
                    break
                # end if

                # Convert the content of the sequence to string and concatenate it
                value = "_".join([str(y) for y in prefix if y]) if isinstance(prefix, list) else str(prefix)
                modified_sequence.append(value)
                # Look for the sequence item in the children of the current state
                state_search = state_last_added.find_next(name=value, stop_at_one=True, description=str())
                if not state_search:
                    # Check for a reflexive arc
                    if self.build_with_loop is True:
                        if state_last_added.name == value:
                            state_last_added.is_self_loop = True
                            loop_count = loop_tracker.get(state_last_added.number, 1) + 1
                            loop_tracker[state_last_added.number] = loop_count
                            state_last_added.loop_count = loop_count

                            if is_final_state is True:
                                state_last_added.is_final_state = True
                            # end if
                            if is_start is True:
                                state_last_added.is_start = True
                            # end if
                            continue
                        # end if
                    # end if

                    if not previous_final_state and self.final_states and was_searched is False:
                        previous_final_state, merge_index, reverse_inputs = self._factorize_suffixes(
                            sequence=sequence[index:], state_numbers=state_numbers)
                        was_searched = True
                        merge_index = (merge_index + index) if merge_index else None
                        if previous_final_state and is_final_state is True:
                            state_last_added.update_next(previous_final_state, remove=False)
                            previous_final_state.update_previous(state_last_added, remove=False)
                            break
                        # end if
                    # end if

                    self._state_number += 1
                    # Create a new state
                    state_next = Navigator(name=value, is_start=is_start, is_final_state=is_final_state)
                    state_next.number = self._state_number
                    state_numbers.add(state_next.number)
                    # Update linkage
                    state_next.update_previous(state_last_added, remove=False)
                    state_last_added.update_next(state_next, remove=False)
                    # Set the current state
                    state_last_added = state_next
                else:
                    state_last_added = state_search[0]
                    state_numbers.add(state_last_added.number)
                # end if
                if is_final_state is True:
                    state_last_added.is_final_state = True
                    if final_states_tracker.get(state_last_added.number, False) is False:
                        added = self.final_states.get(state_last_added.name, list())
                        added.append(state_last_added)
                        self.final_states[state_last_added.name] = added
                        final_states_tracker[state_last_added.number] = True
                    # end if
                # end if
                # Update the alphabet
                if self.alphabet.get(value, None) is None:
                    self.alphabet[value] = [state_last_added]
                elif self.states_orders.get(state_last_added.number, False) is False:
                    # The item would be in the self.states_orders if it was already added
                    self.alphabet[value].append(state_last_added)
                # end if
                self.states_orders[state_last_added.number] = state_last_added
            # end for
            self._sequences.add(",".join(modified_sequence))
            for sn, loop_count in loop_tracker.items():
                if loop_count > self.states_orders[sn].loop_count:
                    self.states_orders[sn].loop_count = loop_count
                # end if
            # end for
        # end for sequence
    # end build_prefix_tree_acceptor

    def _factorize_suffixes(self, sequence: list, state_numbers: set) -> tuple:
        """
        Build a prefix tree acceptor starting from the final state if a matching final state is found in the
        init_final_states dictionary.
        The value of the last item in sequence is compared to the values of the items in init_final_states.

        Parameters
        ----------
        sequence : list
            The list of items to use to build the PTA.

        state_numbers : set
            A set of int containing the name of the states used. This is to prevent
            the use of the same state multiple times.

        Returns
        -------
        tuple

        """
        def get_action(action):
            return "_".join([str(y) for y in action if y]) if isinstance(action, list) else str(action)
        # end get_action

        if isinstance(state_numbers, set) is False:
            raise Exception("state_numbers should be of type set.")
        # end if

        inputs = list()
        current_state = None
        operation = get_action(sequence[-1])
        if self.final_states.get(operation, False) is not False:
            for fs in self.final_states[operation]:
                if fs.name == operation and not fs.next:
                    current_state = fs
                    inputs.append(operation)
                    break
                # end if
            # end for
        # end if

        stopped_at_index = None
        if current_state:
            sequence_len = len(sequence)
            stopped_at_index = sequence_len - 1
            for index in range(-2, -sequence_len, -1):
                operation = get_action(sequence[index])
                # There should only be one final state with the same action name
                found = current_state.find_previous(operation, str(), True)
                # Do not reuse states that were already used.
                if found and found[0].number in state_numbers:
                    found = list()
                # end if
                if self.build_with_loop is True and not found:
                    if isinstance(current_state, Navigator) is True and current_state.name == operation:
                        current_state.is_self_loop = True
                        if current_state.loop_count == 0:
                            current_state.loop_count += 2
                        # end if
                        found = [current_state]
                    # end if
                # end if
                if not found:
                    break
                else:
                    current_state = found[0]
                    stopped_at_index = sequence_len + index
                    inputs.insert(0, operation)
                # end if
            # end for
        # end if
        return current_state, stopped_at_index, inputs
    # end _factorize_suffixes

    # %%
    def get_pta_content(self, include_root: bool = True):
        graph = ""
        if include_root is True:
            graph = self.root.get_content_as_graph()
        # end if
        for _, states in self.alphabet.items():
            for nav in states:
                nav_content = nav.get_content_as_graph()
                graph += nav_content
            # end for
        # end for
        graph = "digraph {\ngraph [rankdir=LR];\n" + graph + "}"
        return graph
    # end get_pta_content

    def display_graph(self):
        content = self.get_pta_content(include_root=True)
        graph = graphviz.Source(content)
        graph.render(view=True, filename=tempfile.mktemp(".png"))
    # end display_graph

# end class PrefixSuffixFactorizedModel

