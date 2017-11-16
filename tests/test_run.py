"""Test run script."""
import os
import pytest
import run

fixtures_dir = os.path.join('tests', 'fixtures')


@pytest.fixture(scope='module')
def setup(request):
    inpfile = os.path.join(fixtures_dir, 'onetep.dat')
    outfile = 'onetep.out'
    onetep = os.path.join(fixtures_dir, 'onetep')

    open(inpfile, 'a').close()
    open(onetep, 'a').close()

    os.chmod(onetep, 0o744)

    def fin():
        os.remove(inpfile)
        os.remove(onetep)
        os.remove(outfile)

    request.addfinalizer(fin)


@pytest.mark.parametrize('args, rcfile, expected', [
    (None, 'not_exists', 'ONETEP path not set'),
    (None,
        os.path.join(fixtures_dir, 'teptoolsrc'),
        'tests/fixtures/not_exists does not exists'),
    (['-v', '2'],
        os.path.join(fixtures_dir, 'teptoolsrc'),
        'No ONETEP input file found or supplied')
])
def test_main_exit(args, rcfile, expected, setup):
    with pytest.raises(SystemExit) as exc:
        run.main(args, rcfile)

    out = exc.value.code

    assert out == expected


@pytest.mark.parametrize('iswrite', [
    (False),
    (True)
])
def test_main(iswrite, capsys, setup):
    args = ['-v', '2', os.path.join(fixtures_dir, 'onetep.dat')]

    if iswrite:
        args.append('--output')

    rcfile = os.path.join(fixtures_dir, 'teptoolsrc')
    run.main(args, rcfile)

    out, err = capsys.readouterr()

    if iswrite:
        assert os.path.isfile('onetep.out')

    assert not err
