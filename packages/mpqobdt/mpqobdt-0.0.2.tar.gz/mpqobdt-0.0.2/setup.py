from setuptools import find_packages, setup
setup(
    name='mpqobdt',
    version='0.0.2',
    description='object detection for MPQ',
    author='MPQ',#作者
    author_email='miaopeiqi@163.com',
    url='https://github.com/miaopeiqi',
    #packages=find_packages(),
    packages=['mpqobdt'],  #这里是所有代码所在的文件夹名称
    package_data={
    '':['*.pyd','*.jpg','*.pt','rar'],
    },
    install_requires=['mpqlock','torch>=1.7.0','torchvision>=0.8.1','scipy>=1.4.1','Pillow>=7.1.2','PyYAML>=5.3.1','requests>=2.23.0','tqdm>=4.64.0'],
)
