"""Extract gzip files from '.sgn' files.

   A '.sgn' file has a signature placed at the beginning of the file. The
   only thing this tool does is removing the signature.

   This tool is based on cnu_fpu. See http://virtualab.ru/en/projects/cnu-fpu
   for the original project.
"""

GZIP_MAGIC_NUMBER_ = '\x1f\x8b'


class InvalidFileError(Exception):
    pass


def unsign_from_fileobj(f_in, f_out):
    bytes_in = f_in.read()
    index = bytes_in.find(GZIP_MAGIC_NUMBER_)
    if index == -1:
        raise InvalidFileError('This .sgn file doesn\'t hold a gzip file')
    f_out.write(bytes_in[index:])


def unsign_from_filename(path_in, path_out):
    f_in = open(path_in, 'rb')
    try:
        f_out = open(path_out, 'wb')
        try:
            unsign_from_fileobj(f_in, f_out)
        finally:
            f_out.close()
    finally:
        f_in.close()


if __name__ == '__main__':
    import os.path
    import sys

    if len(sys.argv) not in (2, 3):
        print >> sys.stderr, '%s input_file [output_file]' % sys.argv[0]
        raise SystemExit(1)
    else:
        path_in = sys.argv[1]
        if len(sys.argv) == 3:
            path_out = sys.argv[2]
        else:
            path_out = path_in.split('.', 1)[0] + '.tgz'
            if path_in == path_out:
                print >> sys.stderr, 'Could not determine an output filename. Specify an output file.'
                raise SystemExit(2)
        unsign_from_filename(path_in, os.path.basename(path_out))
