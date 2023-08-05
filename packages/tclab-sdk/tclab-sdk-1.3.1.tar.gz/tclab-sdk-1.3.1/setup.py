import setuptools
with open("README.md", "r",encoding='utf-8') as fh:
    long_description = fh.read()
setuptools.setup(
    name="tclab-sdk",  # 模块名称
    version="1.3.1",  # 当前版本
    author="Haotian Yang",  # 作者
    author_email="yht1592754117@126.com",  # 作者邮箱
    description="TC Laboratory Central_Management_System Client Module",  # 模块简介
    long_description=long_description,  # 模块详细介绍
    long_description_content_type="text/markdown",  # 模块详细介绍格式
    packages=setuptools.find_packages(),  # 自动找到项目中导入的模块
    # 模块相关的元数据
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 依赖模块
    install_requires=[
        'requests',
        'pycryptodome'
    ],
    python_requires='>=3',
)
