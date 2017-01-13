"""Test helpers module."""
import os
import glob
import pytest
import helpers


fixtures_dir = os.path.join('tests', 'fixtures')


@pytest.fixture
def remove_output(request):
    """Remove files created."""
    def fin():
        for output in glob.glob('*.summary'):
            os.remove(output)

    request.addfinalizer(fin)


@pytest.mark.parametrize('section, default, expected', [
    ('summarise', {
        'options': [],
        'outfile_ext': 'out'
    }, {
        'options': ['--vimdiff', '-wo'],
        'outfile_ext': 'ext'
    }),
    ('geomconv', {
        'outfile_ext': 'out'
    }, {
        'outfile_ext': 'ext'
    }),
    ('emptysection', {
        'empty_setting': ''
    }, {
        'empty_setting': 'empty'
    }),
    ('create', {
        'templates': [],
        'potdir': ''
    }, {
        'templates': ['create.dat'],
        'potdir': 'pot'
    })
])
def test_parse_rcfile(section, default, expected):
    """Test parse_rcfile function."""
    rcfile = os.path.join(fixtures_dir, 'teptoolsrc')
    config = helpers.parse_rcfile(rcfile, section, default)

    assert config == expected


def test_parse_inpfile():
    """Test parse_rcfile function."""
    inpfile = os.path.join(fixtures_dir, 'check.dat')
    config = helpers.parse_inpfile(inpfile)
    expected = {
        'keywords': {
            'task': 'geometryoptimization',
            'do_properties': 't',
            'geom_continuation': 't'
        },
        'blocks': {
            'lattice_cart': [
                'ang',
                '87.6510  0.00000  0.0000',
                '0.00000 30.23030  0.0000',
                '0.00000  0.00000 14.3240'
            ],
            'species': [
                'Mo  Mo   42 -1 13.0',
                'S   S    16 -1 13.0'
            ],
            'species_pot': [
                'Mo  Mo.PBE-paw.abinit',
                'S   S.PBE-paw.abinit',
            ],
            'positions_abs': [
                'ang',
                'S  0.000 0.000 0.000',
                'S  0.515 0.515 0.314',
                'Mo 1.340 1.340 1.340'
            ]
        }
    }

    assert config == expected


@pytest.mark.parametrize('args, expected', [
    ([fixtures_dir],
        [os.path.join(fixtures_dir, 'one.out')]),
    ([os.path.join(fixtures_dir, '*.in')],
        [os.path.join(fixtures_dir, 'two.in')]),
    ([os.path.join('tests', '*')],
        [os.path.join(fixtures_dir, 'one.out')])
])
def test_find_files(args, expected):
    assert helpers.find_files(args, 'out') == expected


def test_create_file(remove_output):
    """create_file should return the new file name and the file object.
    If a file with the same name already exists then create a new file with
    numbered suffix."""
    newfile1, file1 = helpers.create_file('one', 'summary')
    newfile2, file2 = helpers.create_file('one', 'summary')
    newfile3, file3 = helpers.create_file('one', 'summary')

    file1.close()
    file2.close()
    file3.close()

    assert (newfile1 == 'one.summary' and
            newfile2 == 'one_1.summary' and
            newfile3 == 'one_2.summary' and
            os.path.isfile('one.summary') and
            os.path.isfile('one_1.summary') and
            os.path.isfile('one_2.summary'))
