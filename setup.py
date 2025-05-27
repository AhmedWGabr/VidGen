from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='vidgen',
    version='0.1.0',
    description='VidGen: Video Generator from Scene Script',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='VidGen Team',
    author_email='example@domain.com',
    url='https://github.com/AhmedWGabr/VidGen',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'gradio',
        'requests',
        'ffmpeg-python',
        'bark',
        'diffusers',
        'transformers',
        'accelerate',
        'safetensors',
        'scipy',
        'torch',
        'pydantic',
    ],
    include_package_data=True,
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'vidgen=vidgen.main:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
