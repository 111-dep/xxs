在 depand_statics.txt 文件中，找到第7列匹配 tool_list 中模式的行，并输出这些行的第一列和第六列。你可以使用以下命令：
"""
这个命令的解释如下：
1.NR==FNR {tools[$0]; next}：读取 tool_list 文件中的每一行，并将其存储在数组 tools 中。
2. $7 in tools {print $1, $6}：对于 depand_statics.txt 文件中的每一行，如果第7列的值在 tools 数组中，则打印该行的第一列和第六列。
"""
awk -F '\t' 'NR==FNR {tools[$0]; next} $7 in tools {print $1, $6}' tool_list depand_statics.txt


"""
 rsync 命令来复制这些文件并保持目录结构
"""
rsync -av --include '*/' --include 'outs.zip' --exclude '*' /51.100/149data/sc/ /BI2/scenv/js.tang/report/work-test/contract_project/hd_visium/O-1040192/rawData