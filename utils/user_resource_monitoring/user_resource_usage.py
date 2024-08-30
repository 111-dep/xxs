import click
import psutil
import time
import os
import pandas as pd  # 导入pandas库
'''
python user_resource_usage.py --user js.tang --continuous --interval 300 --output output.csv
continuous 是否持续记录
interval 监控间隔时间
output 输出文件名
'''

def get_user_processes(user):
    """根据用户名获取所有进程"""
    user_processes = []
    for proc in psutil.process_iter(['username', 'io_counters']):
        try:
            if proc.info['username'] == user and proc.status() == psutil.STATUS_RUNNING:
                user_processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return user_processes


def monitor_resources(user, continuous, interval, output):
    """监控指定用户的资源使用情况，并将结果输出到CSV文件中"""
    all_data = []  # 用于存储所有行的列表
    while True:
        start_time = time.time()
        io_read_bytes, io_write_bytes, total_mem_usage, total_cpu_percent = 0, 0, 0, 0
        active_processes_info = []  # 用于存储活跃进程的信息

        user_processes = get_user_processes(user)
        for proc in user_processes:
            try:
                io_counters = proc.io_counters()
                io_read_bytes += io_counters.read_bytes
                io_write_bytes += io_counters.write_bytes
                total_mem_usage += proc.memory_info().rss
                total_cpu_percent += proc.cpu_percent(interval=None)  # 获取即时CPU使用率
                active_processes_info.append({
                    'pid': proc.pid,
                    'name': proc.name(),
                    'cmdline': ' '.join(proc.cmdline())
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        wait_time = max(interval - (time.time() - start_time), 0)  # 确保总等待时间为指定的间隔时间
        time.sleep(wait_time)  # 等待，以使CPU百分比计算基于足够的时间间隔

        # 重新获取结束时的IO信息和CPU使用率
        end_io_read_bytes, end_io_write_bytes = 0, 0
        for proc in get_user_processes(user):
            try:
                io_counters = proc.io_counters()
                end_io_read_bytes += io_counters.read_bytes
                end_io_write_bytes += io_counters.write_bytes
                # 注意：不需要再次累加内存和CPU，因为这些在第一次遍历时已完成
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        # 计算IO增量
        io_read_bytes_increment = end_io_read_bytes - io_read_bytes
        io_write_bytes_increment = end_io_write_bytes - io_write_bytes

        all_data.append([
            user,
            round(total_mem_usage / (1024 * 1024 * 1024), 2),
            round(total_cpu_percent / psutil.cpu_count(), 2),
            round(io_read_bytes_increment / (1024 * 1024) / interval, 2),  # 使用指定的间隔时间作为计算基础
            round(io_write_bytes_increment / (1024 * 1024) / interval, 2),
            [proc_info['cmdline'] for proc_info in active_processes_info]
        ])


        if not continuous:
            break  # 如果不是连续监控，退出循环

        # 创建DataFrame
        df = pd.DataFrame(all_data, columns=['User', 'Total Memory Usage (GB)', 'Total CPU Usage (%)', 'IO Read Increment (MB/s)', 'IO Write Increment (MB/s)', 'Active Process Cmdlines'])

        # 输出DataFrame到CSV文件
        if os.path.exists(output):
            df.to_csv(output, sep="\t", index=False, header=False, mode='a')
        else:
            df.to_csv(output, sep="\t", index=False)


@click.command()
@click.option('--user', required=True, help='The username to monitor.')
@click.option('--continuous', is_flag=True, default=False, help='Whether to monitor continuously.')
@click.option('--interval', default=300, help='Interval in seconds between each record.')
@click.option('--output', required=True, help='Output file path for the CSV.')
def main(user, continuous, interval, output):
    """Monitor the resource usage of a given user."""
    monitor_resources(user, continuous, interval, output)


if __name__ == '__main__':
    main()