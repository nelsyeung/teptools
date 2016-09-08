#!/usr/bin/env python3
import os
import argparse
import shutil


def parser(args):
    """Return parsed command line arguments."""
    parser = argparse.ArgumentParser(
        description=('Install teptools.'),
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument(
        '--prefix', default='~',
        help='Install prefix (default: ~)\n'
             'teptools will be installed to $PREFIX/.teptools\n')

    parser.add_argument(
        '-y', '--yes', action='store_true',
        help='Install without confirmation message.')

    return parser.parse_args(args)


def main(args=None, rcfile=None):
    args = parser(args)
    homedir = os.path.expanduser('~')
    install_path = os.path.join(
        os.path.expandvars(os.path.expanduser(args.prefix)),
        '.teptools')

    if not args.yes:
        confirm = input('Are you sure you want to install teptools to\n' +
                        install_path + '\n' +
                        'This will overwrite any existing copies of teptools' +
                        ' [y/N]? ').lower()
        if confirm != 'y' and confirm != 'yes':
            print('teptools will not be installed.')
            return

    if not os.path.isdir(install_path):
        os.mkdir(install_path)

    for filename in os.listdir('teptools'):
        if (filename.endswith('.py') or
                filename.endswith('.pyc') or
                filename == '__pycache__' or
                filename == 'teptoolsrc.default'):
            continue

        filepath = os.path.join('teptools', filename)

        if os.path.isdir(filepath):
            shutil.copytree(filepath, install_path, symlinks=True)

        shutil.copy(filepath, install_path)

    shutil.copy('teptools/helpers.py',
                os.path.join(homedir, '.teptools'))

    if not os.path.isfile(os.path.join(homedir, '.teptoolsrc')):
        print('teptools configuration file not found,'
              'installing default configuration file to $HOME/.teptoolsrc')
        shutil.copy('teptools/teptoolsrc.default',
                    os.path.join(homedir, '.teptoolsrc'))

    print('teptools installed to ' + install_path + '\n\n'
          'To enable the full range of teptools features\n'
          'you must `source` the `tep.sh` script within the installed path\n\n'
          '  $ source ' + install_path + '/tep.sh\n\n'
          'It is recommended that you add the above command into your\n'
          '.bashrc or .bash_profile.\n\n'
          'If you have any problems please check the repository\n'
          'for the full documentation:\n'
          'https://github.com/nelsyeung/teptools')

if __name__ == '__main__':
    main()
