# import argparse
import os
# from openTEPES.openTEPES import openTEPES_run
# import openTEPES.openTEPES as oT
import openTEPES.openTEPES as oT
# import openTEPES

CWD = os.getcwd()
TEST_PATH = CWD + '/openTEPES'
os.chdir(TEST_PATH)

CASE = "9n"
# parser = argparse.ArgumentParser(description='Introducing main parameters.')
# parser.add_argument('--case', type=str, default=None)
# parser.add_argument('--dir', type=str, default=None)
# parser.add_argument('--solver', type=str, default=None)
# DIR = os.path.dirname(openTEPES.__file__)
DIR = TEST_PATH
SOLVER = "gurobi"

oT.openTEPES_run(DIR, CASE, SOLVER)
# def test_openTEPES():
#     assert mTEPES == oT.openTEPES_run(DIR, CASE, SOLVER)


# if __name__ == "__main__":
#     test_openTEPES(DIR, CASE, SOLVER)