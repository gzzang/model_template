# model_template(模型模板)

## 介绍

以最小二乘法为例，给出模型读入、计算、备份和输出的模板。
计算与输出分离，避免重复计算。

## 版本

- v1.0.0 完成
- v2.0.0 重构

## 说明

- data/data.json
  - 确定需要执行的example
- data/.../确定需要执行的example.json
  - is_load
    - 是否读取pickle
  - is_zip
    - 是否打包
  - result
    - 确定需要输出的result
