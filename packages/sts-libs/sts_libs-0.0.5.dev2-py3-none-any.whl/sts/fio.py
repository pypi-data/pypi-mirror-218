"""fio.py: Module to run FIO util."""

#  Copyright: Contributors to the sts project
#  GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import os
import subprocess
import sys

from sts import linux
from sts.utils.cmdline import exists, run, run_ret_out

fio_default_options = {
    "rw": "randrw",  # Type of I/O pattern. Supported(read, write, trim, randread, randwrite, rw, randrw, trimwrite)
    "name": "fio_test",  # signalling the start of a new job.
    "filename": None,  # device or filename
    "direct": 1,  # If true, use non-buffered I/O (usually O_DIRECT)
    "iodepth": 1,  # Number  of  I/O  units  to keep in flight against the file. Note that increasing
    # iodepth beyond 1 will not affect synchronous ioengines
    "runtime": None,  # Terminate processing after the specified number of seconds.
    "size": None,  #
    "time_based": None,  # If given, run for the specified runtime duration even if the files are
    # completely read or written.
    "numjobs": 1,  # Number of clones (processes/threads performing the same workload) of this job
    "bs": "4k",  # lock  size for I/O units.
    "verify": None,  # Method  of verifying file contents after each iteration of the job
}  # (supports: md5 crc16 crc32 crc32c crc32c-intel crc64 crc7 sha256 sha512 sha1 xxhash)

fio_default_verify_options = {
    "verify_backlog": 1024,  # fio will write only N blocks before verifying these blocks.
    # Set to None to verify after all IO is written
    "verify_fatal": 1,  # If true, exit the job on the first observed verification failure
    "do_verify": 1,
    "verify": "crc32c",
}


def install_fio():  # noqa: ANN201
    pkg = "fio"
    if linux.install_package(pkg):
        return True
    if run("fio >/dev/null 2>&1").returncode == 1:
        return True
    # Try to install FIO from source
    return install_fio_from_src()


def install_fio_from_src():  # noqa: ANN201
    git_url = "git://git.kernel.org/pub/scm/linux/kernel/git/axboe/fio.git"

    if not linux.install_package("libaio-devel"):
        print("FAIL: Could not install libaio-devel")
        return False

    if not linux.install_package("zlib-devel"):
        print("FAIL: Could not install zlib-devel")
        return False

    if run(f"git clone {git_url}").returncode != 0:
        print("FAIL: Could not clone fio repo")
        return False

    print("INFO: Installing FIO")
    if run("cd fio && ./configure && make && make install").returncode != 0:
        print("FAIL: Could not build fio")
        return False

    if not exists("fio"):
        print("FAIL: FIO did not install properly")
        return False
    return True


# TODO: rewrite to cmdline.run()
def fio_stress(of, verbose=False, return_output=False, **fio_opts):  # noqa: ANN001, ANN003, ANN201
    # For compatibility with tests using other named parameters
    convert_param = {
        "io_type": "rw",
        "time": "runtime",
        "thread": "numjobs",
        "log_file": "output",
    }

    for key in convert_param:
        if key in list(fio_opts.keys()):
            fio_opts[convert_param[key]] = fio_opts.pop(key)

    fio_opts["filename"] = of

    for opt in fio_default_options:
        if opt not in list(fio_opts.keys()):
            fio_opts[opt] = fio_default_options[opt]

    if int(fio_opts["numjobs"]) > 1:
        fio_opts["group_reporting"] = 1

    if fio_opts["verify"] is not None:
        fio_opts.update(fio_default_verify_options)

    if not exists("fio"):
        print("FATAL: fio is not installed")
        return False

    fio_param = ""
    for key in list(fio_opts.keys()):
        if fio_opts[key]:
            fio_param += f"--{key}='{fio_opts[key]}' "

    if "fiojob" in list(fio_opts.keys()):
        fio_param = f"{fio_opts['fiojob']} --filename={fio_opts['filename']}"

    cmd = f"fio {fio_param}"
    # Append time information to command
    date = 'date "+%Y-%m-%d %H:%M:%S"'
    p = subprocess.Popen(date, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, _ = p.communicate()
    stdout = stdout.decode("ascii", "ignore")
    stdout = stdout.rstrip("\n")
    if not verbose:  # If verbose option is selected, the run() will print the fio command.
        print(f"INFO: [{stdout}] FIO Running: '{cmd}'...")

    # print("INFO: Running %s" % cmd)
    retcode, output = run_ret_out(cmd, return_output=True, verbose=verbose)
    if retcode != 0:
        print("FAIL: running FIO")
        print(output)
        if return_output:
            return False, None
        return False

    print("INFO: FIO executed successfully")
    if return_output:
        return True, output

    return True


def fio_stress_background(of, verbose=False, **fio_opts):  # noqa: ANN001, ANN003, ANN201
    """Run FIO on background."""
    newpid = os.fork()
    if newpid == 0:
        # Trying to flush stdout to avoid duplicated lines when running hba_test
        sys.stdout.flush()
        rt = fio_stress(of, verbose=verbose, **fio_opts)
        if not rt:
            os._exit(1)  # noqa: SLF001
        os._exit(0)  # noqa: SLF001
        return None

    sys.stdout.flush()
    print("INFO: fio_stress_background(): Child thread %d is running FIO Stress" % newpid)
    return newpid
