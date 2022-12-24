#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 16:43:40 2022

@author: lautisilber
"""

from multiprocessing import Pool, cpu_count
from multiprocessing.dummy import Pool as ThreadPool
from tqdm.auto import tqdm
from tqdm import tqdm as ftqdm # tqdm forced to normal terminal
from functools import partial
from typing import Union, Iterable


CPU_CORES = cpu_count()


def _map(pooltype: Union[Pool, ThreadPool], func: callable, iterable: Iterable, desc=None, leave=True, unit='it', tqdm_force_terminal=False, **kwargs):
    '''
    

    Parameters
    ----------
    pooltype : Either Pool or ThreadPool
    func : Callable
        Function to be called in the pool.
    iterable : iterable
        func will be called one time with every element in iterable.
    desc : str or None
        tqdm description
    unit : str or None
        tqdm unit
    tqdm_force_terminal : bool, optional
        Force tqdm terminal mode. The default is False
    leave : bool, optional
        If False, removes all traces of the progressbar upon termination of iteration. The default is True
    **kwargs : TYPE
        Any kwargs will be applied  to all func calls.

    Returns
    -------
    list
        A list with the function results.

    '''
    if kwargs:
        func = partial(func, **kwargs)
    _tqdm = tqdm if not tqdm_force_terminal else ftqdm
    with pooltype() as pool:
        return list(_tqdm(pool.imap(func, iterable), total=len(iterable), desc=desc, unit=unit, leave=leave))

def _map_notqdm(pootlype: Union[Pool, ThreadPool], func: callable, iterable: Iterable, **kwargs):
    if kwargs:
        func = partial(func, **kwargs)
    with pootlype() as pool:
        return pool.map(func, iterable)

def pmap(func, iterable, no_tqdm=False, desc=None, unit='it', tqdm_force_terminal=False, leave=True, **kwargs):
    '''
    

    Parameters
    ----------
    func : Callable
        Function to be called in the pool.
    iterable : iterable
        func will be called one time with every element in iterable.
    no_tqdm : bool, optional
        wether to display tqdm or not. The default is False.
    desc : str or None, optional
        tqdm description. The default is None.
    unit : str or None, optional
        tqdm unit. The default is 'it'.
    tqdm_force_terminal : bool, optional
        Force tqdm terminal mode. The default is False.
    leave : bool, optional
        If False, removes all traces of the progressbar upon termination of iteration. The default is True
    **kwargs : TYPE
        Any kwargs will be applied  to all func calls.

    Returns
    -------
    list
        A list with the function results.

    '''
    if no_tqdm:
        return _map_notqdm(Pool, func, iterable, **kwargs)
    return _map(Pool, func, iterable, desc=desc, unit=unit, tqdm_force_terminal=tqdm_force_terminal, leave=leave, **kwargs)

def tmap(func, iterable, no_tqdm=False, desc=None, unit='it', tqdm_force_terminal=False, leave=False, **kwargs):
    '''
    

    Parameters
    ----------
    func : Callable
        Function to be called in the pool.
    iterable : iterable
        func will be called one time with every element in iterable.
    no_tqdm : bool, optional
        wether to display tqdm or not. The default is False.
    desc : str or None, optional
        tqdm description. The default is None.
    unit : str or None, optional
        tqdm unit. The default is 'it'.
    tqdm_force_terminal : bool, optional
        Force tqdm terminal mode. The default is False.
    leave : bool, optional
        If False, removes all traces of the progressbar upon termination of iteration. The default is True
    **kwargs : TYPE
        Any kwargs will be applied  to all func calls.

    Returns
    -------
    list
        A list with the function results.

    '''
    if no_tqdm:
        return _map_notqdm(ThreadPool, func, iterable, **kwargs)
    return _map(ThreadPool, func, iterable, desc=desc, unit=unit, tqdm_force_terminal=tqdm_force_terminal, leave=leave, **kwargs)

def test(x, b):
    return x ** 2 + b

if __name__ == '__main__':
    res = pmap(test, [1, 2, 3], tqdm_force_terminal=True, b=-1)
    print(res)







