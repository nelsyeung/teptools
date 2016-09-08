"""Test create script."""
import os
import shutil
import pytest
import create

input_num = 0
fixtures_dir = os.path.join('tests', 'fixtures')


@pytest.fixture
def setup(request):
    cwd = os.getcwd()
    potdir = 'pot'
    w1 = os.path.join(potdir, 'w1.pot')
    s2 = os.path.join(potdir, 'S2.pot')

    os.chdir(fixtures_dir)
    os.mkdir('pot')
    open(w1, 'a').close()
    open(s2, 'a').close()

    def fin():
        shutil.rmtree('pot')
        shutil.rmtree('cutoff')
        shutil.rmtree('radius')
        os.chdir(cwd)

    request.addfinalizer(fin)


@pytest.fixture
def create_potfiles(request):
    potdir = 'pot'
    w1 = os.path.join(potdir, 'w1.pot')
    w2 = os.path.join(potdir, 'W2.pot')
    s1 = os.path.join(potdir, 's1.pot')
    s2 = os.path.join(potdir, 'S2.pot')
    os.mkdir('pot')
    open(w1, 'a').close()
    open(w2, 'a').close()
    open(s1, 'a').close()
    open(s2, 'a').close()

    def fin():
        shutil.rmtree('pot')
        os.remove('create_inpfile.dat')

    request.addfinalizer(fin)


def test_get_cell_blocks():
    """Test get_cell_blocks function."""
    cellfile = os.path.join(fixtures_dir, 'create.cell')
    expected = {
        'lattice_cart': [
            'ang    # angstrom units\n',
            '  91.119728884583495   0.000000000000023   0.000000000000000\n',
            '   0.000000000000000  16.439999999999998   0.000000000000000\n',
            '   0.000000000000000   0.000000000000000  12.900000000000000\n'
        ],
        'positions_abs': [
            'ang    # angstrom units\n',
            'Mo   0.949163842547745   1.644000000000001   3.225000000000000\n',
            'S    1.898327685095489   0.000000000000000   1.586700000000000\n',
            'Se  64.543141293246649   6.576000000000014   1.612500000000000\n'
        ]
    }
    blocks = create.get_cell_blocks(cellfile)

    assert blocks == expected


def test_get_atomic_number():
    """Test get_atomic_number function."""
    assert create.get_atomic_number('Mo') == 42


def test_create_inpfile(monkeypatch, create_potfiles):
    """Test create_inpfile function."""
    global input_num
    input_num = 0

    def mock_input(_):
        global input_num
        input_num += 1

        if input_num == 1:
            return ''
        elif input_num == 2:
            return '2'

    monkeypatch.setitem(__builtins__, 'input', mock_input)
    inpfile = 'create_inpfile.dat'
    template = os.path.join(fixtures_dir, 'create.dat')
    cell_blocks = {
        'lattice_cart': [
            'ang    # angstrom units\n',
            '  91.119728884583495   0.000000000000023   0.000000000000000\n',
            '   0.000000000000000  16.439999999999998   0.000000000000000\n',
            '   0.000000000000000   0.000000000000000  12.900000000000000\n'
        ],
        'positions_abs': [
            'ang    # angstrom units\n',
            'Mo   0.949163842547745   1.644000000000001   3.225000000000000\n',
            'S    1.898327685095489   0.000000000000000   1.586700000000000\n',
            'Se  64.543141293246649   6.576000000000014   1.612500000000000\n'
        ]
    }
    expected_file = os.path.join(fixtures_dir, 'create_expected.dat')
    create.create_inpfile(template, inpfile, ['W', 'S'], 10, 'pot',
                          cell_blocks, '')

    with open(inpfile, 'r') as f:
        out = f.readlines()

    with open(expected_file, 'r') as f:
        expected = f.readlines()

    assert out == expected


def test_create(monkeypatch, setup):
    """Test main function."""
    global input_num
    input_num = 0

    def mock_input(_):
        global input_num
        input_num += 1

        if input_num == 1:
            return '1000'

        if input_num == 2:
            return '1200'

        if input_num == 3:
            return '100'

        if input_num == 4:
            return '10'

        if input_num == 5:
            return '12'

        if input_num == 6:
            return '0.5'

    def get_all_out(test_dir, inpfile):
        res = []

        for d in os.listdir(test_dir):
            dir = os.path.join(test_dir, d)

            if not os.path.isdir(dir):
                continue

            with open(os.path.join(dir, inpfile), 'r') as f:
                res.extend(f.readlines())

        return res

    name = 'WS'
    inpfile = name + '.dat'
    monkeypatch.setitem(__builtins__, 'input', mock_input)
    args = name + ' -e W S --cell create.cell --conv-test cutoff radius'
    create.main(args.split(), 'teptoolsrc')

    # Cutoff
    with open(os.path.join('cutoff', inpfile), 'r') as f:
        cutoff_out = f.readlines()

    with open('cutoff_expected.dat', 'r') as f:
        cutoff_expected = f.readlines()

    cutoff_all_out = get_all_out('cutoff', inpfile)

    cutoff_all_expected = [
        'includefile: ../WS.dat\n',
        '\n',
        'cutoff_energy: 1000 eV',
        'includefile: ../WS.dat\n',
        '\n',
        'cutoff_energy: 1100 eV',
        'includefile: ../WS.dat\n',
        '\n',
        'cutoff_energy: 1200 eV'
    ]

    # Radius
    with open(os.path.join('radius', inpfile), 'r') as f:
        radius_out = f.readlines()

    with open('radius_expected.dat', 'r') as f:
        radius_expected = f.readlines()

    radius_all_out = get_all_out('radius', inpfile)

    radius_all_expected = [
        'includefile: ../WS.dat\n',
        '\n',
        '%block species\n',
        'W   W    74 -1 10.0\n',
        'S   S    16 -1 10.0\n',
        '%endblock species',
        'includefile: ../WS.dat\n',
        '\n',
        '%block species\n',
        'W   W    74 -1 10.5\n',
        'S   S    16 -1 10.5\n',
        '%endblock species',
        'includefile: ../WS.dat\n',
        '\n',
        '%block species\n',
        'W   W    74 -1 11.0\n',
        'S   S    16 -1 11.0\n',
        '%endblock species',
        'includefile: ../WS.dat\n',
        '\n',
        '%block species\n',
        'W   W    74 -1 11.5\n',
        'S   S    16 -1 11.5\n',
        '%endblock species',
        'includefile: ../WS.dat\n',
        '\n',
        '%block species\n',
        'W   W    74 -1 12.0\n',
        'S   S    16 -1 12.0\n',
        '%endblock species'
    ]

    assert cutoff_out == cutoff_expected
    assert cutoff_all_out == cutoff_all_expected
    assert radius_out == radius_expected
    assert radius_all_out == radius_all_expected
