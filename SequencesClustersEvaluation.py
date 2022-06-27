#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 10:08:04 2020

@author: Vahana Dorcis
"""
import pdb
import warnings


class SequencesClustersEvaluation(object):

    @staticmethod
    def find_largest_subsequence_index(subsequence: list, sequence: list) -> tuple:
        # Validate inputs
        if (isinstance(subsequence, list) is False or isinstance(sequence, list) is False
                or not subsequence or not sequence):
            raise Exception("subsequence and sequence should be of type list and not empty.")
        # end if
        # Holds the length of the subsequence
        subsequence_size = len(subsequence)
        # Check the size of the subsequence
        if subsequence_size <= 1 or subsequence[0] not in sequence:
            return None
        # end if
        # Compare both items
        if subsequence == sequence:
            return [(0, subsequence_size)], 0, subsequence_size
        # end if
        # Holds the search index
        search_index = 0
        best_index = None  # The index where the most items was found
        best_number_items = None  # The number of items found
        # Holds the length of the sequence
        sequence_size = len(sequence)
        while subsequence[0] in sequence[search_index:]:
            # Get the index of the first item
            index = sequence[search_index:].index(subsequence[0])
            # Update the index
            index += search_index
            # Update the size of the sequence
            seq_size = sequence_size - index
            # Holds the number of items found
            items_found = 1
            if subsequence == sequence[index:]:
                items_found = subsequence_size
            else:
                for i in range(1, subsequence_size):
                    if i >= seq_size or subsequence[i] != sequence[i + index]:
                        break
                    # end if
                    items_found += 1
                # end for
            # end if
            if best_index is None or best_number_items < items_found:
                best_index = index
                best_number_items = items_found
            # end if
            # When the number of items found is greater than the remaining items,
            # stop the search
            if best_number_items >= seq_size:
                break
            # end if
            # Increment the search index by 1
            search_index = index + 1
        # end while
        return best_index, best_number_items
    # end find_largest_subsequence_index

    # %%
    @staticmethod
    def remove_back_to_back_repetitions(sequence: list) -> list:
        """
        Create a new sequence that is a copy of the current one
        but without the back to back repetitions.

        Parameters
        ----------
        sequence: list
            The sequence to modify.

        Returns
        -------
        list (A new sequence without the back to back repetitions)
        """
        if isinstance(sequence, list) is False:
            raise TypeError("sequence should be of type list")
        # end if
        if not sequence:
            return sequence
        # end if
        new_sequence = [sequence[0]]
        for s in sequence[1:]:
            if s != new_sequence[-1]:
                new_sequence.append(s)
            # end if
        # end for
        return new_sequence
    # end remove_back_to_back_repetitions

    # %%
    @staticmethod
    def calculate_dissimilarity_shift_indexes(sequence1: list, sequence2: list) -> tuple:
        """
        Compare the sequences by comparing each of their items. The score
        returned is the size of the union of the missing items. The order in
        which the items appear is considered but the repetitions are ignored.
        The comparison is done using the indexes of the items, when an item is
        not found, a shift in index occurs to see if the item can be found.

        Parameters
        ----------
        sequence1 : list
            The list containing the items to compare.

        sequence2 : list
            The list containing the items to compare.

        Returns
        -------
        tuple
            (The number of missing items: int, the missing items: list)

        """
        # Validate the inputs
        if isinstance(sequence1, list) is False or isinstance(sequence2, list) is False:
            raise Exception("The inputs should be of type list and not empty.")
        # end if
        if sequence1 == sequence2:
            return 0, list()
        # end if
        # Holds the remaining sequences
        shortest, longest = None, None
        # Get the length of the sequences
        len_seq1 = len(sequence1)
        len_seq2 = len(sequence2)
        if len_seq1 > len_seq2:
            longest = sequence1.copy()
            shortest = sequence2.copy()
        else:
            shortest = sequence1.copy()
            longest = sequence2.copy()
        # end if

        # Holds the last items removed from the sequences
        shifted_items = list()  # Holds the items that were shifted
        missing_items = list()  # Holds the items that are not in both sequences

        while shortest:
            # Compare the sequences
            if shortest == longest:
                shortest = list()
                longest = list()
                # Stop here since they are equal
                continue
            # end if
            # Get the first item of the shortest sequence
            current_item = shortest[0]

            if longest and current_item == longest[0]:
                # Remove the item found from the longest sequence
                longest = longest[1:]
            else:
                if current_item not in longest:
                    # Add the missing item
                    missing_items.append(current_item)
                else:
                    # Search for a subsequence in the longest sequence
                    search = SequencesClustersEvaluation.find_largest_subsequence_index(
                        subsequence=shortest, sequence=longest)
                    # If there is a subsequence, remove them
                    if search is not None:
                        index, number_items = search
                        # Holds the subsequence that was shifted
                        shifted = shortest[:number_items]
                        shifted_items.append(shifted)
                        # Remove the subsequence from the shortest sequence
                        shortest = shortest[number_items:]
                        # Get the ending part of the longest sequence
                        part2 = longest[index + number_items:]
                        # Remove the subsequence from the longest sequence
                        longest = longest[:index] + part2
                        if not shortest and longest:
                            shifted_items.append(longest)
                            longest = list()
                        # end if
                        continue
                    else:
                        longest.remove(current_item)
                        shifted_items.append(current_item)
                    # end if
                # end if
            # end if
            # Remove the item from the shortest sequence
            shortest = shortest[1:]
        # end while
        for item in shortest + longest:
            missing_items.append(item)
        # end for
        # Holds the number of missing items
        missing_score = len(missing_items) + len(shifted_items)
        return missing_score, missing_items
    # end calculate_dissimilarity_shift_indexes

    @staticmethod
    def homogeneity_evaluation(sequence1: list, sequence2: list) -> tuple:
        if isinstance(sequence1, list) is False or isinstance(sequence2, list) is False:
            raise TypeError("The inputs should be of type list.")
        # end if
        # Make a copy to avoid modifying the original sequences
        copy1 = sequence1.copy()
        copy2 = sequence2.copy()
        if copy1 == copy2:
            return 0, list()
        # end if
        # Holds the missing items
        missing = list()
        while copy1 and copy2:
            if copy1 == copy2:
                copy1, copy2 = list(), list()
                break
            # end if
            current = copy1[0]
            is_missing = True
            while current in copy2:
                is_missing = False
                copy2.remove(current)
            # end while
            while current in copy1:
                copy1.remove(current)
            # end while
            if is_missing is True and current not in missing:
                missing.append(current)
            # end if
        # end while
        for item in copy1 + copy2:
            if item not in missing:
                missing.append(item)
            # end if
        # end for
        return len(missing), missing
    # end homogeneity_evaluation

    @staticmethod
    def disparity_evaluation(sequence1: list, sequence2: list):
        if isinstance(sequence1, list) is False or isinstance(sequence2, list) is False:
            raise TypeError("The inputs should be of type list.")
        # end if
        if sequence1 == sequence2:
            return 0, list()
        # end if
        len1, len2 = len(sequence1), len(sequence2)
        seq_short, seq_long = sequence1.copy(), sequence2.copy()
        if len2 < len1:
            seq_long = seq_short
            seq_short = sequence2.copy()
        # end if
        # Holds the missing items
        missing, subsequences_shifted = list(), list()
        # count1, count2 = 0, 0
        while seq_short:
            if seq_short == seq_long:
                seq_short, seq_long = list(), list()
                break
            # end if
            do_search = False
            if seq_short[0] == seq_long[0]:
                if len(seq_short) == 1:
                    seq_long = seq_long[1:]
                elif len(seq_long) > 1 and seq_short[0] in seq_long[1:]:
                    # See if there is a longer subsequence
                    do_search = True
                else:
                    seq_long = seq_long[1:]
                # end if
            elif seq_short[0] in seq_long:
                if len(seq_short) == 1:
                    seq_long.remove(seq_short[0])
                    subsequences_shifted.append(seq_short[0])
                    seq_short = list()
                else:
                    do_search = True
                # end if
            else:
                missing.append(seq_short[0])
            # end if
            if do_search is True:
                # start_time1 = time.time()
                search_result = SequencesClustersEvaluation.find_largest_subsequence_index(seq_short, seq_long)
                if search_result is not None:
                    best_index, subsequence_size = search_result
                    # Holds the subsequence to shift
                    shifted = seq_short[:subsequence_size]
                    if best_index > 0:
                        subsequences_shifted.append(shifted)
                    # end if
                    seq_short = seq_short[subsequence_size:]
                    seq_long = seq_long[:best_index] + seq_long[best_index + subsequence_size:]
                else:
                    pdb.set_trace()
                # end if
            else:
                seq_short = seq_short[1:]
            # end if
        # end while
        for item in seq_short + seq_long:
            if item not in missing:
                missing.append(item)
            # end if
        # end for
        return len(missing + subsequences_shifted), missing
    # end disparity_evaluation

    @staticmethod
    def predecessors_evaluation(
            sequence1: list, sequence2: list, remove_immediate_occurrences: bool = True, final_states: list = None
    ) -> tuple:
        """
        Evaluate the predecessors of the sequences in relation to the final states.
        The immediate occurrences (back to back repetition) are eliminated before
        comparing the predecessors. If the homogeneity score is not 0, the predecessors
        evaluation is not done.

        Returns
        -------
        tuple (int: The homogeneity score, int: the predecessors evaluation score)

        """
        if isinstance(sequence1, list) is False or isinstance(sequence2, list) is False:
            raise TypeError("The inputs should be of type list.")
        # end if
        if sequence1 == sequence2:
            return 0, 0
        # end if
        homogeneity = SequencesClustersEvaluation.homogeneity_evaluation(sequence1, sequence2)
        if homogeneity[0] > 0:
            return homogeneity[0], 1
        # end if
        seq1, seq2 = list(), list()
        if remove_immediate_occurrences is True:
            # Make a copy of sequence1 without repetition
            seq1 = SequencesClustersEvaluation.remove_back_to_back_repetitions(sequence1)
            # Make a copy of sequence2 without repetition
            seq2 = SequencesClustersEvaluation.remove_back_to_back_repetitions(sequence2)
        else:
            seq1 = sequence1.copy()
            seq2 = sequence2.copy()
        # end if
        # If the length of the sequences after transformation is not the same, move on
        if len(seq1) != len(seq2):
            return homogeneity[0], 1
        # end if
        if seq1 == seq2:
            return homogeneity[0], 0
        # end if
        if final_states is None or not final_states:
            final_states = [seq1[-1]]
            if seq2[-1] not in final_states:
                final_states.append(seq2[-1])
            # end if
        # end if
        for fs in final_states:
            predecessor1, has_fs1 = list(), False
            remaining = seq1.copy()
            while fs in remaining:
                index = remaining.index(fs)
                predecessor1.append([remaining[:index]])
                remaining = remaining[index+1:]
                has_fs1 = True
            # end while
            predecessor2, has_fs2 = list(), False
            remaining = seq2.copy()
            while fs in remaining:
                index = remaining.index(fs)
                predecessor2.append([remaining[:index]])
                remaining = remaining[index + 1:]
                has_fs2 = True
            # end while
            if has_fs1 != has_fs2:
                # If they don't match, it means one has the state and the other doesn't.
                return homogeneity[0], 1
            # end if
            if predecessor1 != predecessor2:
                return homogeneity[0], 1
            # end if
        # end for
        return homogeneity[0], 0
    # end predecessors_evaluation

    @staticmethod
    def evaluate_sequences(
            one: list, to_many: list, eval_homogeneity: bool = True, eval_disparity: bool = True,
            memoization: dict = None) -> tuple:
        # Holds the unique sequences
        unique_sequences = list()
        key_seq = "unique_sequences"
        if memoization and isinstance(memoization, dict) is True:
            if key_seq in memoization.keys():
                unique_sequences = memoization[key_seq]
            # end if
        else:
            memoization = dict()
        # end if
        if one not in unique_sequences:
            unique_sequences.append(one)
        # end if
        # Holds the memoization key for one
        memo_key1 = str(unique_sequences.index(one))
        # Holds the dictionary keys
        key_sh, key_sd = "homogeneity", "disparity"
        key_has_key = "has_key"

        def calculate_scores(current_sequence: list) -> dict:
            if memo_key in memoization:
                score_memo = memoization[memo_key]
                return {key_has_key: True, key_sh: score_memo[0], key_sd: score_memo[1]}
            # end if
            scores = {key_has_key: False, key_sh: None, key_sd: None}
            if eval_homogeneity is True:
                score_h = SequencesClustersEvaluation.homogeneity_evaluation(one, current_sequence)
                scores[key_sh] = score_h[0]
            # end if
            if eval_disparity is True:
                score_d = SequencesClustersEvaluation.disparity_evaluation(one, current_sequence)
                scores[key_sd] = score_d[0]
            # end if
            return scores
        # end calculate_scores

        # Holds the scores
        result_sh, result_sd = list(), list()
        for sequence in to_many:
            # Add the sequence to the unique sequences
            if sequence not in unique_sequences:
                unique_sequences.append(sequence)
            # end if
            # Holds the memoization key for the sequences
            memo_key2 = str(unique_sequences.index(sequence))
            memo_key = f"{memo_key1}->{memo_key2}"
            # Get the scores and assign the values
            eval_scores = calculate_scores(sequence)
            if eval_scores[key_sh] is not None:
                result_sh.append(eval_scores[key_sh])
            if eval_scores[key_sd] is not None:
                result_sd.append(eval_scores[key_sd])
            if eval_scores[key_has_key] is False:
                memoization[memo_key] = [eval_scores[key_sh], eval_scores[key_sd]]
            # end if
        # end for to_many
        scores_homogeneity, scores_disparity = None, None
        if result_sh:
            scores_homogeneity = [min(result_sh), max(result_sh)]
        # end if
        if result_sd:
            scores_disparity = [min(result_sd), max(result_sd)]
        # end if
        memoization[key_seq] = unique_sequences
        return scores_homogeneity, scores_disparity, memoization
    # end evaluate_sequences

    @staticmethod
    def evaluate_cluster(
            cluster: list, eval_homogeneity: bool = True, eval_disparity: bool = True,
            eval_disparity_if_homogeneity_is_zero: bool = True, memoization: dict = None) -> tuple:
        """
        Calculate the Condition 1 (C1),
        Condition 2 (C2) scores of the cluster.

        Parameters
        ----------
        cluster : list
            A list of sequences (list) in the cluster.
        eval_homogeneity : bool, optional
            When True, will calculate the homogeneity score.
            The default is True.
        eval_disparity : bool, optional
            When True, will calculate the disparity score.
            The default is True.
        eval_disparity_if_homogeneity_is_zero : bool, optional
            When True, disparity will be calculated only if homogeneity == 0.
            The default is True.
        memoization : dict, optional
            This is used for faster computing. It only helps if there are duplicates of the sequences.
            The default is None.

        Returns
        -------
        scores_homogeneity : list (None if eval_homogeneity is False.)
            [minimum, maximum, average] scores.
        scores_disparity : list (None if disparity was not calculated.)
            [minimum, maximum, average] scores.

        """
        cluster_size = len(cluster)
        if cluster_size <= 1:
            return None, None, None, memoization
        # end if
        if not memoization or isinstance(memoization, dict) is False:
            memoization = dict()
        # end if
        scores_homogeneity = None if eval_homogeneity is False else [0.0, 0.0, 0.0]
        scores_disparity = None if eval_disparity is False else [0.0, 0.0, 0.0]
        # Compute the number of comparison to be done
        n_comparison = cluster_size * (cluster_size - 1)  # - 1 because of the inner loop
        for outer in range(cluster_size):
            sequence_outer = cluster[outer]
            if outer < cluster_size:
                sequence_remaining = cluster[outer + 1:]
                if not sequence_remaining:
                    continue
                # end if
                scores_h, scores_d, memoization = SequencesClustersEvaluation.evaluate_sequences(
                    one=sequence_outer, to_many=sequence_remaining, eval_homogeneity=eval_homogeneity,
                    eval_disparity=eval_disparity, memoization=memoization)
                if scores_homogeneity is not None and scores_h is not None:
                    scores_homogeneity[0] += min(scores_h)
                    scores_homogeneity[1] += max(scores_h)
                # end if
                if scores_disparity is not None and scores_d is not None:
                    if eval_disparity is True and eval_disparity_if_homogeneity_is_zero is True:
                        if max(scores_d) > 0:
                            eval_disparity = False
                            scores_disparity = None
                            continue
                        # end if
                    # end if
                    scores_disparity[0] += min(scores_d)
                    scores_disparity[1] += max(scores_d)
                # end if
            # end if
        # end for outer
        for s in [scores_homogeneity, scores_disparity]:
            if s:
                s[0] /= n_comparison
                s[1] /= n_comparison
                s[2] = (s[0] + s[1]) / 2
            # end if
        # end for
        return scores_homogeneity, scores_disparity, memoization
    # end evaluate_cluster

    @staticmethod
    def evaluate_model(
            model: list, eval_homogeneity: bool = True, eval_disparity: bool = True,
            eval_disparity_if_homogeneity_is_zero: bool = True, memoization: dict = None
    ) -> tuple:
        """


        Parameters
        ----------
        model : list
            DESCRIPTION.
        eval_homogeneity : bool, optional
            When True, will calculate the homogeneity score.
            The default is True.
        eval_disparity : bool, optional
            When True, will calculate the disparity score.
            The default is True.
        eval_disparity_if_homogeneity_is_zero : bool, optional
            When True, disparity will be calculated only if homogeneity == 0.
            The default is True.
        memoization : dict, optional
            This is used for faster computing. It only helps
            if there are duplicates of the sequences.
            The default is None.

        Raises
        ------
        Exception
            Raised when a there is a type mismatch.

        Returns
        -------
        scores_result : tuple
            (dict : [[min, max, average], [non-zero clusters]],
            homogeneity key, predecessor key, disparity key).

        """
        model_size = len(model)
        # Holds the keys
        key_h, key_d = "homogeneity", "disparity"
        if model_size <= 1:
            return {key_d: None, key_h: None}, key_h, key_d, memoization
        # end if
        # Holds the scores
        model_scores = {key_h: [[0.0, 0.0, 0.0], list()], key_d: [[0.0, 0.0, 0.0], list()]}
        if eval_homogeneity is False:
            model_scores[key_h] = None
        # end if
        if eval_disparity is False:
            model_scores[key_d] = None
        # end if
        size1_clusters = 0  # Holds the number of clusters of size 1
        for _, cluster in enumerate(model):
            if not cluster or isinstance(cluster, list) is False:
                raise TypeError("The items in the model should be non-empty and of type list.")
            # end if
            if len(cluster) == 1:
                size1_clusters += 1
                continue
            # end if
            scores_homogeneity, scores_disparity, memoization = SequencesClustersEvaluation.evaluate_cluster(
                cluster=cluster, eval_homogeneity=eval_homogeneity, memoization=memoization,
                eval_disparity=eval_disparity,
                eval_disparity_if_homogeneity_is_zero=eval_disparity_if_homogeneity_is_zero)
            if scores_homogeneity is None and scores_disparity is None:
                continue
            # end if
            if eval_disparity is True and eval_disparity_if_homogeneity_is_zero is True:
                if not scores_homogeneity or (scores_homogeneity and scores_homogeneity[2] > 0):
                    eval_disparity = False
                    model_scores[key_d] = None
                # end if
            # end if
            # Compute the scores
            for index, score in enumerate([scores_homogeneity, scores_disparity]):
                # scores_homogeneity, scores_disparity, memoization
                if score is not None:
                    key = key_h
                    if index == 1:
                        key = key_d
                    # end if
                    if model_scores[key] is not None:
                        if score[2] > 0:
                            model_scores[key][1].append([cluster])
                        for idx, value in enumerate(score):
                            model_scores[key][0][idx] += value
                        # end for
                    # end if
                # end if
            # end for
        # end for model
        if size1_clusters == model_size:
            warnings.warn("All the clusters in the model have a size of 1.")
        # end if
        for _, v in model_scores.items():
            if v is None:
                continue
            for idx in range(len(v[0])):
                v[0][idx] /= model_size
            # end for
        # end for

        return model_scores, key_h, key_d, memoization
    # end evaluate_model

    @staticmethod
    def evaluate_model_using_weak_disparity(model: list, memoization: dict = None) -> tuple:
        if isinstance(model, list) is False:
            raise TypeError("model should be of type list.")
        # end if
        # Consider Order of Sequence (COS), Immediate Occurrence (CIO), Duplicate Values (CDV)
        cos, cio, cdv = True, True, False
        immediate_occurrence_max = 2

        def create_pattern(from_sequence: list) -> list:
            if not from_sequence or isinstance(from_sequence, list) is False:
                raise TypeError("from_sequence should be a non-empty list.")
            patterns = list()
            sequence_copy = from_sequence.copy()
            if cos is False:
                sequence_copy = sorted(from_sequence)
            # Go through the content of the from_sequence
            for fs_item in sequence_copy:
                if cio is False:
                    # Back to back values are not considered, therefore
                    # move on if the current value is the same as the last one.
                    if patterns and fs_item == patterns[-1]:
                        continue
                # end if
                if cdv is False and fs_item in patterns:
                    if cio is True:
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
            # end for from_sequence
            return patterns
        # end create_pattern

        # Rebuild the model with the disparity setting
        new_model = list()
        for cluster in model:
            if isinstance(cluster, list) is False:
                raise TypeError("The items in the model should be of type list.")
            # end if
            if not cluster:
                raise Exception("The items in the model should not be empty.")
            # end if
            new_cluster = list()
            for sequence in cluster:
                new_cluster.append(create_pattern(sequence))
            # end for sequence in cluster
            new_model.append(new_cluster)
        # end for cluster in model
        # Evaluate the model
        eval_result = SequencesClustersEvaluation.evaluate_model(
            model=new_model, eval_homogeneity=True, eval_disparity=True,
            eval_disparity_if_homogeneity_is_zero=False, memoization=memoization)
        return eval_result
    # end evaluate_model_using_weak_disparity

    @staticmethod
    def example_sequences() -> list:
        sequence1 = [['unlock', 0], ['scan', 0], ['scan', 0], ['scan', 0],
                     ['scan', 0], ['scan', 0], ['scan', 0], ['scan', 0],
                     ['scan', 0], ['scan', -2], ['scan', 0], ['scan', 0],
                     ['scan', 0], ['scan', 0], ['transmit', 0], ['abandon', 0],
                     ['openSession', 0], ['add', 0], ['closeSession', 0], ['pay', 5]]
        sequences = [
            sequence1, sequence1[::-1],
            [['unlock', 0], ['scan', 0], ['scan', 0], ['scan', 0], ['scan', 0],
             ['scan', 0], ['scan', 0], ['scan', 0], ['scan', 0], ['scan', -2],
             ['scan', 0], ['scan', 0], ['scan', 0], ['scan', 0],
             ['transmit', 0], ['abandon', 0], ['openSession', 0], ['add', 0],
             ['closeSession', 0], ['payer', 5]],
            [['unlock', 0], ['scan', 0], ['scan', 0], ['scan', 0], ['scan', 0],
             ['scan', -2], ['scan', 0], ['scan', 0], ['scan', 0], ['scan', 0],
             ['scan', 0], ['scan', 0], ['scan', 0], ['scan', 0], ['transmit', 0],
             ['abandon', 0], ['openSession', 0], ['add', 0],
             ['closeSession', 0], ['pay', 5]],
            [['unlock', 0], ['scan', 0], ['scan', 0], ['scan', 0], ['scan', 0],
             ['scan', 0], ['scan', 0], ['scan', 0], ['scan', 0], ['scan', -2],
             ['scan', 0], ['scan', 0], ['scan', 0], ['scan', 0], ['transmit', 0],
             ['abandon', 0], ['openSession', 0], ['add', 0],
             ['closeSession', 0], ['pay', 5]],
            [['unlock', 0], ['scan', 0], ['scan', 0], ['scan', 0], ['scan', 0],
             ['scan', 0], ['scan', 0], ['scan', 0], ['scan', 0], ['scan', -2],
             ['scan', 0], ['scan', 0], ['transmit', 0], ['scan', 0], ['scan', 0],
             ['abandon', 0], ['openSession', 0], ['add', 0],
             ['closeSession', 0], ['pay', 5]],
            [['unlock', 0], ['scan', 0], ['scan', 0], ['scan', 0], ['scan', 0],
             ['scan', 0], ['scan', 0], ['scan', 0], ['scan', 0], ['scan', -2],
             ['scan', 0], ['scan', 0], ['abandon', 0], ['openSession', 0],
             ['scan', 0], ['scan', 0], ['transmit', 0], ['abandon', 0],
             ['openSession', 0], ['add', 0], ['closeSession', 0], ['pay', 5]],
            [['unlock', 0], ['scan', 0], ['scan', 0], ['scan', 0], ['scan', 0],
             ['scan', 0], ['scan', 0], ['scan', 0], ['scan', 0], ['scan', -2],
             ['scan', 0], ['scan', 0], ['scan', 0], ['scan', 0], ['transmit', 0],
             ['abandon', 0], ['openSession', 0], ['add', 0],
             ['closeSession', 0], ['pay', 5]]
        ]
        return sequences
    # end example_sequences

    @staticmethod
    def example_condition1_evaluation():
        sequence1 = [['unlock', 0], ['scan', 0], ['scan', 0], ['scan', 0],
                     ['scan', 0], ['scan', 0], ['scan', 0], ['scan', 0],
                     ['scan', 0], ['scan', -2], ['scan', 0], ['scan', 0],
                     ['scan', 0], ['scan', 0], ['transmit', 0],
                     ['abandon', 0], ['openSession', 0], ['add', 0],
                     ['closeSession', 0], ['pay', 5]]
        sequence2 = sequence1[::-1]
        result1 = SequencesClustersEvaluation.homogeneity_evaluation(sequence1, sequence2)
        assert result1[0] == 0, "Result did not match assert value of 0."

        sequence7 = [['unlock', 0], ['scan', 0], ['scan', 0], ['scan', 0],
                     ['scan', 0], ['scan', 0], ['scan', 0], ['scan', 0],
                     ['scan', 0], ['scan', -2], ['scan', 0], ['scan', 0],
                     ['abandon', 0], ['openSession', 0], ['scan', 0],
                     ['scan', 0], ['transmit', 0], ['abandon', 0],
                     ['openSession', 0], ['add', 0], ['closeSession', 0],
                     ['pay', 5]]

        sequence8 = [['unlock', 0], ['scan', 0], ['scan', 0], ['scan', 0],
                     ['scan', 0], ['scan', 0], ['scan', 0], ['scan', 0],
                     ['scan', 0], ['scan', -2], ['scan', 0], ['scan', 0],
                     ['scan', 0], ['scan', 0], ['transmit', 0],
                     ['abandon', 0], ['openSession', 0], ['add', 0],
                     ['closeSession', 0], ['pay', 5]]
        result4 = SequencesClustersEvaluation.homogeneity_evaluation(sequence7, sequence8)
        assert result4[0] == 0, "Result did not match assert value of 0."
    # end example_condition1_evaluation

    @staticmethod
    def example_disparity_evaluation():
        sequence1 = [['unlock', 0], ['scan', 0], ['scan', 0], ['scan', 0],
                     ['scan', 0], ['scan', 0], ['scan', 0], ['scan', 0],
                     ['scan', 0], ['scan', -2], ['scan', 0], ['scan', 0],
                     ['scan', 0], ['scan', 0], ['transmit', 0],
                     ['abandon', 0], ['openSession', 0], ['add', 0],
                     ['closeSession', 0], ['pay', 5]]
        sequence2 = sequence1[::-1]
        result1 = SequencesClustersEvaluation.disparity_evaluation(sequence1, sequence2)
        assert result1[0] == 9, "Result did not match assert value of 9."

        sequence3 = [['unlock', 0], ['scan', 0], ['scan', 0], ['scan', 0],
                     ['scan', 0], ['scan', 0], ['scan', 0], ['scan', 0],
                     ['scan', 0], ['scan', -2], ['scan', 0], ['scan', 0],
                     ['scan', 0], ['scan', 0], ['transmit', 0], ['abandon', 0],
                     ['openSession', 0], ['add', 0], ['closeSession', 0],
                     ['payer', 5]]
        sequence4 = [['unlock', 0], ['scan', 0], ['scan', 0], ['scan', 0],
                     ['scan', 0], ['scan', -2], ['scan', 0], ['scan', 0],
                     ['scan', 0], ['scan', 0], ['scan', 0], ['scan', 0],
                     ['scan', 0], ['scan', 0], ['transmit', 0],
                     ['abandon', 0], ['openSession', 0], ['add', 0],
                     ['closeSession', 0], ['pay', 5]]
        result2 = SequencesClustersEvaluation.disparity_evaluation(sequence3, sequence4)
        assert result2[0] == 4, "The expected result is 4"

        sequence5 = [['unlock', 0], ['scan', 0], ['scan', 0], ['scan', 0],
                     ['scan', 0], ['scan', 0], ['scan', 0], ['scan', 0],
                     ['scan', 0], ['scan', -2], ['scan', 0], ['scan', 0],
                     ['scan', 0], ['scan', 0], ['transmit', 0],
                     ['abandon', 0], ['openSession', 0], ['add', 0],
                     ['closeSession', 0], ['pay', 5]]

        sequence6 = [['unlock', 0], ['scan', 0], ['scan', 0], ['scan', 0],
                     ['scan', 0], ['scan', 0], ['scan', 0], ['scan', 0],
                     ['scan', 0], ['scan', -2], ['scan', 0], ['scan', 0],
                     ['transmit', 0], ['scan', 0], ['scan', 0], ['abandon', 0],
                     ['openSession', 0], ['add', 0], ['closeSession', 0], ['pay', 5]]
        result3 = SequencesClustersEvaluation.disparity_evaluation(sequence5, sequence6)
        assert result3[0] == 1, "The expected result is 1 for ['transmit', 0]"

        sequence7 = [['unlock', 0], ['scan', 0], ['scan', 0], ['scan', 0],
                     ['scan', 0], ['scan', 0], ['scan', 0], ['scan', 0],
                     ['scan', 0], ['scan', -2], ['scan', 0], ['scan', 0],
                     ['abandon', 0], ['openSession', 0], ['scan', 0], ['scan', 0],
                     ['transmit', 0], ['abandon', 0], ['openSession', 0],
                     ['add', 0], ['closeSession', 0], ['pay', 5]]

        sequence8 = [['unlock', 0], ['scan', 0], ['scan', 0], ['scan', 0],
                     ['scan', 0], ['scan', 0], ['scan', 0], ['scan', 0],
                     ['scan', 0], ['scan', -2], ['scan', 0], ['scan', 0],
                     ['scan', 0], ['scan', 0], ['transmit', 0], ['abandon', 0],
                     ['openSession', 0], ['add', 0], ['closeSession', 0], ['pay', 5]]
        result4 = SequencesClustersEvaluation.disparity_evaluation(sequence7, sequence8)
        assert result4[0] == 3, "The expected result is 3 for 1 shift and 2 items ['abandon', 0], ['openSession', 0]"
        result = SequencesClustersEvaluation.disparity_evaluation(
            [["e", 0], ["r", 0]], [["e", 0], ["e", 0], ["r", 0], ["e", 0]])
    # end example_disparity_evaluation

    @staticmethod
    def example_predecessors_evaluation():
        sequence1 = [['unlock', 0], ['scan', 0], ['scan', 0], ['scan', 0],
                     ['scan', 0], ['scan', 0], ['scan', 0], ['scan', 0],
                     ['scan', 0], ['scan', -2], ['scan', 0], ['scan', 0],
                     ['scan', 0], ['scan', 0], ['transmit', 0],
                     ['abandon', 0], ['openSession', 0], ['add', 0],
                     ['closeSession', 0], ['pay', 5]]
        sequence2 = [['unlock', 0], ['scan', 0], ['scan', 0], ['scan', 0],
                     ['scan', 0], ['scan', -2], ['scan', 0], ['scan', 0],
                     ['transmit', 0], ['abandon', 0], ['openSession', 0], ['add', 0],
                     ['closeSession', 0], ['pay', 5]]
        result1 = SequencesClustersEvaluation.predecessors_evaluation(sequence1, sequence2)
        assert result1 == (0, 0), "Result did not match assert value of 0."
        sequence2 = [['unlock', 0], ['scan', 0], ['scan', 0], ['scan', 0],
                     ['scan', 0], ['scan', -2], ['scan', 0], ['scan', 0], ['add', 0],
                     ['transmit', 0], ['abandon', 0], ['openSession', 0],
                     ['closeSession', 0], ['pay', 5]]
        result1 = SequencesClustersEvaluation.predecessors_evaluation(
            sequence1, sequence2, final_states=[['scan', 0]])
    # end example_predecessors_evaluation

    @staticmethod
    def example_evaluate_cluster():
        result = SequencesClustersEvaluation.evaluate_cluster(
            SequencesClustersEvaluation.example_sequences(), False
        )
        return result
    # end example_evaluate_cluster

    @staticmethod
    def example_evaluate_model():
        model = [SequencesClustersEvaluation.example_sequences()] * 2
        result = SequencesClustersEvaluation.evaluate_model(model)
        return result
    # end example_evaluate_model

    @staticmethod
    def example_evaluate_model_using_weak_disparity():
        model = [SequencesClustersEvaluation.example_sequences()] * 2
        result = SequencesClustersEvaluation.evaluate_model_using_weak_disparity(model)
        return result
    # end example_evaluate_model_using_weak_disparity

    @staticmethod
    def example_evaluate_sequences():
        sequence = [['ACCOUNT_CREATED'], ['WISH_CREATION'],
                    ['FILE_SUBMITTED'], ['SUBMISSION_OF_APPLICATION']]
        sequences = [
            [['ACCOUNT_CREATED'], ['WISH_CREATION'], ['WISH_CREATION'],
             ['WISH_CREATION'], ['FILE_SUBMITTED'], ['FILE_SUBMITTED'],
             ['FILE_SUBMITTED'], ['SUBMISSION_OF_APPLICATION']],
            sequence,
            [['ACCOUNT_CREATED'], ['WISH_CREATION'], ['FILE_SUBMITTED'],
             ['FILE_SUBMITTED'], ['SUBMISSION_OF_APPLICATION'],
             ['IMPROPER_PROCEDURE']], sequence
        ]
        # result = SequencesClustersEvaluation.disparity_evaluation(
        #     sequence, sequences[0])
        # assert result[0] == 9, "Result did not match assert value of 9."
        result = SequencesClustersEvaluation.evaluate_sequences(
            one=sequence, to_many=sequences)
        assert result is not None
    # end example_evaluate_sequences

    @staticmethod
    def example_compute_score():
        model = [
            [[['ACCOUNT_CREATED'], ['WISH_CREATION'], ['FILE_SUBMITTED'],
              ['SUBMISSION_OF_APPLICATION'], ['APPLICATION_INCOMPLETE'],
              ['FILE_SUBMITTED'], ['FILE_SUBMITTED'], ['SUBMISSION_OF_APPLICATION'],
              ['APPLICATION_COMPLETE'], ['ADVISORY_DECISION_UNFAVORABLE'],
              ['PROPOSAL_FOR_ADMISSION'], ['ADMISSION_CONFIRMATION']],
             [['ACCOUNT_CREATED'], ['WISH_CREATION'], ['FILE_SUBMITTED'],
              ['SUBMISSION_OF_APPLICATION'], ['APPLICATION_INCOMPLETE'],
              ['FILE_SUBMITTED'], ['SUBMISSION_OF_APPLICATION'],
              ['APPLICATION_COMPLETE'], ['ADVISORY_DECISION_FAVORABLE'],
              ['PROPOSAL_FOR_ADMISSION'], ['APPLICATION_CLOSED']],
             [['ACCOUNT_CREATED'], ['WISH_CREATION'], ['WISH_CREATION'],
              ['WISH_CREATION'], ['FILE_SUBMITTED'], ['SUBMISSION_OF_APPLICATION'],
              ['APPLICATION_COMPLETE'], ['ADVISORY_DECISION_UNFAVORABLE'],
              ['PROPOSAL_FOR_ADMISSION'], ['ADMISSION_WITHDRAWAL']]],
            [[['ACCOUNT_CREATED'], ['WISH_CREATION'], ['FILE_SUBMITTED'],
              ['SUBMISSION_OF_APPLICATION']],
             [['ACCOUNT_CREATED'], ['WISH_CREATION'], ['WISH_CREATION'],
              ['APPLICATION_CLOSED']], [['ACCOUNT_CREATED']],
             [['ACCOUNT_CREATED'], ['WISH_CREATION'], ['FILE_SUBMITTED'],
              ['FILE_SUBMITTED'], ['SUBMISSION_OF_APPLICATION'],
              ['APPLICATION_COMPLETE'], ['ADVISORY_DECISION_FAVORABLE'],
              ['PROPOSAL_FOR_ADMISSION'], ['ADMISSION_WITHDRAWAL']],
             [['ACCOUNT_CREATED'], ['WISH_CREATION'], ['WISH_CREATION'],
              ['WISH_CREATION'], ['FILE_SUBMITTED'], ['FILE_SUBMITTED'],
              ['FILE_SUBMITTED'], ['SUBMISSION_OF_APPLICATION']],
             [['ACCOUNT_CREATED'], ['WISH_CREATION']]],
            [[['ACCOUNT_CREATED'], ['WISH_CREATION'], ['FILE_SUBMITTED'],
              ['FILE_SUBMITTED'], ['SUBMISSION_OF_APPLICATION'],
              ['IMPROPER_PROCEDURE']],
             [['ACCOUNT_CREATED'], ['WISH_CREATION'], ['FILE_SUBMITTED'],
              ['FILE_SUBMITTED'], ['FILE_SUBMITTED'],
              ['SUBMISSION_OF_APPLICATION'], ['IMPROPER_PROCEDURE']],
             [['ACCOUNT_CREATED'], ['WISH_CREATION'], ['FILE_SUBMITTED'],
              ['FILE_SUBMITTED'], ['SUBMISSION_OF_APPLICATION'],
              ['IMPROPER_PROCEDURE']],
             [['ACCOUNT_CREATED'], ['WISH_CREATION'], ['FILE_SUBMITTED'],
              ['SUBMISSION_OF_APPLICATION'], ['APPLICATION_INCOMPLETE'],
              ['FILE_SUBMITTED'], ['SUBMISSION_OF_APPLICATION'],
              ['IMPROPER_PROCEDURE']]]
        ]
        SequencesClustersEvaluation.evaluate_model(model, eval_disparity_if_homogeneity_is_zero=False)
    # end example_compute_score

# end SequencesClustersEvaluation
