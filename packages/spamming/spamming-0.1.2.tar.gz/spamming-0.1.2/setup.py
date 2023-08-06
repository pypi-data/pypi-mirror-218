from setuptools import setup


setup(
    name='spamming',
    version='0.1.2',
    license='MIT',
    description= "A spamming package",
    long_description= open("README.md").read(),
    long_description_content_type= "text/markdown",
    author="gugu256",
    author_email='gugu256@mail.com',
    keywords=["spamming", "spam", "automation", "pyautogui"],
    install_requires=[
          'pyautogui',
      ],
    classifiers= [
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]

)