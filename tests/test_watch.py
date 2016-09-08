"""Test helpers module."""
import os
import shutil
import multiprocessing
import time
import pytest
import watch

fixtures_dir = os.path.join('tests', 'fixtures')


@pytest.fixture
def setup(request):
    """Remove files created."""
    cwd = os.getcwd()
    os.chdir(fixtures_dir)
    os.mkdir('watch1')
    os.mkdir('watch2')

    open(os.path.join('watch1', 'onetep.dat'), 'a').close()
    open(os.path.join('watch3'), 'a').close()

    def fin():
        shutil.rmtree('watch1')
        shutil.rmtree('watch2')
        os.remove('watch3')
        os.chdir(cwd)

    request.addfinalizer(fin)


@pytest.fixture
def setup_process_dirs(request):
    """Create the necessary files for process_dirs function."""
    error_dir = os.path.join(fixtures_dir, 'watch_error')
    completed_dir = os.path.join(fixtures_dir, 'watch_completed')
    completed_dir = os.path.join(fixtures_dir, 'watch_completed')
    empty_dir = os.path.join(fixtures_dir, 'watch_empty')

    os.mkdir(error_dir)
    os.mkdir(completed_dir)
    os.mkdir(empty_dir)

    open(os.path.join(error_dir, 'f.error_message'), 'a').close()
    shutil.copy(os.path.join(fixtures_dir, 'one.out'), completed_dir)

    def fin():
        shutil.rmtree(error_dir)
        shutil.rmtree(completed_dir)
        shutil.rmtree(empty_dir)

    request.addfinalizer(fin)


@pytest.fixture
def setup_run(request):
    """Create the necessary files for run function."""
    error_dir = os.path.join(fixtures_dir, 'run_error')
    completed_dir = os.path.join(fixtures_dir, 'run_completed')
    empty_dir = os.path.join(fixtures_dir, 'run_empty')

    os.mkdir(error_dir)
    os.mkdir(completed_dir)
    os.mkdir(empty_dir)
    shutil.copy(os.path.join(fixtures_dir, 'one.out'), empty_dir)

    def create_output():
        time.sleep(0.1)
        error_file = os.path.join(error_dir, 'f.error_message')
        completed_file = os.path.join(completed_dir, 'f.out')
        open(error_file, 'a').close()

        with open(completed_file, 'w') as f:
            f.write('line1\nline2\nline3\nline4\nline5\n'
                    'Job started: foo\nJob completed: bar')

    d = multiprocessing.Process(target=create_output)
    d.daemon = True
    d.start()

    def fin():
        shutil.rmtree(error_dir)
        shutil.rmtree(completed_dir)
        shutil.rmtree(empty_dir)

    request.addfinalizer(fin)


@pytest.mark.parametrize('args', [
    [],
    ['*'],
    ['watch*'],
    ['watch1']
])
def test_watchdirs(args, setup):
    expected = ['watch1']

    if args == []:
        os.chdir('watch1')
        expected = ['./']

    out = watch.watchdirs(args, 'dat')

    if args == []:
        os.chdir('../')

    assert out == expected


def test_process_dirs(setup_process_dirs):
    """Test process_dirs function within Watch class."""
    config = {
        'outfile_ext': 'out',
        'interval': 1
    }
    watch_dirs = [
        os.path.join(fixtures_dir, 'watch_error'),
        os.path.join(fixtures_dir, 'watch_completed'),
        os.path.join(fixtures_dir, 'watch_empty')
    ]
    w = watch.Watch(watch_dirs, config)
    out = w.process_dirs()

    expected = [
        {
            'have_errfile': True,
            'have_outfile': False,
            'completed': True
            },
        {
            'have_errfile': False,
            'have_outfile': True,
            'completed': True
            },
        {
            'have_errfile': False,
            'have_outfile': False,
            'completed': False
        }
    ]

    assert out == expected


def test_run(setup_run):
    log_file = 'teptools-' + time.strftime('%d%m%Y-%H%M') + '.log'
    config = {
        'outfile_ext': 'out',
        'interval': 0.3,
        'email': ''
    }
    watch_dirs = [
        os.path.join(fixtures_dir, 'run_error'),
        os.path.join(fixtures_dir, 'run_completed'),
        os.path.join(fixtures_dir, 'run_empty')
    ]
    expected = [
        (' tests/fixtures/run_error failed\n'),
        (' tests/fixtures/run_completed successfully completed\n')
    ]
    w = watch.Watch(watch_dirs, config)
    w.run()

    with open(log_file, 'r') as f:
        out = f.readlines()

    os.remove(log_file)

    for i in range(len(out)):
        assert out[i].endswith(expected[i])
