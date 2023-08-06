# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='otio-svg-adapter',
    version='1.0.0',
    description='OpenTimelineIO SVG Adapter',
    long_description='# OpenTimelineIO SVG Adapter\n\nThe `svg` adapter is part of OpenTimelineIO\'s core adapter plugins.  \nIt renders a svg representation of an otio file.  \nPoints in calculations are y-up. Points in SVG are y-down.\n\n# Adapter Feature Matrix\n\nThe following features of OTIO are supported by the `svg` adapter:\n\n|Feature                  | Support |\n|-------------------------|:-------:|\n|Single Track of Clips    |    ✔    |\n|Multiple Video Tracks    |    ✔    |\n|Audio Tracks & Clips     |    ✔    |\n|Gap/Filler               |    ✔    |\n|Markers                  |    ✔    |\n|Nesting                  |    ✖    |\n|Transitions              |    ✔    |\n|Audio/Video Effects      |   N/A   |\n|Linear Speed Effects     |   N/A   |\n|Fancy Speed Effects      |   N/A   |\n|Color Decision List      |   N/A   |\n|Image Sequence Reference |    ✖    |\n\n\n# License\nOpenTimelineIO and the "svg" adapter are open source software. \nPlease see the [LICENSE](LICENSE) for details.\n\nNothing in the license file or this project grants any right to use Pixar or \nany other contributor’s trade names, trademarks, service marks, or product names.\n\n\n## Contributions\n\nIf you want to contribute to the project, \nplease see: https://opentimelineio.readthedocs.io/en/latest/tutorials/contributing.html\n\n\n# Contact\n\nFor more information, please visit http://opentimeline.io/\nor https://github.com/AcademySoftwareFoundation/OpenTimelineIO\nor join our discussion forum: https://lists.aswf.io/g/otio-discussion\n',
    author_email='Contributors to the OpenTimelineIO project <otio-discussion@lists.aswf.io>',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Multimedia :: Video',
        'Topic :: Multimedia :: Video :: Display',
        'Topic :: Multimedia :: Video :: Non-Linear Editor',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'opentimelineio>=0.15.0',
    ],
    entry_points={
        'opentimelineio.plugins': [
            'otio_svg_adapter = otio_svg_adapter',
        ],
    },
    packages=[
        'otio_svg_adapter',
    ],
    package_dir={'': 'src'},
)
