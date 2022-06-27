#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 16 2021

@author: Vahana Dorcis
"""


class Navigator(object):

    def __init__(self, name: str, is_start: bool = False, is_final_state: bool = False, description=str(),
                 number: int = 0):
        self.name = name
        self.description = description
        self.previous = list()
        self.next = list()
        self.is_start = is_start
        self.is_final_state = is_final_state
        self.is_self_loop = False
        self.loop_count = 0
        self.number = number
        self.other_names = set()
        self.highlight = False
    # end __init__

    def __str__(self):
        content = f"name: {self.name}, description: {self.description}"
        content += f", Is Start: {self.is_start}"
        content += f", Is Final State: {self.is_final_state}"
        content += f", Is self loop: {self.is_self_loop}, loop count: {self.loop_count}"
        content += f", Number: {self.number}"
        return content
    # end __str__

    def __eq__(self, other):
        if isinstance(other, Navigator) is False:
            return False
        # end if
        # if self.arrival != other.arrival or self.outgoing != other.outgoing:
        #     return False
        # # end if
        if self.name != other.name:
            return False
        # end if
        if (self.previous and not other.previous) or (other.previous and not self.previous):
            return False
        # end if
        if len(self.previous) != len(other.previous):
            return False
        # end if
        if self.previous[0].name != other.previous[0].name:
            return False
        # end if
        if (self.next and not other.next) or (other.next and not self.next):
            return False
        # end if
        if other.number in [a.number for a in self.next] or self.number in [a.number for a in other.next]:
            return False
        # end if
        # See if both states have at least one destination in common
        destination, destination_other = False, False
        for a in self.next:
            if a.name in [b.name for b in other.next]:
                destination = True
                break
            # end if
        # end for
        for a in other.next:
            if a.name in [b.name for b in self.next]:
                destination_other = True
                break
            # end if
        # end for
        if destination is False and destination_other is False and (len(self.next) > 0 or len(other.next) > 0):
            return False
        # end if
        return destination == destination_other
    # end __eq__

    def build_sequences_from_name(self) -> set:
        if self.is_self_loop is True and self.loop_count == 0:
            # When there is a loop, there has to be at least 2 counts
            self.loop_count = 2
        # end if
        sequences = set()
        names = self.other_names.copy()
        names.add(self.name)
        for name in names:
            if not name:
                continue
            # end if
            # sequences.add(tuple([name]) if self.is_self_loop is False else tuple([name] * self.loop_count))
            sequences.add(tuple([name]))
            for i in range(2, self.loop_count + 1):
                sequences.add(tuple([name] * i))
            # end for
        # end for
        return sequences
    # end build_sequences_from_name

    def make_quick_copy(self):
        nav = Navigator(
            name=self.name, description=self.description, is_start=self.is_start,
            is_final_state=self.is_final_state
        )
        nav.number = self.number
        return nav
    # end make_quick_copy

    @staticmethod
    def is_navigator(other):
        if isinstance(other, Navigator) is False:
            raise TypeError("other should be of type Navigator.")
        # end if
        return True
    # end is_navigator

    def update_next(self, other, remove: bool):
        self.is_navigator(other)
        if isinstance(remove, bool) is False:
            raise TypeError("remove should be of type bool.")
        # end if
        if remove is False and other.number not in [o.number for o in self.next]:
            if self.number == other.number:
                self.is_self_loop = True
                self.loop_count += 1
            else:
                self.next.append(other)
            # end if
        # end if
        if remove is True:
            for idx in range(len(self.next)):
                if other.number == self.next[idx].number:
                    self.next.pop(idx)
                    break
                # end if
            # end for
        # end if
    # end update_next

    def update_previous(self, other, remove: bool):
        self.is_navigator(other)
        if isinstance(remove, bool) is False:
            raise TypeError("remove should be of type bool.")
        # end if
        if remove is False and other.number not in [o.number for o in self.previous]:
            if self.number == other.number:
                self.is_self_loop = True
                self.loop_count += 1
            else:
                self.previous.append(other)
            # end if
        # end if
        if remove is True:
            for idx in range(len(self.previous)):
                if other.number == self.previous[idx].number:
                    self.previous.pop(idx)
                    break
                # end if
            # end for
        # end if
    # end update_previous

    def get_content_as_graph(self) -> str:
        """
        Return the content of the object as vertices in a tree.

        Returns
        -------
        str
        """
        def get_state_name(item: Navigator):
            """ Return the name to use for the state. """
            return f'"{item.number}"'
        # end get_state_name

        def add_legend() -> str:
            legend = str()
            if self.is_final_state is True and self.is_start is True:
                legend = ' [shape = diamond, peripheries = 2'
            elif self.is_final_state is True:
                legend = ' [peripheries = 2'
            elif self.is_start is True:
                legend = ' [shape = diamond'
            # end if
            if self.highlight is True:
                legend = f"{legend}, " if legend else " ["
                legend += "color=Orange, fontcolor=White, fillcolor=Orange, style=filled"
            # end if
            return get_state_name(self) + legend + "];\n" if legend else str()
        # end add_legend

        content = ""
        s_name = get_state_name(self)
        current_name = self.name
        if self.other_names:
            current_name += f", {', '.join(self.other_names)}"
        # end if
        if self.is_self_loop is True:
            content += f'{s_name} -> {s_name} [label="{self.description if self.description else self.name}"];\n'
        # end if
        alt_name = f'"{self.number}_a"'
        if len(self.previous) > 1:
            content += f"{alt_name} [shape=point, width=0.01, height=0.01];\n"
            content += f'{alt_name} -> {s_name} [label="{current_name}"];\n'
            s_name = alt_name
        # end if

        for nav in self.previous:
            # Get the state name of the current object
            name = get_state_name(nav)
            label = f' [label="{current_name}'
            if self.description:
                label += " " + self.description
            # end if
            label += '"]'
            if s_name == alt_name:
                label = ' [dir=none]'
            # end if
            if nav.name == s_name:
                label = str()
            # end if
            content += f"{name} -> {s_name}{label};\n"
        # end for
        # for nav in self.next:
        #     # Get the state name of the current object
        #     name = get_state_name(nav)
        #     label = f' [label="{nav.name}'
        #     if include_count is True:
        #         label += f' [{self.get_outgoing_count(nav.name)}]'
        #         if self.get_outgoing_count(nav.name) == 0:
        #             cnt = 0
        #             for n in nav.name.split("\n"):
        #                 cnt += self.get_outgoing_count(n)
        #             # end for
        #             label = f' [label="{nav.name} [{cnt}]'
        #             if nav.name != s_name:
        #                 label += f"{nav.name} "
        #             # end if
        #             label += f"[{cnt}]"
        #         # end if
        #     # end if
        #     label += '"]'
        #     if nav.name == s_name:
        #         label = str()
        #     # end if
        #     content += f"{s_name} -> {name}{label};\n"
        # # end for
        content += add_legend()
        return content
    # end get_content_as_graph

    @staticmethod
    def find_items(name: str, description: str, navigators: list, stop_at_one: bool = False) -> list:
        if not navigators or isinstance(navigators, list) is False:
            return list()
        # end if
        if name and isinstance(name, str) is False:
            raise TypeError("name should be of type str.")
        # end if
        if name == str():
            name = None
        # end if
        if description and isinstance(description, str) is False:
            raise TypeError("description should be of type str.")
        # end if
        if description == str():
            description = None
        # end if
        found = list()
        for nav in navigators:
            is_found = False
            if name and (name == nav.name or name in nav.other_names):
                is_found = True
            elif name:
                continue
            # end if
            if description and description == nav.description:
                is_found = True
            elif description:
                continue
            # end if
            if is_found:
                found.append(nav)
                if stop_at_one is True:
                    break
                # end if
            # end if
        # end for
        return found
    # end find_items

    def find_previous(self, name: str, description: str, stop_at_one: bool = False):
        if not self.previous:
            return list()
        return self.find_items(
            name=name, description=description, navigators=self.previous,
            stop_at_one=stop_at_one)
    # end find_previous

    def find_next(self, name: str, description: str, stop_at_one: bool = False):
        if not self.next:
            return list()
        return self.find_items(
            name=name, description=description, navigators=self.next,
            stop_at_one=stop_at_one)
    # end find_next

    def remove_child(self, name: str, description: str):
        if not name and not description:
            return
        # end if
        children = list()
        for child in self.next:
            if name and description:
                if child.name == name and child.description == description:
                    continue
                # end if
            elif name:
                if child.name == name:
                    continue
                # end if
            elif description:
                if child.description == description:
                    continue
                # end if
            # end if
            children.append(child)
        # end for
        self.next = children
    # end remove_child

# end class Navigator

