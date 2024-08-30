import pandas as pd
import yaml
import os
import subprocess
import click


@click.command()
@click.argument('csv_file')
@click.argument('yaml_file')
@click.argument('command')
def process_csv(csv_file, yaml_file, command):
    # 读取CSV文件
    df = pd.read_csv(csv_file, sep='\t')

    # 读取原有的YAML文件
    with open(yaml_file, 'r') as file:
        config = yaml.safe_load(file)

    # 遍历每一行
    for index, row in df.iterrows():
        # 动态更新YAML文件中的参数
        for col in df.columns:
            if col in config:
                config[col] = row[col]

        # 创建行名的文件夹
        dir_name = row[df.columns[0]]  # 假设第一列是行名
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        # 将更新后的配置写入新的YAML文件
        with open(os.path.join(dir_name, 'config.yaml'), 'w') as file:
            yaml.dump(config, file)

        # 在行名文件夹里面执行某个命令
        full_command = f"{command} --config {os.path.join(dir_name, 'config.yaml')}"
        subprocess.run(full_command, shell=True)


if __name__ == '__main__':
    process_csv()