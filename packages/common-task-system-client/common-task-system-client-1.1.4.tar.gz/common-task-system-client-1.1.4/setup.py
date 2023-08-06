from setuptools import setup, find_packages

setup(
    name='common-task-system-client',
    packages=find_packages(),
    version='1.1.4',
    install_requires=[
        "py-cone>=1.0.2",
    ],
    # extras_require={
    # },
    author='cone387',
    maintainer_email='1183008540@qq.com',
    license='MIT',
    url='https://github.com/cone387/CommonTaskSystemClent',
    python_requires='>=3.7, <4',
    entry_points={
        'console_scripts': [
            'common-task-system-client=task_system_client.main:start_task_system',
        ],
    },
)
