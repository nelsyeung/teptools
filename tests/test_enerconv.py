"""Test enerconv script.

All args arrays have extra default values in it to prevent custom user rc file
interfering with the tests."""
import os
import pytest
import enerconv

fixtures_dir = os.path.join('tests', 'fixtures')


@pytest.fixture
def chdir_fixtures(request):
    """Change the directory to the fixtures dir and back to the root directory
    after finished."""
    cwd = os.getcwd()
    os.chdir(fixtures_dir)
    open('not_finished.out', 'a').close()

    def fin():
        os.remove('not_finished.out')
        os.chdir(cwd)

    request.addfinalizer(fin)


def test_main(capsys, chdir_fixtures):
    """Test main function."""
    enerconv.main(['one.out', 'two.in', 'not_finished.out'], 'emptyrc')
    out, err = capsys.readouterr()

    assert out == ('fixtures -14338.56459039093170\n'
                   'fixtures -14348.98291773412348\n'
                   'not_finished.out <-- not finished\n')
