import os
import re
import sys

# old_licenses = [
#     r'^# This program(.|\n)*MA 02110-1301 USA..$',
#     r'^# This program(.|\n)*MA 02110-1301 USA.$',
#     r'^# This program(.|\n)*<http://www.gnu.org/licenses/>$',
# ]
# new_license = ''


# Usage
# find -name '*.py' -exec ../../projects/license/license_updater.py {} \;


def main(argv):
    for filename in argv:
        if os.path.isdir(filename):
            continue
        with open(filename, 'r+') as f:
            content = f.read()
            for old_license in old_licenses:
                output = re.sub(old_license, new_license, content, flags=re.MULTILINE)
                if content != output:
                    break
            f.seek(0)
            f.write(output)
            f.truncate()


if __name__ == "__main__":
    main(sys.argv[1:])
