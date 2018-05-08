#!/usr/local/bin/python3
import os
import subprocess
import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        project = sys.argv[1]
        module = sys.argv[2]
        test_name = module
        module_name = os.path.basename(module)
        if "test_" not in module_name:
            test_name = module.replace(module_name,
                                       "test_{}".format(module_name))
        try:
            cmd = ["python3", "-m", "unittest", test_name]
            output = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            output = output.communicate()[0].decode("utf-8")
            print(output)
        except Exception as exception:
            print(exception)
    else:
        print("Usage: run_tests <project> <module>")
