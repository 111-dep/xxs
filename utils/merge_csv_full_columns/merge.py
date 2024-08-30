import pandas as pd
import click

"""
python merge.py -i f1.csv -i f2.csv -i f3.csv -i f4.csv -i f5.csv -o merged_output.csv
相同列名取全集
"""
@click.command()
@click.option('--input_files', '-i', multiple=True, required=True, help='输入的CSV文件列表')
@click.option('--output_file', '-o', required=True, help='输出的合并后的CSV文件')
def merge_tables(input_files, output_file):
    # 读取所有输入文件并存储在一个列表中
    dataframes = [pd.read_csv(file,sep = '\t') for file in input_files]

    # 使用第一个表格作为基准进行合并
    merged_df = dataframes[0]

    # 依次合并剩余的表格
    for df in dataframes[1:]:
        merged_df = pd.merge(merged_df, df, on=merged_df.columns[0], how='outer', suffixes=('', '_drop'))

        # 去除重复的列
        for col in merged_df.columns:
            if '_drop' in col:
                base_col = col.replace('_drop', '')
                merged_df[base_col] = merged_df[base_col].combine_first(merged_df[col])
                merged_df.drop(columns=[col], inplace=True)

    # 保存合并后的表格到输出文件
    merged_df.to_csv(output_file, index=False)


if __name__ == '__main__':
    merge_tables()