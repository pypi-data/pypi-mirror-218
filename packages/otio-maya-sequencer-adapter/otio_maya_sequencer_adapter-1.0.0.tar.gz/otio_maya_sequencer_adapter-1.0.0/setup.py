# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='otio-maya-sequencer-adapter',
    version='1.0.0',
    description='OpenTimelineIO Maya Sequencer Adapter',
    long_description='# OpenTimelineIO Maya Sequencer Adapter\n\nThe `maya_sequencer` adapter is part of OpenTimelineIO\'s contrib adapter plugins.\nSet the ${OTIO_MAYA_PYTHON_BIN} environment variable to point the location of `mayapy` within the maya installation.\n\n# License\n\nOpenTimelineIO and the "maya sequencer" adapter are open source software.\nPlease see the [LICENSE](LICENSE) for details.\n\nNothing in the license file or this project grants any right to use Pixar or\nany other contributor’s trade names, trademarks, service marks, or product names.\n\n## Contributions\n\nIf you want to contribute to the project,\nplease see: https://opentimelineio.readthedocs.io/en/latest/tutorials/contributing.html\n\n# Contact\n\nFor more information, please visit http://opentimeline.io/\nor https://github.com/AcademySoftwareFoundation/OpenTimelineIO\nor join our discussion forum: https://lists.aswf.io/g/otio-discussion\n',
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
            'otio_maya_sequencer_adapter = otio_maya_sequencer_adapter',
        ],
    },
    packages=[
        'otio_maya_sequencer_adapter',
    ],
    package_dir={'': 'src'},
)
