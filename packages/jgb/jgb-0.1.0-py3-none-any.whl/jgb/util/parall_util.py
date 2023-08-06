#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# tr!bf tribf@tribf.com

import itertools
import math
import multiprocessing as mp
from concurrent.futures import ALL_COMPLETED, ThreadPoolExecutor, wait

import tqdm


def get_chunks(list_in, size, **kwargs):
    n = math.ceil(len(list_in) / size)

    if "min_chunk_size" in kwargs:
        n = max(n, kwargs.get("min_chunk_size"))

    chunks = [list_in[i : i + n] for i in range(0, len(list_in), n)]
    return chunks


def pmap(task_fun, tasks, **kwargs):
    parallelism = kwargs.get("parallelism", max(mp.cpu_count() - 4, 2))
    parallelism = min(parallelism, len(tasks))

    with mp.Pool(parallelism) as pool:
        result = list(tqdm.tqdm(pool.imap_unordered(task_fun, tasks), total=len(tasks)))
    return result


def tmap(task_fun, tasks, **kwargs):
    parallelism = kwargs.get("parallelism", max(mp.cpu_count() - 2, 2))
    parallelism = min(parallelism, len(tasks))
    with ThreadPoolExecutor(max_workers=parallelism) as pool:
        all_task = [pool.submit(task_fun, task) for task in tasks]
        wait(all_task, return_when=ALL_COMPLETED)
        return [r.result() for r in all_task]


def flatten(mapped_result):
    return [res for res in itertools.chain(*mapped_result)]


def main():
    print(get_chunks([1], 2))
    print(get_chunks([1, 2, 3, 4], 2))


if __name__ == "__main__":
    main()
