# compare_df
## 介绍
找出两个几乎DataFrame的差异

## 安装
```bash
pip install compare_df
```

## 使用
```python
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

# 检查所有列名一致的列，其余请填入different_col_names
compare(df1, df2, col_index="id", different_col_names=[("age1", "age2")], dfname_1="左表", dfname_2="右表")
```
输出：
```
左表中有，右表中没有的id：{5}
右表中有，左表中没有的id：{6}
=====================================
   name_左表 name_右表
id                
3        c       f
=====================================
    age1  age2
id            
2     20    25
=====================================
```