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


def files2zip(files, _extra=".jpg", dst_zip_size=30):
    """
    :param files: 文件夹信息
    :param _extra: 后缀
    :param dst_zip_size:  目标文件大小，实际转换时会 * 0.8 防止大小溢出
    :return:
    """
    init_folder_num = 0
    folder_size = len(files)
    avg_file_size = sum([os.path.getsize(i) / float(1024 * 1024) for i in files]) / folder_size  # 计算转换后文件平均大小
    _split_num = int(dst_zip_size * 0.8 // avg_file_size)  # 计算切割的文件个数， 因为是平均值，* 0.8 防止溢出

    # 创建文件夹
    for i in range(folder_size // _split_num + 1):
        os.makedirs(f"Dst/part{i}", int("755", 8))  # 十进制转变为八进制

    # 移动文件
    for i in range(folder_size):
        if (folder_size - i) % _split_num:
            # shutil.move(JPG[i], f"Dst/part{init_folder_num}")
            shutil.copy(files[i], f"Dst/part{init_folder_num}")
            continue
        init_folder_num += 1
        # shutil.move(JPG[i], f"Dst/part{init_folder_num}")
        shutil.copy(files[i], f"Dst/part{init_folder_num}")

    # zip 打包
    for i in range(folder_size // _split_num + 1):
        folder_name = f"Dst/part{i}"
        z = zipfile.ZipFile(f"{folder_name}.zip", 'w')
        files = glob.glob(os.path.join(f"{folder_name}", f"*{_extra}"))
        for _file in files:
            z.write(_file)


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