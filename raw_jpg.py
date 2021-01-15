import rawpy
import glob
import os
import imageio
import shutil
import zipfile


def raw2jpg(raw_file_name, dst="Temp_JPG", _suffix=".ARW"):
    """
    :param raw_file_name:
    :param dst: 存储目录
    :param _suffix: 文件后缀
    :return:
    """
    with rawpy.imread(raw_file_name) as raw:
        im = raw.postprocess(
            use_camera_wb=True,  # 是否使用拍摄时的白平衡值
            use_auto_wb=False,
            # half_size=True,  # 是否输出一半大小的图像，通过将每个2x2块减少到一个像素而不是进行插值来
            exp_shift=3  # 修改后光线会下降，所以需要手动提亮，线性比例的曝光偏移。可用范围从0.25（变暗2级）到8.0（变浅3级）。
        )
        imageio.imsave(dst + raw_file_name.strip(_suffix) + ".jpg", im)  # 因为glob函数返回的是一个相对路径，所以不需要使用os.path


src_suffix = ".ARW"
dst_suffix = ".jpg"
raw_files = glob.glob(f"ARW/*{src_suffix}")

print("正在转换中，请耐心等待....")
for num, raw_file in enumerate(raw_files):
    if num % 5 == 0: print(f"已转换{num}张照片...")
    raw2jpg(raw_file, _suffix=src_suffix)

print("转换完成！")
print("所有数据保留在Dst目录，请前往查看!")
print("Done!")
