"""Test check script.

All args arrays have extra default values in it to prevent custom user rc file
interfering with the tests."""
import check
import os
import pytest

fixtures_dir = os.path.join('tests', 'fixtures')


@pytest.fixture
def setup_continue(request):
    """Create a continuation directory and a continuation file inside."""
    continuation_dir = os.path.join(fixtures_dir, 'continuation')
    continuation_file = os.path.join(continuation_dir, 'foo.continuation')
    os.mkdir(continuation_dir)
    open(continuation_file, 'a')

    def fin():
        os.remove(continuation_file)
        os.rmdir(continuation_dir)

    request.addfinalizer(fin)


@pytest.mark.parametrize('dirpath, config, expected', [
    (fixtures_dir, {
        'keywords': {
            'task': 'singlepoint',
            'geom_continuation': 't'
        }
    }, ''),
    (fixtures_dir, {
        'keywords': {
            'task': 'geometryoptimization',
            'geom_continuation': 't'
        }
    }, 'geom_continuation is true but continuation file not found.'),
    (os.path.join(fixtures_dir, 'continuation'), {
        'keywords': {
            'task': 'geometryoptimization',
            'geom_continuation': 'f'
        }
    }, 'geom_continuation is false but a continuation file exists.'),
    (os.path.join(fixtures_dir, 'continuation'), {
        'keywords': {
            'task': 'geometryoptimization'
        }
    }, 'geom_continuation keyword not found but a continuation file exists.')
])
def test_check_coninuation(dirpath, config, expected, capsys, setup_continue):
    """Supplying a single input file should print out the correct errors."""
    c = check.Check(dirpath, config)
    c.check_continuation()

    if not expected:
        assert c.errors == []
    else:
        assert c.errors == [expected]


def test_main(capsys):
    """Supplying a single input file should print out the correct errors."""
    args = [os.path.join(fixtures_dir, 'check.dat')]
    check.main(args, 'emptyrc')
    out, err = capsys.readouterr()

    assert out == ('geom_continuation is true but ' +
                   'continuation file not found.\n')
