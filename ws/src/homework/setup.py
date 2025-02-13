from setuptools import find_packages, setup

package_name = 'homework'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sunwolee',
    maintainer_email='128200788+malenwater@users.noreply.github.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'move_array = homework.homework1.move:main',
            'gear = homework.homework2.gear:main',
            'genga_stand = homework.homework3.genga_stand:main',
            'cup_stand3 = homework.homework4.cup_stand:main',
            'cup_stand11 = homework.homework5_final.cup_stand_11:main',
        ],
    },
)
