#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# tr!bf tribf@tribf.com

import pandas as pd

from . import file_util

csv_args = {
    "sep": "\t",  # 使用 TAB 作为分隔符
    "na_rep": "null",  # 将nan值输出为null
    # 'lineterminator': '\r\n',  # 使用CRLF作为行终止符
    "lineterminator": "\n",  # 使用LF作为行终止符
    "index": False,  # 不记录索引序号
    "header": False,  # 不记录头
    "encoding": "utf-8",  # 使用 utf-8 编码
}

csv_dict_semi_args = {
    "sep": ";",  # 使用 分号 作为分隔符
    "na_rep": "null",  # 将nan值输出为null
    # 'lineterminator': '\r\n',  # 使用CRLF作为行终止符
    "lineterminator": "\n",  # 使用LF作为行终止符
    "index": False,  # 不记录索引序号
    "header": False,  # 不记录头
    "encoding": "utf-8",  # 使用 utf-8 编码
}

csv_args_h = {
    "sep": "\t",  # 使用 TAB 作为分隔符
    "na_rep": "null",  # 将nan值输出为null
    # 'lineterminator': '\r\n',  # 使用CRLF作为行终止符
    "lineterminator": "\n",  # 使用LF作为行终止符
    "index": False,  # 不记录索引序号
    "header": True,
    "encoding": "utf-8",  # 使用 utf-8 编码
}


def df_value_counts(df_in, col, names=None):
    cnts = df_in[col].value_counts().to_dict()
    if names is not None:
        for c in names:
            if c not in cnts:
                cnts[c] = 0

    df = pd.DataFrame.from_dict(cnts, orient="index", columns=["counts"])
    df = df.reset_index().rename(columns={"index": col})

    return df


def from_dict(d, k_name, v_name):
    df = pd.DataFrame.from_dict(d, orient="index", columns=[v_name])
    df = df.reset_index().rename(columns={"index": k_name})
    return df


def from_list_of_dict(l) -> pd.DataFrame:
    df = pd.DataFrame(l)
    return df


def to_excel(out_xlsx, df, index=False):
    out_xlsx = file_util.resolve_filepath(out_xlsx)
    file_util.ensure_dir(out_xlsx.parent)

    df.to_excel(out_xlsx, index=index, engine="openpyxl")
    print(f"dump xlsx file: {out_xlsx}")


def to_tab_csv(out_csv, df):
    out_csv = file_util.resolve_filepath(out_csv)
    file_util.ensure_dir(out_csv.parent)
    df.to_csv(out_csv, **csv_args_h)
    print(f"dump csv file: {out_csv}")


def to_tab_csv_no_header(out_csv, df):
    out_csv = file_util.resolve_filepath(out_csv)
    file_util.ensure_dir(out_csv.parent)
    df.to_csv(out_csv, **csv_args)
    print(f"dump csv file: {out_csv}")


def read_tab_csv(csv_file):
    csv_file = file_util.resolve_filepath(csv_file)
    return pd.read_csv(csv_file, sep="\t")


def read_tab_csv_no_header(csv_file, columns):
    file_util.resolve_filepath(csv_file)
    return pd.read_csv(csv_file, sep="\t", header=None, names=columns)


def load_counts(csv_file, key, value):
    df = read_tab_csv(csv_file)
    cnts = {}
    for _, r in df.iterrows():
        cnts[r[key]] = r[value]
    return cnts
