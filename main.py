# main.py
import argparse
import glob
import os
import sys
import time
import numpy as np
from preprocess import preprocess_gpx
from model import build_model, train_model, generate_gpx

try:
    import select
except ImportError:
    select = None

try:
    import msvcrt
except ImportError:
    msvcrt = None

# 反标准化函数，将数据恢复到原始的经纬度范围
def denormalize(lat, lon, mean_coords, std_coords):
    denorm_lat = (lat * std_coords[0]) + mean_coords[0]
    denorm_lon = (lon * std_coords[1]) + mean_coords[1]
    return denorm_lat, denorm_lon

# 保存为 GPX 路线格式的函数
def save_to_gpx_route(filename, data, mean_coords, std_coords):
    with open(filename, 'w') as file:
        # 写入 GPX 文件头
        file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        file.write('<gpx version="1.1" creator="StackAll">\n')
        file.write(' <rte>\n')
        file.write('  <name>Generated Route</name>\n')
        file.write('  <number>1</number>\n')
        
        # 写入路线点
        for point in data:
            lat, lon = denormalize(point[0], point[1], mean_coords, std_coords)
            file.write(f'   <rtept lat="{lat}" lon="{lon}"></rtept>\n')
        
        # 写入 GPX 文件尾
        file.write(' </rte>\n')
        file.write('</gpx>\n')

# 增加了命令行参数解析
def parse_args():
    parser = argparse.ArgumentParser(description='GPX Route Generation')
    parser.add_argument('-ni', '--no-interaction', action='store_true',
        help='Run without interactive input, using default values')
    parser.add_argument('-e', '--epochs', type=int, default=100,
        help='Number of epochs to train the model')
    parser.add_argument('-p', '--num-points', type=int, default=100,
        help='Number of points to generate in each GPX route')
    parser.add_argument('-n', '--num-files', type=int, default=10,
        help='Number of GPX files to generate')
    return parser.parse_args()

def cross_platform_input_with_timeout(prompt, timeout, default):
    print(prompt, end='', flush=True)
    input_str = ''
    start_time = time.time()

    while True:
        if msvcrt:
            while (time.time() - start_time) < timeout:
                if msvcrt.kbhit():
                    char = msvcrt.getche()
                    if ord(char) == 13:
                        return input_str or default
                    if char.decode().isdigit():
                        input_str += char.decode()
                    else:
                        print("\n请输入数字。")
                        return cross_platform_input_with_timeout(prompt, timeout, default)
                time.sleep(0.05)
        else:
            if (time.time() - start_time) < timeout:
                rlist, _, _ = select.select([sys.stdin], [], [], timeout)
                if rlist:
                    input_str = sys.stdin.readline().rstrip('\n')
                    if input_str.isdigit() or input_str == '':
                        return input_str or default
                    else:
                        print("请输入数字。")
                        return cross_platform_input_with_timeout(prompt, timeout, default)
                timeout -= (time.time() - start_time)
            else:
                print()
                return default

def ensure_directories():
    if not os.path.exists('./input'):
        os.makedirs('./input')
        print("创建了 './input' 文件夹。请将您的 GPX 文件导入到这个文件夹。")
    if not os.path.exists('./output'):
        os.makedirs('./output')
        print("创建了 './output' 文件夹。")

def ensure_numeric_args(args):
    if not str(args.epochs).isdigit() or not str(args.num_points).isdigit() or not str(args.num_files).isdigit():
        print("参数必须为数字。现在进入交互式。")
        return False
    return True

def main():
    ensure_directories()
    args = parse_args()

    if not ensure_numeric_args(args):
        args.no_interaction = False

    # 默认使用命令行参数设置变量
    epochs = args.epochs
    num_points = args.num_points
    num_files = args.num_files

    # 如果启用了交互模式，则使用用户输入覆盖
    if not args.no_interaction:
        epochs_str = cross_platform_input_with_timeout(
            "请输入训练模型的迭代次数（默认为 100，10s 后采用默认值）：",
            10,
            str(args.epochs)
        )
        epochs = int(epochs_str) if epochs_str.isdigit() else args.epochs
        
        num_points_str = cross_platform_input_with_timeout(
            "请输入每个 GPX 路线要生成的点数（默认为 100，10s 后采用默认值）：",
            10,
            str(args.num_points)
        )
        num_points = int(num_points_str) if num_points_str.isdigit() else args.num_points

    if not args.no_interaction:
        num_files_str = cross_platform_input_with_timeout(
            "请输入要生成的 GPX 数量（默认为 10，10s 后采用默认值）：",
            10,
            str(args.num_files)
        )
        num_files = int(num_files_str) if num_files_str.isdigit() else args.num_files

    # 在input文件夹中查找所有.gpx文件
    gpx_files = glob.glob('./input/*.gpx')

    # 数据预处理
    sequences, next_points, mean_coords, std_coords = preprocess_gpx(gpx_files)

    if sequences is not None:
        # 构建模型
        input_shape = (sequences.shape[1], sequences.shape[2])  # 序列长度和特征数
        model = build_model(input_shape)

        # 训练模型
        train_model(model, sequences, next_points, epochs=epochs)

        # 生成并保存新的GPX路线
        seed = sequences[:1]  # 使用现有序列作为种子
        for i in range(num_files):  # 使用 num_files 控制生成的 GPX 文件数量
            generated_route = generate_gpx(model, seed, num_points=num_points)
            # 反标准化并将生成的路径保存到 GPX 文件
            filename = f'./output/generated_route_{i+1}.gpx'
            save_to_gpx_route(filename, generated_route, mean_coords, std_coords)
            print(f'生成的GPX路线已保存至 {filename}')

if __name__ == '__main__':
    main()
