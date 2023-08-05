import pandas as pd
from typing import List, Tuple

def _compare_cols(df, col1, col2):
    return df[df[col1] != df[col2]][[col1, col2]]

def compare(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    col_index: str,
    different_col_names: List[Tuple[str, str]] = None,
    dfname_1: str = "左表",
    dfname_2: str = "右表"
) -> List[pd.DataFrame]:
    """
    根据一列作为比较的唯一索引，比较两个DataFrame的不同
    
    Parameters
    ----------
    df1 : pd.DataFrame
        第一个DataFrame
    df2 : pd.DataFrame
        第二个DataFrame
    col_index : str
        作为比较的唯一索引的列名
    different_col_names : List[Tuple[str, str]], optional
        比较时，不同的列名，by default None
    dfname_1 : str, optional
        第一个DataFrame的名称，by default "左表"
    dfname_2 : str, optional
        第二个DataFrame的名称，by default "右表"
    
    Returns
    -------
    List[pd.DataFrame]
        返回存在差异的数据
    """
    set_index1 = set(df1[col_index])
    set_index2 = set(df2[col_index])
    
    print(f"{dfname_1}中有，{dfname_2}中没有的{col_index}：{set_index1 - set_index2}")
    print(f"{dfname_2}中有，{dfname_1}中没有的{col_index}：{set_index2 - set_index1}")
    
    merged = pd.merge(df1, df2, on=col_index, how="inner", suffixes=(f"_{dfname_1}", f"_{dfname_2}"))
    merged.set_index(col_index, inplace=True)
    
    set_cols1 = set(df1.columns) - set([col_index])
    set_cols2 = set(df2.columns) - set([col_index])
    
    cols_to_compare = [(f"{col}_{dfname_1}", f"{col}_{dfname_2}") for col in set_cols1 & set_cols2] + different_col_names
    
    result = []
    print("=====================================")
    for col1, col2 in cols_to_compare:
        diff = _compare_cols(merged, col1, col2)
        if not diff.empty:
            result.append(diff)
            print(diff)
            print("=====================================")
            
    return result

df1 = pd.DataFrame({
    "id": [1, 2, 3, 4, 5],
    "name": ["a", "b", "c", "d", "e"],
    "age1": [10, 20, 30, 40, 50],
})
                   
df2 = pd.DataFrame({
    "id": [1, 2, 3, 4, 6],
    "name": ["a", "b", "f", "d", "e"],
    "age2": [10, 25, 30, 40, 50],
})

compare(df1, df2, col_index="id", different_col_names=[("age1", "age2")], dfname_1="左表", dfname_2="右表")