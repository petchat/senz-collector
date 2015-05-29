# -*- coding: utf-8 -*-

"""Align time sequences by length and time distribution"""

__author__ = 'jiaying.lu'
__all__ = ['generate_sequences_measures']

from logger import logger

TIME_SEG_NUM = 3

def _get_sequence_length(sequence):
    """Return length of sequence
    """
    return len(sequence)


def _get_time_distribution_params(sequence_list, time_seg_num=TIME_SEG_NUM):
    """Return params of sequences' time distribution

    Parameters
    ----------
    sequence_list: array_like, shape(m, n?)
      List of m time sequence,
      each time sequence may has different elems
    time_seg_num: int, default TIME_SEG_NUM
      时间分段的段数

    Returns
    -------
    time_seq_start: int, timestamp
      时间分布最宽的时间序列的开始时间戳 
    time_seg_len: int, in milliseconds
      时间分段的长度
    """
    sequences_time_wide = [] 
    for sequence in sequence_list:
        # assert not sequence
        sequences_time_wide.append(sequence[-1]-sequence[0])
    time_seg_len = max(sequences_time_wide) / time_seg_num

    max_sequence_index = sequences_time_wide.index(max(sequences_time_wide))
    time_seg_start = sequence_list[max_sequence_index][0]

    return time_seg_start, time_seg_len


def _get_time_distribution(sequence, time_seq_start,
                           time_seg_len, time_seg_num=TIME_SEG_NUM):
    """Return time distribution of sequence

    Parameters
    ----------
    sequence: array_like, shape(1, n)
      Time sequence of n timestamp
    time_seq_start: int, timestamp
      时间分布最宽的时间序列的开始时间戳 
    time_seg_len: int, in milliseconds
      时间分段的长度
    time_seg_num: int, default TIME_SEG_NUM
      时间分段的段数

    Returns
    -------
    time_dis: float
      measure of time distribution
    """
    sequence_time_slice = lambda sequence, start, end: filter(lambda e: e>=start and e<end, sequence)

    time_dis = 1  # cause time_dis = TT seg_dis(i)
    time_slice_nodes = [(time_seq_start+i*time_seg_len, time_seq_start+(i+1)*time_seg_len)
                       for i in xrange(time_seg_num)]

    for start, end in time_slice_nodes: 
        sequence_seg = sequence_time_slice(sequence, start, end)
        time_dis *= len(sequence_seg)

    return time_dis

def generate_sequences_measures(sequence_list):
    """Generate length, time distribution measures of time sequences

    Parameters
    ----------
    sequence_list: array_like, shape(m, n?)
      List of m time sequence,
      each time sequence may has different elems

    Returns
    -------
    measures: array_like, shape(m, 2)
      Measures of m time sequence,
      each time sequence has 2 measures - length, time dis
    """
