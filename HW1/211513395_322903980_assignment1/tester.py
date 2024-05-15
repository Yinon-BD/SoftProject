import subprocess
import platform
import re
#Run from directory containing kmeans.c, kmeans.py and unpacked tests directory
def main():
    output1_file_path="tests/tests/output_1.txt"
    output2_file_path="tests/tests/output_2.txt"
    output3_file_path="tests/tests/output_3.txt"
    input1_file_path="tests/tests/input_1.txt"
    input2_file_path="tests/tests/input_2.txt"
    input3_file_path="tests/tests/input_3.txt"
    python_cmd="python3"
    pattern = re.compile("Python 3[0-9]*.[0-9]+.[0-9]+")
    if not pattern.match(run_cmd(python_cmd+" --version")):
        python_cmd="python"
        if not pattern.match(run_cmd(python_cmd+" --version")):
            print("Can't find command python or python3")
            return
    
    pre_file="./"
    if platform.system() == "Windows":
        pre_file=".\\"

    cluster_error="Invalid number of clusters!\n"
    point_error="Invalid number of points!\n"
    dim_error="Invalid dimension of point!\n"
    iter_error="Invalid maximum iteration!\n"
    general_error="An Error Has Occurred\n"
    

    output1 = ""
    output2 = ""
    output3 = ""
    with open(output1_file_path) as f:
        output1 = f.read()
    with open(output2_file_path) as f:
        output2 = f.read()
    with open(output3_file_path) as f:
        output3 = f.read()
    
    #Checking no errors or warnings while compiling
    tests_passed=True
    print("0)\tTesting c compilition")
    if run_cmd("gcc -ansi -Wall -Wextra -Werror -pedantic-errors kmeans.c -o kmeans")!="":
        print("\t\tErrors or warnings while compiling C")
        tests_passed=False
    if tests_passed:
        print("\t\tPassed!")
    else:
        print("\t\tFailed!")

    #Checking exact match of outputs given in tests in python program
    tests_passed=True
    print("1)\tComparing python output to provided outputs")
    if run_cmd(python_cmd+" kmeans.py 3 800 3 600 "+input1_file_path)!=output1:
        print("\t\tError in 1.1")
        tests_passed=False
    if run_cmd(python_cmd+" kmeans.py 7 430 11 "+ input2_file_path)!=output2:
        print("\t\tError in 1.2")
        tests_passed=False
    if run_cmd(python_cmd+" kmeans.py 15 5000 5 300 "+input3_file_path)!=output3:
        print("\t\tError in 1.3")
        tests_passed=False
    if tests_passed:
        print("\t\tPassed!")
    else:
        print("\t\tFailed!")

    #Checking exact match of outputs given in tests in c program
    tests_passed=True
    print("2)\tComparing c output to provided outputs")
    if run_cmd(pre_file+"kmeans 3 800 3 600 < "+input1_file_path)!=output1:
        print("\t\tError in 2.1")
        tests_passed=False
    if run_cmd(pre_file+"kmeans 7 430 11 < "+input2_file_path)!=output2:
        print("\t\tError in 2.2")
        tests_passed=False
    if run_cmd(pre_file+"kmeans 15 5000 5 300 < "+input3_file_path)!=output3:
        print("\t\tError in 2.3")
        tests_passed=False
    if tests_passed:
        print("\t\tPassed!")
    else:
        print("\t\tFailed!")
    
    #Input error checking python
    tests_passed=True
    print("3)\tTesting python input error checking")
    if run_cmd(python_cmd+" kmeans.py 1 5000 5 300 "+input3_file_path)!=cluster_error:
        print("\t\tError in 3.1")
        tests_passed=False
    if run_cmd(python_cmd+" kmeans.py 5 5 5 "+input3_file_path)!=cluster_error:
        print("\t\tError in 3.2")
        tests_passed=False
    if run_cmd(python_cmd+" kmeans.py 10s1 5000 5 300 "+input3_file_path)!=cluster_error:
        print("\t\tError in 3.3")
        tests_passed=False
    if run_cmd(python_cmd+" kmeans.py 15 50s00 5 300 "+input3_file_path)!=point_error:
        print("\t\tError in 3.4")
        tests_passed=False
    if run_cmd(python_cmd+" kmeans.py 15 0 5 300 "+input3_file_path)!=point_error:
        print("\t\tError in 3.5")
        tests_passed=False
    if run_cmd(python_cmd+" kmeans.py 15 5000 0 300 "+input3_file_path)!=dim_error:
        print("\t\tError in 3.6")
        tests_passed=False
    if run_cmd(python_cmd+" kmeans.py 15 5000 5s 300 "+input3_file_path)!=dim_error:
        print("\t\tError in 3.7")
        tests_passed=False
    if run_cmd(python_cmd+" kmeans.py 15 5000 5 1 "+input3_file_path)!=iter_error:
        print("\t\tError in 3.8")
        tests_passed=False
    if run_cmd(python_cmd+" kmeans.py 15 5000 5 1000 "+input3_file_path)!=iter_error:
        print("\t\tError in 3.9")
        tests_passed=False
    if run_cmd(python_cmd+" kmeans.py 15 5000 5 300s "+input3_file_path)!=iter_error:
        print("\t\tError in 3.10")
        tests_passed=False
    if run_cmd(python_cmd+" kmeans.py 15 5000 "+input3_file_path)!=general_error:
        print("\t\tError in 3.11")
        tests_passed=False
    if run_cmd(python_cmd+" kmeans.py 15 5000 5 300 4 "+input3_file_path)!=general_error:
        print("\t\tError in 3.12")
        tests_passed=False
    if tests_passed:
        print("\t\tPassed!")
    else:
        print("\t\tFailed!")

    #Input error checking C
    tests_passed=True
    print("4)\tTesting c input error checking")
    if run_cmd(pre_file+"kmeans 1 800 3 600 < "+input1_file_path)!=cluster_error:
        print("\t\tError 4.1")
        tests_passed=False
    if run_cmd(pre_file+"kmeans 5 5 3 600 < "+input2_file_path)!=cluster_error:
        print("\t\tError 4.2")
        tests_passed=False
    if run_cmd(pre_file+"kmeans 10s1 800 3 600 < "+input1_file_path)!=cluster_error:
        print("\t\tError 4.3")
        tests_passed=False
    if run_cmd(pre_file+"kmeans 5 80s0 3 600 < "+input1_file_path)!=point_error:
        print("\t\tError 4.4")
        tests_passed=False
    if run_cmd(pre_file+"kmeans 5 0 3 600 < "+input1_file_path)!=point_error:
        print("\t\tError 4.5")
        tests_passed=False
    if run_cmd(pre_file+"kmeans 15 5000 0 600 < "+input1_file_path)!=dim_error:
        print("\t\tError 4.6")
        tests_passed=False
    if run_cmd(pre_file+"kmeans 15 5000 5s 600 < "+input1_file_path)!=dim_error:
        print("\t\tError 4.7")
        tests_passed=False
    if run_cmd(pre_file+"kmeans 15 5000 5 1 < "+input1_file_path)!=iter_error:
        print("\t\tError 4.8")
        tests_passed=False
    if run_cmd(pre_file+"kmeans 15 5000 5 1000 < "+input1_file_path)!=iter_error:
        print("\t\tError 4.9")
        tests_passed=False
    if run_cmd(pre_file+"kmeans 15 5000 5 300s < "+input1_file_path)!=iter_error:
        print("\t\tError 4.10")
        tests_passed=False
    if run_cmd(pre_file+"kmeans 15 5000 < "+input1_file_path)!=general_error:
        print("\t\tError 4.11")
        tests_passed=False
    if run_cmd(pre_file+"kmeans 15 5000 5 300 5 < "+input1_file_path)!=general_error:
        print("\t\tError 4.12")
        tests_passed=False
    if tests_passed:
        print("\t\tPassed!")
    else:
        print("\t\tFailed!")

    #Memory leak checks
    print("5)\tTesting c memory leaks in valgrind")
    valgrind_out = run_cmd("valgrind --version")
    pattern = re.compile("valgrind-[0-9]+.[0-9]+.[0-9]+")
    if pattern.match(valgrind_out):
        tests_passed=True
        run_cmd("valgrind --log-file=\".tester_valgrind.txt\" " + pre_file+"kmeans 1 800 3 600 < "+input1_file_path)
        with open(".tester_valgrind.txt") as f:
            valgrind_out=f.read()
        if valgrind_out.find("ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)")==-1 or valgrind_out.find("All heap blocks were freed -- no leaks are possible")==-1:
            print("\t\tError 5.1")
            tests_passed=False

        run_cmd("valgrind --log-file=\".tester_valgrind.txt\" " + pre_file + "kmeans 15 5000 5 300 < "+input3_file_path)
        with open(".tester_valgrind.txt") as f:
            valgrind_out=f.read()
        if valgrind_out.find("ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)")==-1 or valgrind_out.find("All heap blocks were freed -- no leaks are possible")==-1:
            print("\t\tError 5.2")
            tests_passed=False
        run_cmd("rm .tester_valgrind.txt")
        if tests_passed:
            print("\t\tPassed!")
        else:
            print("\t\tFailed!")
    else:
        print("\t\tValgrind not found, skipping memory leak tests.")

    #Return value of c program tests
    print("6)\tTesting return value of c program")
    tests_passed=True
    if get_ret_code(pre_file+"kmeans 15 5000 5 300 5 < "+input1_file_path)!=1:
        print("\t\tError 6.1")
        tests_passed=False
    if get_ret_code(pre_file+"kmeans 15 5000 5 300 < "+input3_file_path)!=0:
        print("\t\tError 6.2")
        tests_passed=False
    if get_ret_code(pre_file+"kmeans 1 5000 5 300 < "+input1_file_path)!=1:
        print("\t\tError 6.3")
        tests_passed=False
    if get_ret_code(pre_file+"kmeans 15 0 5 300 < "+input1_file_path)!=1:
        print("\t\tError 6.4")
        tests_passed=False
    if get_ret_code(pre_file+"kmeans 15 100s 5 300 < "+input1_file_path)!=1:
        print("\t\tError 6.5")
        tests_passed=False
    if get_ret_code(pre_file+"kmeans 15 100s 5 < "+input1_file_path)!=1:
        print("\t\tError 6.6")
        tests_passed=False
    if get_ret_code(pre_file+"kmeans 15 5000 < "+input1_file_path)!=1:
        print("\t\tError 6.7")
        tests_passed=False
    if get_ret_code(pre_file+"kmeans 15 5000 0 < "+input1_file_path)!=1:
        print("\t\tError 6.8")
        tests_passed=False
    if get_ret_code(pre_file+"kmeans 15 5000 5 1 < "+input1_file_path)!=1:
        print("\t\tError 6.9")
        tests_passed=False
    if get_ret_code(pre_file+"kmeans 15 5000 5 1000 < "+input1_file_path)!=1:
        print("\t\tError 6.10")
        tests_passed=False
    if tests_passed:
        print("\t\tPassed!")
    else:
        print("\t\tFailed!")

    
    print("---------All tests are done!---------")

def run_cmd(cmd):
    s=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout.read().decode()
    if platform.system() == "Windows":
        s = s.replace("\r","")
    return s

def get_ret_code(cmd):
    return subprocess.run(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).returncode


    



if __name__=="__main__":
    main()