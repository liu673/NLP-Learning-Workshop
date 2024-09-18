# -*- coding: utf-8 -*-
import os
import json
import requests
import pandas as pd
from utils import MRPCSingle, _process_mrpc


def maybe_download_mrpc(save_dir="./MRPC/", proxy=None):
    train_url = 'https://mofanpy.com/static/files/MRPC/msr_paraphrase_train.txt'
    test_url = 'https://mofanpy.com/static/files/MRPC/msr_paraphrase_test.txt'
    os.makedirs(save_dir, exist_ok=True)
    proxies = {"http": proxy, "https": proxy}
    for url in [train_url, test_url]:
        raw_path = os.path.join(save_dir, url.split("/")[-1])
        if not os.path.isfile(raw_path):
            print("downloading from %s" % url)
            r = requests.get(url, proxies=proxies)
            with open(raw_path, "w", encoding="utf-8") as f:
                f.write(r.text.replace('"', "<QUOTE>"))
                print("completed")


def txt_to_csv(txt_dir="./test", save_dir="./test"):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    files = os.listdir(txt_dir)
    for file in files:
        if file.endswith('.txt'):
            txt_path = os.path.join(txt_dir, file)
            csv_path = os.path.join(save_dir, file.replace('.txt', '.csv'))

            # 检查文件是否为空
            if os.path.getsize(txt_path) == 0:
                print(f"The file {file} is empty.")
                continue

            try:
                # 尝试读取文件
                with open(txt_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                # 忽略第一行
                header = lines[0].strip()
                data = lines[1:]

                # 尝试将数据写入CSV
                print("Writing to CSV...")
                df = pd.read_csv(txt_path, sep='\t')
                print(df)
                # df = pd.DataFrame([line.strip().split('\t') for line in data])
                # df.to_csv(csv_path, index=False, header=[header], encoding='utf-8')
            except Exception as e:
                print(f"Failed to process {file}: {e}")


def load_data(file_path="./MRPC/", save_path="./processed.json"):
    dataset, v2i, i2v = _process_mrpc(file_path)
    # print(dataset)
    output_data = {
        "dataset": dataset,
        "v2i": v2i,
        "i2v": i2v
    }

    # 将字典数据保存为JSON文件
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    # maybe_download_mrpc()
    # load_data()
    dataset = MRPCSingle()
    print(dataset.num_word)

