#!/bin/bash
# 执行命令 bash terminate_nfs_processes.sh ,删除当前目录的所有 nfs 文件

# 定义要查找和删除 .nfs 文件的目录
TARGET_DIR="."

# 查找占用 .nfs 文件的进程并保存到 nfs_processes.txt 文件
lsof | grep .nfs > nfs_processes.txt

# 读取 nfs_processes.txt 文件并终止所有相关进程
while read -r line; do
    # 提取进程ID (PID)
    pid=$(echo $line | awk '{print $2}')
    echo "Terminating process $pid"
    # 终止进程
    kill -9 $pid
done < nfs_processes.txt

# 删除 .nfs 文件
find "$TARGET_DIR" -name ".nfs*" -exec rm -f {} \;

# 清理临时文件
rm nfs_processes.txt

echo "All .nfs files have been deleted."