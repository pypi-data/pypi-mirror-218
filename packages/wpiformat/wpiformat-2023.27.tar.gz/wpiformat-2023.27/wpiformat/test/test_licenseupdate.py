from datetime import date
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

from .test_tasktest import *
from wpiformat.config import Config
from wpiformat.licenseupdate import LicenseUpdate


class OpenTemporaryDirectory:
    def __init__(self):
        self.prev_dir = os.getcwd()

    def __enter__(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        os.chdir(self.temp_dir.name)
        return self.temp_dir

    def __exit__(self, type, value, traceback):
        os.chdir(self.prev_dir)


def test_licenseupdate():
    year = str(date.today().year)

    task = LicenseUpdate()
    test = TaskTest(task)

    file_appendix = (
        "#pragma once"
        + os.linesep
        + os.linesep
        + "#include <iostream>"
        + os.linesep
        + os.linesep
        + "int main() {"
        + os.linesep
        + '  std::cout << "Hello World!";'
        + os.linesep
        + "}"
    )

    # pragma once at top of file
    test.add_input("./Test.h", file_appendix)
    test.add_output(
        "/*                                Company Name                                */"
        + os.linesep
        + "/* Copyright (c) {} Company Name. All Rights Reserved.                      */".format(
            year
        )
        + os.linesep
        + os.linesep
        + file_appendix,
        True,
    )

    # pragma once at top of file preceded by newline
    test.add_input("./Test.h", os.linesep + file_appendix)
    test.add_output(
        "/*                                Company Name                                */"
        + os.linesep
        + "/* Copyright (c) {} Company Name. All Rights Reserved.                      */".format(
            year
        )
        + os.linesep
        + os.linesep
        + file_appendix,
        True,
    )

    # File containing up-to-date license preceded by newline
    test.add_input(
        "./Test.h",
        os.linesep
        + "/*                                Company Name                                */"
        + os.linesep
        + "/* Copyright (c) {} Company Name. All Rights Reserved.                      */".format(
            year
        )
        + os.linesep
        + os.linesep
        + file_appendix,
    )
    test.add_output(
        "/*                                Company Name                                */"
        + os.linesep
        + "/* Copyright (c) {} Company Name. All Rights Reserved.                      */".format(
            year
        )
        + os.linesep
        + os.linesep
        + file_appendix,
        True,
    )

    # File containing up-to-date range license
    test.add_input(
        "./Test.h",
        "/*                                Company Name                                */"
        + os.linesep
        + "// Copyright (c) 2011-{} Company Name. All Rights Reserved.".format(year)
        + os.linesep
        + os.linesep
        + file_appendix,
    )
    test.add_output(
        "/*                                Company Name                                */"
        + os.linesep
        + "/* Copyright (c) 2011-{} Company Name. All Rights Reserved.                 */".format(
            year
        )
        + os.linesep
        + os.linesep
        + file_appendix,
        True,
    )

    # File containing up-to-date license with one year
    test.add_input(
        "./Test.h",
        "/*                                Company Name                                */"
        + os.linesep
        + "/* Copyright (c) {} Company Name. All Rights Reserved.                      */".format(
            year
        )
        + os.linesep
        + os.linesep
        + file_appendix,
    )
    test.add_latest_input_as_output(True)

    # File with three newlines between license and include guard
    test.add_input(
        "./Test.h",
        "/*                                Company Name                                */"
        + os.linesep
        + "/* Copyright (c) {} Company Name. All Rights Reserved.                      */".format(
            year
        )
        + os.linesep
        + os.linesep
        + os.linesep
        + file_appendix,
    )
    test.add_output(
        "/*                                Company Name                                */"
        + os.linesep
        + "/* Copyright (c) {} Company Name. All Rights Reserved.                      */".format(
            year
        )
        + os.linesep
        + os.linesep
        + file_appendix,
        True,
    )

    # File with only one newline between license and include guard
    test.add_input(
        "./Test.h",
        "/*                                Company Name                                */"
        + os.linesep
        + "/* Copyright (c) {} Company Name. All Rights Reserved.                      */".format(
            year
        )
        + os.linesep
        + file_appendix,
    )
    test.add_output(
        "/*                                Company Name                                */"
        + os.linesep
        + "/* Copyright (c) {} Company Name. All Rights Reserved.                      */".format(
            year
        )
        + os.linesep
        + os.linesep
        + file_appendix,
        True,
    )

    # File with multiline comment spanning multiple lines of license header
    test.add_input(
        "./Test.h",
        "/*"
        + os.linesep
        + " * Autogenerated file! Do not manually edit this file. This version is regenerated"
        + os.linesep
        + " * any time the publish task is run, or when this file is deleted."
        + os.linesep
        + " */"
        + os.linesep
        + os.linesep
        + 'const char* WPILibVersion = "";',
    )
    test.add_output(
        "/*                                Company Name                                */"
        + os.linesep
        + "/* Copyright (c) {} Company Name. All Rights Reserved.                      */".format(
            year
        )
        + os.linesep
        + os.linesep
        + "/*"
        + os.linesep
        + " * Autogenerated file! Do not manually edit this file. This version is regenerated"
        + os.linesep
        + " * any time the publish task is run, or when this file is deleted."
        + os.linesep
        + " */"
        + os.linesep
        + os.linesep
        + 'const char* WPILibVersion = "";',
        True,
    )

    # File containing license year range in different postion than template
    # (If the year isn't extracted, the range will be replaced with one year and
    # the test will fail.)
    test.add_input(
        "./Test.h",
        "/*                                Company Name                                */"
        + os.linesep
        + "/* Copyright (c) Company Name 2011-{}. All Rights Reserved.                 */".format(
            year
        )
        + os.linesep
        + os.linesep
        + file_appendix,
    )
    test.add_output(
        "/*                                Company Name                                */"
        + os.linesep
        + "/* Copyright (c) 2011-{} Company Name. All Rights Reserved.                 */".format(
            year
        )
        + os.linesep
        + os.linesep
        + file_appendix,
        True,
    )

    # Ensure "/*" after "*/" on same line is detected
    test.add_input(
        "./Test.h",
        "/*----------------------------------------------------------------------------*/"
        + os.linesep
        + "/* Copyright (c) 2011 FIRST. All Rights Reserved.                             */"
        + os.linesep
        + "/* Open Source Software - may be modified and shared by FRC teams. The code   */"
        + os.linesep
        + "/* must be accompanied by the FIRST BSD license file in the root directory of */"
        + os.linesep
        + "/* the project.                                                               */"
        + os.linesep
        + "/*----------------------------------------------------------------------------*//*"
        + os.linesep
        + os.linesep
        + "blah"
        + os.linesep
        + os.linesep
        + "*/"
        + os.linesep,
    )
    test.add_output(
        "/*                                Company Name                                */"
        + os.linesep
        + "/* Copyright (c) 2011-{} Company Name. All Rights Reserved.                 */".format(
            year
        )
        + os.linesep
        + os.linesep,
        True,
    )

    # File excluded from license update isn't modified
    test.add_input(
        "./Excluded.h",
        "/* Copyright (c) Company Name 2011-{}. */".format(year)
        + os.linesep
        + os.linesep
        + file_appendix,
    )
    test.add_latest_input_as_output(True)

    # Ensure license regex matches
    test.add_input(
        "./Test.h",
        "/* Company Name */"
        + os.linesep
        + "/* Copyright (c) 1992-2015 Company Name. All Rights Reserved. */"
        + os.linesep
        + os.linesep
        + file_appendix,
    )
    test.add_output(
        "/*                                Company Name                                */"
        + os.linesep
        + "/* Copyright (c) 1992-"
        + year
        + " Company Name. All Rights Reserved.                 */"
        + os.linesep
        + os.linesep
        + file_appendix,
        True,
    )

    # Ensure excluded files won't be processed
    config_file = Config(os.path.abspath(os.getcwd()), ".styleguide")
    assert not task.should_process_file(config_file, "./Excluded.h")

    # Create git repo to test license years for commits
    with OpenTemporaryDirectory():
        subprocess.run(["git", "init", "-q"])

        # Add base files
        with open(".styleguide-license", "w") as file:
            file.write("// Copyright (c) {year}")
        with open(".styleguide", "w") as file:
            file.write("cppSrcFileInclude {\n" + r"\.cpp$")
        subprocess.run(["git", "add", ".styleguide-license"])
        subprocess.run(["git", "add", ".styleguide"])
        subprocess.run(["git", "commit", "-q", "-m", '"Initial commit"'])

        # Add file with commit date of last year and range through this year
        with open("last-year.cpp", "w") as file:
            file.write(f"// Copyright (c) 2017-{year}")
        subprocess.run(["git", "add", "last-year.cpp"])
        subprocess.run(["git", "commit", "-q", "-m", '"Last year"'])
        last_iso_year = f"{int(year) - 1}-01-01T00:00:00"
        subprocess.Popen(
            ["git", "commit", "-q", "--amend", "--no-edit", f"--date={last_iso_year}"],
            env={**os.environ, "GIT_COMMITTER_DATE": last_iso_year},
        ).wait()

        # Add file with commit date of this year and range through this year
        with open("this-year.cpp", "w") as file:
            file.write(f"// Copyright (c) 2017-{year}")
        subprocess.run(["git", "add", "this-year.cpp"])
        subprocess.run(["git", "commit", "-q", "-m", '"This year"'])

        # Add file with commit date of next year and range through this year
        with open("next-year.cpp", "w") as file:
            file.write(f"// Copyright (c) 2017-{year}")
        subprocess.run(["git", "add", "next-year.cpp"])
        subprocess.run(["git", "commit", "-q", "-m", '"Next year"'])
        next_iso_year = f"{int(year) + 1}-01-01T00:00:00"
        subprocess.Popen(
            ["git", "commit", "-q", "--amend", "--no-edit", f"--date={next_iso_year}"],
            env={**os.environ, "GIT_COMMITTER_DATE": next_iso_year},
        ).wait()

        # Create uncommitted file with no year
        Path("no-year.cpp").touch()

        # Run wpiformat on last-year.cpp
        with open("last-year.cpp", "r") as input:
            lines = input.read()
        output, success = task.run_pipeline(config_file, "last-year.cpp", lines)
        assert output == f"// Copyright (c) 2017-{int(year) - 1}\n\n"

        # Run wpiformat on last-year.cpp with uncommitted changes. It should
        # update to next year instead of keeping previous year
        with open("last-year.cpp", "a") as input:
            input.write("change\n")
        output, success = task.run_pipeline(
            config_file, "last-year.cpp", lines + "change\n"
        )
        assert output == f"// Copyright (c) 2017-{year}\n\nchange\n"

        # Erase changes made to last-year.cpp in previous test
        with open("last-year.cpp", "w") as input:
            input.write(lines)

        # Run wpiformat on this-year.cpp
        with open("last-year.cpp", "r") as input:
            lines = input.read()
        output, success = task.run_pipeline(config_file, "this-year.cpp", lines)
        assert output == f"// Copyright (c) 2017-{year}\n\n"

        # Run wpiformat on next-year.cpp
        with open("next-year.cpp", "r") as input:
            lines = input.read()
        output, success = task.run_pipeline(config_file, "next-year.cpp", lines)
        assert output == f"// Copyright (c) 2017-{int(year) + 1}\n\n"

        # Run wpiformat on no-year.cpp
        # Should have current calendar year
        with open("no-year.cpp", "r") as input:
            lines = input.read()
        output, success = task.run_pipeline(config_file, "no-year.cpp", lines)
        assert output == f"// Copyright (c) {year}\n\n"

    test.run(OutputType.FILE)
