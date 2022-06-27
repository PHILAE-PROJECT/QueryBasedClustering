#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  27 23:40:00 2020

@author: Vahana Dorcis
"""


class SequencesStringComparisonClustering(object):
    """
    The algorithm creates the clusters based on the homogeneity of the items in the data.
    The data is a set of lists of lists called sequences. A sequence is a list of string
    or couple that represents the actions or steps taken by a user or bot during the
    usage of an application.
    The clusters are created by comparing the steps taken in each sequence to the
    steps taken in the other sequences. Two sequences are the same if the steps
    taken in both are identical. The definition of identical is controlled by the
    tuning parameters. Identical could mean:
    same steps in the same order with same number of steps,
    or same steps in the same order with different number of steps,
    or same steps in different order with same number of steps,
    or same steps in different order with different number of steps.
    The recurring criteria, homogeneity which is the basis of the algorithm is "same steps".

    Outcome:
    Let us denote C for cluster, S for sequence, and A the steps taken in the sequences.
    A cluster is a set of sequences: C = {S1, S2,..., Sn}  # C = {x | 1 <= x <= n S}
    A sequence is a set of steps: S = {A1, A2,..., An}
    A cluster is never empty: C ≠ ∅, it has to have at least 1 sequence |C| >= 1.
    For each sequence in a cluster, the set of steps in the sequence is equivalent to the
    set of steps of any sequence in the cluster. ∀ S ∈ C, AS <-> AS' where S' is any
    sequence in the cluster that is not the current sequence S.
    """
    @staticmethod
    def are_patterns_similar(pattern1: list, pattern2: list, consider_order_of_sequence: bool = True) -> bool:
        if isinstance(consider_order_of_sequence, bool) is False:
            raise TypeError("consider_order_of_sequence should be of type bool.")
        # end if
        if isinstance(pattern1, list) is False or isinstance(pattern2, list) is False:
            raise TypeError("The patterns should be of type list.")
        # end if
        if not pattern1 or not pattern2:
            return False
        # end if
        if pattern1 == pattern2:
            return True
        # end if
        if len(pattern1) != len(pattern2):
            return False
        # end if
        if consider_order_of_sequence is False:
            return sorted(pattern1) == sorted(pattern2)
        else:
            for idx, pat in enumerate(pattern1):
                if pat != pattern2[idx]:
                    return False
                # end if
            # end for
        # end if
        return True
    # end are_patterns_similar

    @staticmethod
    def _helper_validate_pattern_inputs(subsequence_size: int, consider_order_of_sequence: bool,
                                        consider_immediate_occurrence: bool, consider_duplicate_values: bool,
                                        immediate_occurrence_max: int) -> bool:
        """
        Validate the inputs parameters and throw a TypeError
        exception if one of the parameters does not meet the
        expected Type.

        Raises
        ------
        TypeError
            Raised when one of the input parameters is not
            the right type.

        Returns
        -------
        bool
        """
        if isinstance(subsequence_size, int) is False:
            raise TypeError("subsequence_size should be of type int.")
        # end if
        if isinstance(consider_order_of_sequence, bool) is False:
            raise TypeError("consider_order_of_sequence should be of type bool.")
        # end if
        if isinstance(consider_immediate_occurrence, bool) is False:
            raise TypeError("consider_immediate_occurrence should be of type bool.")
        # end if
        if isinstance(consider_duplicate_values, bool) is False:
            raise TypeError("consider_duplicate_values should be of type bool.")
        # end if
        if isinstance(immediate_occurrence_max, int) is False:
            raise TypeError("immediate_occurrence_max should be of type int.")
        # end if
        return True
    # end _helper_validate_pattern_inputs

    @staticmethod
    def create_pattern(
            from_sequence: list, subsequence_size: int, consider_order_of_sequence: bool = True,
            consider_immediate_occurrence: bool = True, consider_duplicate_values: bool = True,
            immediate_occurrence_max: int = 2
    ) -> tuple:
        """
        Create pattern and subsequences from the sequence provided.

        Parameters
        ----------
        from_sequence : list
            The sequence to use to create the pattern.

        subsequence_size : int
            The size of each subsequence extracted from the from_sequence.
            Set to 1 for normal processing.

        consider_order_of_sequence : bool, optional
            When True, the patterns will be created using the sequence
            as provided, otherwise the sequence will be sorted before
            processing. The default is True.

        consider_immediate_occurrence : bool, optional
            When False, if the same value occurs more than once in a row,
            only one is kept.
            Example: Given A = ["a", "a", "a", "b", "c", "a", "a", "a"]
            A becomes ["a", "b", "c", "a"] if False, otherwise A stays
            the same.
            If consider_duplicate_values is False and
            consider_immediate_occurrence is True then the number of
            back to back occurrence of the same value is capped at
            immediate_occurrence_max.

        consider_duplicate_values : bool, optional
            When False, only one value of the same is kept.
            When False, and consider_immediate_occurrence is True,
            the same value kept does not exceed
            immediate_occurrence_max.
            When True, all the values are kept depending on the
            value of consider_immediate_occurrence.

        immediate_occurrence_max : int, optional
            The number of back to back matching value to keep. It is
            only used if consider_immediate_occurrence is True.
            The default and minimum value is 2.

        Raises
        ------
        TypeError
            Raised when one of the input parameters is not the right type.

        Returns
        -------
        tuple (
            patterns : list
                The patterns created using the input values.
            subsequences : list
                Equals to patterns if subsequence_size == 1.
        )
        """
        if not from_sequence or isinstance(from_sequence, list) is False:
            raise TypeError("from_sequence should be a non-empty list.")
        # end if
        if not subsequence_size:
            subsequence_size = 1
        # end if
        _ = SequencesStringComparisonClustering._helper_validate_pattern_inputs(
                subsequence_size=subsequence_size, consider_order_of_sequence=consider_order_of_sequence,
                consider_immediate_occurrence=consider_immediate_occurrence,
                consider_duplicate_values=consider_duplicate_values, immediate_occurrence_max=immediate_occurrence_max
        )
        if immediate_occurrence_max < 2:
            immediate_occurrence_max = 2
        # end if
        subsequences, patterns = list(), list()
        sequence_copy = from_sequence.copy()
        if consider_order_of_sequence is False:
            sequence_copy = sorted(from_sequence)
        # end if
        # Go through the content of the from_sequence
        for fs_item in sequence_copy:
            if consider_immediate_occurrence is False:
                # Back to back values are not considered, therefore
                # move on if the current value is the same as the last one.
                if patterns and fs_item == patterns[-1]:
                    continue
                # end if
            # end if
            if consider_duplicate_values is False and fs_item in patterns:
                if consider_immediate_occurrence is True:
                    if len(patterns) >= immediate_occurrence_max:
                        compare_to = [fs_item] * immediate_occurrence_max
                        if patterns[-immediate_occurrence_max:] == compare_to:
                            continue
                        # end if
                    # end if
                else:
                    continue
                # end if
            # end if
            # Add the item
            patterns.append(fs_item)

            if subsequence_size <= 1:
                subsequences.append(fs_item)
            else:
                p_size = len(patterns)
                if p_size == subsequence_size:
                    subsequences.append(patterns[:subsequence_size])
                elif p_size > subsequence_size:
                    subsequence = patterns[-subsequence_size + 1] + [fs_item]
                    # Only keep unique values
                    if subsequence not in subsequences:
                        subsequences.append(subsequence)
                    # end if
                # end if
            # end if
        # end for from_sequence
        return patterns, subsequences
    # end create_pattern

    # %%
    @staticmethod
    def create_clusters(
            sequences: list, subsequence_size: int = 1, consider_order_of_sequence: bool = True,
            consider_immediate_occurrence: bool = True, consider_duplicate_values: bool = True,
            immediate_occurrence_max: int = 2
    ) -> tuple:
        if not subsequence_size:
            subsequence_size = 1
        # end if
        _ = SequencesStringComparisonClustering._helper_validate_pattern_inputs(
                subsequence_size=subsequence_size, consider_order_of_sequence=consider_order_of_sequence,
                consider_immediate_occurrence=consider_immediate_occurrence,
                consider_duplicate_values=consider_duplicate_values, immediate_occurrence_max=immediate_occurrence_max
        )
        if immediate_occurrence_max < 2:
            immediate_occurrence_max = 2
        # end if
        # Holds the extracted subsequences
        dict_patterns = dict()
        # Holds the clustering result
        column_sequence = "Sequences"
        column_sequence_pattern = "Sequences Pattern"
        column_cluster_number = "Cluster Number"
        cluster_columns = [column_sequence, column_sequence_pattern, column_cluster_number]
        cluster_values = list()
        for sequence in sequences:
            # Create a pattern
            pattern_result = SequencesStringComparisonClustering.create_pattern(
                from_sequence=sequence, subsequence_size=subsequence_size,
                consider_order_of_sequence=consider_order_of_sequence,
                consider_immediate_occurrence=consider_immediate_occurrence,
                consider_duplicate_values=consider_duplicate_values, immediate_occurrence_max=immediate_occurrence_max
            )
            patterns, subsequences = pattern_result
            # Holds the cluster number
            cluster_number = 0
            if not dict_patterns:
                dict_patterns = {cluster_number: (subsequences, [sequence])}
            else:
                has_pattern = False
                for number, values in dict_patterns.items():
                    if SequencesStringComparisonClustering.are_patterns_similar(
                        pattern1=subsequences, pattern2=values[0],
                        consider_order_of_sequence=consider_order_of_sequence
                    ) is True:
                        has_pattern = True
                        cluster_number = number
                        # Update the dictionary
                        new_values = (subsequences, values[1] + [sequence])
                        dict_patterns[cluster_number] = new_values
                        break
                    # end if
                # end for
                if has_pattern is False:
                    cluster_number = len(dict_patterns)
                    dict_patterns[cluster_number] = (subsequences, [sequence])
                # end if
            # end if
            # Store the clustering result
            cluster_row = [None] * len(cluster_columns)
            cluster_row[cluster_columns.index(column_cluster_number)] = cluster_number
            cluster_row[cluster_columns.index(column_sequence_pattern)] = patterns
            cluster_row[cluster_columns.index(column_sequence)] = sequence
            cluster_values.append(cluster_row)
        # end for sequences
        cluster_size = len(dict_patterns)
        return cluster_columns, cluster_values, cluster_size, dict_patterns
    # end create_clusters

# end SequencesStringComparisonClustering
