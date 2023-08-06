import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='nonebot-plugin-nobahpicture',
    version='1.0.2',
    author='Hansa',
    author_email='hanasakayui2022@gmail.com',
    description='获取碧蓝档案涩图',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Lptr-byte/nonebot-plugin-nobahpicture',
    packages=setuptools.find_packages(),
    install_requires=['httpx==0.24.1', 'nonebot2==2.0.0', 'nonebot-adapter-onebot'],
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    )  # type: ignore
)