import pandas as pd
from loguru import logger
from typing import Optional, List, Literal, Iterable, TypeAlias
from fire import Fire
from dataporter.utils import exec_multi_expr

FileWriteMode: TypeAlias = Literal["a", "w", "x", "at", "wt", "xt", "ab", "wb", "xb", "w+", "w+b", "a+", "a+b"]


def write_csv(
    trunk_df: Iterable[pd.DataFrame],
    csv_mode: FileWriteMode,
    pandas_exprs: List[str] | None,
    header: bool,
    debug: bool,
    names: List[str] | None,
    **pandas_kwargs,
):
    for i, df in enumerate(trunk_df):
        if names:
            df = df.rename(dict(zip(df.columns, names)), axis=1)
            if i == 0:
                logger.info(f"will rename {df.columns} to {names}")

        if pandas_exprs:
            df = exec_multi_expr(df, pandas_exprs, debug=debug)
        df: pd.DataFrame
        if csv_mode.startswith("w") and i == 0:
            df.to_csv(**pandas_kwargs, mode=csv_mode, header=header)
        else:
            df.to_csv(**pandas_kwargs, mode="a", header=False)


def csv2csv(
    read_filename: str,
    write_filename: str,
    read_names: Optional[List[str]] = None,
    read_sep: str = ",",
    read_quotechar: str = '"',
    read_escapechar: Optional[str] = None,
    read_lineterminator: Optional[str] = None,
    header: List[int] | Literal["infer"] | None = "infer",
    write_header: bool = True,
    write_names: Optional[List[str]] = None,
    write_mode: FileWriteMode = "w",
    sep: str = ",",
    index: bool = False,
    quotechar: str = '"',
    escapechar: Optional[str] = None,
    lineterminator: Optional[str] = None,
    chunk_size: Optional[int] = None,
    pandas_exprs: List[str] | None = None,
    debug: bool = False,
):
    """
    convert csv to csv file.

    :param read_filename: source csv filename.
    :param write_filename: target csv filename.
    :param read_names: source csv column names, a list e.g. `a,b,c,d`, defaults to None.
    :param read_sep: source csv sep defaults to ",".
    :param read_quotechar: source csv quotechar, defaults to '"'.
    :param read_escapechar: source csv escapechar, defaults to '"'.
    :param read_lineterminator: source csv lineterminator, defaults to '\n;
    :param header: source csv, header parameter in pandas read_csv, defaults to "infer".
    :param write_header: if write header to target csv.
    :param write_names: target csv columns, a list e.g. `a,b,c,d`, defaults to None.
    :param write_mode: how to write the csv, same as mode in open().
    :param sep: target csv sep, defaults to ",".
    :param index: should write index(linenumber) to target csv, defaults to False.
    :param quotechar: target csv quotechar, defaults to '"'.
    :param escapechar: target csv escapechar, defaults to '"'.
    :param lineterminator: target csv lineterminator, defaults to '\n'.
    :param chunk_size: read&write chunk size, use less memory, defaults to None
    :param pandas_exprs: exec multiple pandas expr in order, e.g.--pandas_exprs="['df.drop([\"xxxx\"], axis=1)','expr2 xxx']".
    :param debug: if debug mod on, will print every result after exec pandas exprs.
    """
    if chunk_size is None:
        df = pd.read_csv(
            read_filename,
            sep=read_sep,
            names=read_names,
            header=header,
            quotechar=quotechar,
            escapechar=read_escapechar,
            lineterminator=read_lineterminator,
        )

        if write_names:
            logger.info(f"will rename {df.columns} to {write_names}")
            df = df.rename(dict(zip(df.columns, write_names)), axis=1)

        if pandas_exprs:
            df = exec_multi_expr(df, pandas_exprs, debug=debug)
        df.to_csv(
            write_filename,
            index=index,
            sep=sep,
            quotechar=quotechar,
            escapechar=escapechar,
            mode=write_mode,
            header=write_header,
        )

    else:
        df = pd.read_csv(
            read_filename,
            sep=read_sep,
            chunksize=chunk_size,
            names=read_names,
            header=header,
            quotechar=read_quotechar,
            escapechar=read_escapechar,
            lineterminator=read_lineterminator,
            iterator=True,
        )
        write_csv(
            df,
            pandas_exprs=pandas_exprs,
            debug=debug,
            header=write_header,
            csv_mode=write_mode,
            path_or_buf=write_filename,
            sep=sep,
            names=write_names,
            index=index,
            chunksize=chunk_size,
            quotechar=quotechar,
            escapechar=escapechar,
            lineterminator=lineterminator,
        )


def main():
    Fire(csv2csv)


if __name__ == "__main__":
    main()
