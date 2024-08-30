import click
import tifffile
from PIL import Image
import numpy as np
'''
执行环境 source /BI2/scenv/js.tang/miniconda3/bin/activate myenv_10x
执行命令 python convert_image.py --input_file Visium_HD_Human_Colon_Cancer_tissue_image.btf --output_file output.png --scale_factor 0.01
'''
def read_image(input_file):
    if input_file.lower().endswith(('.btf', '.tiff', '.tif')):
        with tifffile.TiffFile(input_file) as tif:
            img = tif.asarray()

    else:
        img = np.array(Image.open(input_file))

    # 打印原始图像的形状和数据类型
    img = img.astype(np.uint8)

    # 打印转换后的图像的形状和数据类型
    print(f"Converted image shape: {img.shape}, dtype: {img.dtype}")
    # 判断是否需要转置
    if img.ndim == 3 and img.shape[0] in [1, 3]:
        img = np.transpose(img, (1, 2, 0))

    return img

def save_image(img, output_file):

    # 打印图像的形状和数据类型
    print(f"Saving image with shape: {img.shape} and dtype: {img.dtype}")
    Image.fromarray(img).save(output_file)

@click.command()
@click.option('--input_file', required=True, help='输入文件路径')
@click.option('--output_file', required=True, help='输出文件路径')
@click.option('--scale_factor', default=0.1, help='压缩比例 (0-1)')
def process_image(input_file, output_file, scale_factor):
    Image.MAX_IMAGE_PIXELS = None
    # 读取图像数据
    img = read_image(input_file)

    # 选择正确的高和宽
    print(img.shape)

    new_width = max(1, int(img.shape[1] * scale_factor))
    new_height = max(1, int(img.shape[0] * scale_factor))
    print(f'new_width:{new_width},new_height:{new_height}')

    # 降低图像分辨率
    img_resized = np.array(Image.fromarray(img).resize(
        (new_width, new_height),
        Image.LANCZOS
    ))

    # 保存为指定格式的文件
    save_image(img_resized, output_file)

    print(f"Preview image saved as {output_file}")

if __name__ == '__main__':
    process_image()