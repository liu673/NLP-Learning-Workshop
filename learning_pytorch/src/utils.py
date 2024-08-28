# -*- coding: utf-8 -*-
import requests
from pathlib import Path
from tqdm.auto import tqdm
import torch
import os


print(os.cpu_count())
# print(torch.__version__)

help_function_file = "https://raw.githubusercontent.com/mrdbourke/pytorch-deep-learning/main/helper_functions.py"
help_function_name = "helper_functions.py"


def download_py_file():
    if Path(help_function_name).is_file():
        print(f"{help_function_name} already exists")
    else:
        print(f"Downloading {help_function_name}")
        try:
            request = requests.get(help_function_file)
            request.raise_for_status()  # 这会引发 HTTP 错误（如 404）
            with open(help_function_name, "wb") as f:
                f.write(request.content)
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {help_function_name}: {e}")


def download_zip_file():
    import zipfile

    data_path = Path("data/")
    image_path = data_path / "pizza_steak_sushi"
    zip_file_path = data_path / "pizza_steak_sushi.zip"
    zip_file_url = "https://github.com/mrdbourke/pytorch-deep-learning/raw/main/data/pizza_steak_sushi.zip"

    if image_path.is_dir():
        print(f"{image_path} directory exists.")
    else:
        print(f"Did not find {image_path}, creating one...")
        image_path.mkdir(parents=True, exist_ok=True)

    if zip_file_path.is_file():
        print(f"{zip_file_path} already exists.")
    else:
        print(f"Downloading {zip_file_path}...")
        try:
            with open(zip_file_path, "wb") as f:
                request = requests.get(zip_file_url)
                f.write(request.content)
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {zip_file_path}: {e}")

    if zip_file_path.is_file():
        print(f"Extracting {zip_file_path}...")
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall(image_path)
        print(f"{zip_file_path} extracted to {image_path}")
    else:
        print(f"{zip_file_path} not found.")
    return image_path



def function_calc_time():
    from timeit import default_timer as timer

    def print_train_time(start, end, device=None):
        total_time = end - start
        print(f"Train time on {device}: {total_time:.3f} seconds")
        return total_time

    """
    example:
        function_start = timer()
        # function code...
        function_end = timer()
        print_train_time(function_start, function_end)
    """

    return print_train_time


def load_import_question():
    try:
        import torchmetrics, mlxtend
        print(f"mlxtend version: {mlxtend.__version__}")

        # 检查 torchmetrics 版本
        if torchmetrics.__version__ < "0.7.0":
            raise ImportError("Please upgrade torchmetrics to version >= 0.7.0")

    except ImportError:
        # 如果 torchmetrics 或 mlxtend 未安装或版本不符合要求，先卸载再安装
        import subprocess
        import sys

        # 卸载旧版本
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", "torchmetrics", "mlxtend"])

        # 安装或升级到指定版本
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "torchmetrics>=0.7.0", "mlxtend"])

        # 重新导入库
        import torchmetrics, mlxtend
        print(f"mlxtend version: {mlxtend.__version__}")


# load_import_question()
