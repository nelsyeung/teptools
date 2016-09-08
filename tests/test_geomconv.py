"""Test geomconv script."""
import os
import pytest
import geomconv

fixtures_dir = os.path.join('tests', 'fixtures')


@pytest.fixture
def chdir_fixtures(request):
    """Change the directory to the fixtures dir and back to the root directory
    after finished."""
    cwd = os.getcwd()
    os.chdir(fixtures_dir)

    def fin():
        os.chdir(cwd)

    request.addfinalizer(fin)


def test_main_single(capsys):
    """Supplying a single outfile should print out the correct geomconv."""
    outfile = os.path.join(fixtures_dir, 'one.out')
    expected_file = os.path.join(fixtures_dir, 'one_expected.geomconv')
    geomconv.main([outfile], 'emptyrc')
    out, err = capsys.readouterr()

    with open(expected_file, 'r') as f:
        expected = f.read()

    assert out == expected


@pytest.mark.parametrize('outfile', [
    [],
    ['*.out']
])
def test_main_globbing(outfile, capsys, chdir_fixtures):
    """Supplying a glob pattern should also get the correct file."""
    geomconv.main(outfile, 'emptyrc')
    out, err = capsys.readouterr()

    with open('one_expected.geomconv', 'r') as f:
        expected = f.read()

    assert out == expected


def test_side_view(capsys):
    """Supplying two outfile should print out the two outputs side-by-side."""
    outfiles = [os.path.join(fixtures_dir, 'one.out'),
                os.path.join(fixtures_dir, 'two.in')]
    expected_file = os.path.join(fixtures_dir, 'side_view_expected.geomconv')
    geomconv.main(outfiles)
    out, err = capsys.readouterr()

    with open(expected_file, 'r') as f:
        expected = f.read()

    assert out == expected
