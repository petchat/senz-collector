# -*- coding: utf-8 -*-

"""Align time sequences by length and time distribution"""

__author__ = 'jiaying.lu'

from logger import logger

def _get_sequence_length(sequence):
    """Return length of sequence
    """
    return len(sequence)


def _get_time_distribution(sequence, time_seq_start, time_seg_len, time_seg_num=3):
    """Return time distribution of sequence

    Parameters
    ----------
    sequence: array_like, shape(1, n)
      Time sequence of n timestamp
    time_seq_start: int, timestamp
      时间分布最宽的时间序列的开始时间戳 
    time_seg_len: int, in milliseconds
      时间分段的长度
    time_seg_num: int, default 3
      时间分段的段数

    Returns
    -------
    time_dis: float
      measure of time distribution
    """
