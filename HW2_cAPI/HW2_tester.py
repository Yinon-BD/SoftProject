import subprocess
import platform
import re
import argparse
import csv
import os
import numpy as np
import pandas as pd
def main():
    parser = argparse.ArgumentParser(description="Tester for HW2 in the course Software Project TAU 2024a")
    parser.add_argument("-n",action="store_true",help="Skip deleting build directory and rebuilding")
    parser.add_argument("--fix_files",action="store_true",help="fix outputs file formatting to .4f")
    parser.add_argument("--mingw32",action="store_true",help="Specify mingw32 compiler, used on windows to compile using gcc port")
    parser.add_argument("--cygwin",action="store_true",help="Specify cygwin compiler, used on windows to compile using gcc port")
    parser.add_argument("--cmp",action="store_true",help="Compare your program to the refrence written in this tester")
    parser.add_argument("--mem",action="store_true",help="Brute force check for memory leaks")
    args = parser.parse_args()
    mem_test_file_contents= ""
    prog_name = "kmeans_pp.py"
    pre_file="./"
    rmv_file_cmd = "rm"
    rmv_dir_cmd = "rm -r"
    copy_cmd = "cp"
    slash = "/"
    if platform.system() == "Windows":
        pre_file=".\\"
        rmv_file_cmd = "del"
        rmv_dir_cmd = "rmdir /s /q"
        copy_cmd = "copy"
        slash = "\\"
    output_files= [f"tests{slash}output_{i+1}.txt" for i in range(3)]
    input_files= [[f"tests{slash}input_{i+1}_db_{j+1}.txt" for j in range(2)] for i in range(3)]
    csv_input_files = [[fp[:fp.rfind(".")]+".csv" for fp in inputs] for inputs in input_files]
    python_cmd="python3"
    pattern = re.compile("Python 3[0-9]*.[0-9]+.[0-9]+")
    if not pattern.match(run_cmd(python_cmd+" --version")):
        python_cmd="python"
        if not pattern.match(run_cmd(python_cmd+" --version")):
            print("Can't find command python or python3")
            return

    cluster_error="Invalid number of clusters!\n"
    iter_error="Invalid maximum iteration!\n"
    epsilon_error ="Invalid epsilon!\n"
    general_error="An Error Has Occurred\n"
    errors = [cluster_error,iter_error,epsilon_error,general_error]
    if args.fix_files:
        output_file_formatter(output_files)
    outputs=[]
    for file_p in output_files:
        with open(file_p) as f:
            outputs.append(f.read())

    for i in range(len(input_files)):
        for j in range(len(input_files[i])):
            run_cmd(f"{copy_cmd} {input_files[i][j]} {csv_input_files[i][j]}")

    if not args.n:#Add flag -n to skip this step or flags --mingw32/--cygwin to specify compiler
        run_cmd(f"{rmv_dir_cmd} -r build")
        #Checking no errors or warnings while pcompiling
        tests_passed=True
        print("0)\tTesting setup.py build")
        cmd = f"{python_cmd} setup.py build_ext --inplace"
        if args.cygwin:
            cmd += " --compiler=cygwin"
        elif args.mingw32:
            cmd += " --compiler=mingw32"
        cmd_out = run_cmd(cmd)
        if cmd_out.find("warning") != -1 or cmd_out.find("failed with") != -1:
            print("\t\tErrors or warnings while building c extention")
            print("Output was "+cmd_out)
            tests_passed=False
        if tests_passed:
            print("\t\tPassed!")
        else:
            print("\t\tFailed!")

    #Checking exact match of outputs given in tests in python program
    tests_passed=True
    print("1)\tComparing program output to provided outputs")
    
    if run_cmd(f"{python_cmd} {prog_name} 3 333 0 {input_files[0][0]} {input_files[0][1]}")!=outputs[0]:
        print("\t\tError in 1.1")
        cmd_out = run_cmd(f"{python_cmd} {prog_name} 3 333 0 {input_files[0][0]} {input_files[0][1]}")
        print_diff(cmd_out,outputs[0])
        tests_passed=False
    if run_cmd(f"{python_cmd} {prog_name} 7 0 {input_files[1][0]} {input_files[1][1]}")!=outputs[1]:
        print("\t\tError in 1.2")
        cmd_out = run_cmd(f"{python_cmd} {prog_name} 7 0 {input_files[1][0]} {input_files[1][1]}")
        print_diff(cmd_out,outputs[1])
        tests_passed=False
    if run_cmd(f"{python_cmd} {prog_name} 15 750 0 {input_files[2][0]} {input_files[2][1]}")!=outputs[2]:
        print("\t\tError in 1.3")
        cmd_out = run_cmd(f"{python_cmd} {prog_name} 15 750 {input_files[2][0]} {input_files[2][1]}")
        print_diff(cmd_out,outputs[2])
        tests_passed=False
    if tests_passed:
        print("\t\tPassed!")
    else:
        print("\t\tFailed!")
        print("\t\toutput files might not be in the right format (.4f),")
        print("\t\tyou can run tester with --fix_files to convert them")

    #Input error checking python
    tests_passed=True
    print("2)\tTesting program input error checking (might take a while, python startup with c extentions is slow)")
    if run_cmd(f"{python_cmd} {prog_name} 1 750 0 {input_files[2][0]} {input_files[2][1]}")!=cluster_error:
        print("\t\tError in 2.1")
        tests_passed=False
    if run_cmd(f"{python_cmd} {prog_name} 100 750 0 {input_files[0][0]} {input_files[0][1]}")!=cluster_error:
        print("\t\tError in 2.2")
        tests_passed=False
    if run_cmd(f"{python_cmd} {prog_name} 15s 750 0 {input_files[2][0]} {input_files[2][1]}")!=cluster_error:
        print("\t\tError in 2.3")
        tests_passed=False
    if run_cmd(f"{python_cmd} {prog_name} 1s5 750 0 {input_files[2][0]} {input_files[2][1]}")!=cluster_error:
        print("\t\tError in 2.4")
        tests_passed=False
    if run_cmd(f"{python_cmd} {prog_name} 15 0 0 {input_files[2][0]} {input_files[2][1]}")!=iter_error:
        print("\t\tError in 2.5")
        tests_passed=False
    if run_cmd(f"{python_cmd} {prog_name} 15 1000 0 {input_files[2][0]} {input_files[2][1]}")!=iter_error:
        print("\t\tError in 2.6")
        tests_passed=False
    if run_cmd(f"{python_cmd} {prog_name} 15 750s 0 {input_files[2][0]} {input_files[2][1]}")!=iter_error:
        print("\t\tError in 2.7")
        tests_passed=False
    if run_cmd(f"{python_cmd} {prog_name} 15 7s50 0 {input_files[2][0]} {input_files[2][1]}")!=iter_error:
        print("\t\tError in 2.8")
        tests_passed=False
    if run_cmd(f"{python_cmd} {prog_name} 15 750 0s {input_files[2][0]} {input_files[2][1]}")!=epsilon_error:
        print("\t\tError in 2.9")
        tests_passed=False
    if run_cmd(f"{python_cmd} {prog_name} 15 750 s0 {input_files[2][0]} {input_files[2][1]}")!=epsilon_error:
        print("\t\tError in 2.10")
        tests_passed=False
    if run_cmd(f"{python_cmd} {prog_name} 15 750 -1 {input_files[2][0]} {input_files[2][1]}")!=epsilon_error:
        print("\t\tError in 2.11")
        tests_passed=False
    if run_cmd(f"{python_cmd} {prog_name} 15 {input_files[2][0]} {input_files[2][1]}")!=general_error:
        print("\t\tError in 2.12")
        tests_passed=False
    if run_cmd(f"{python_cmd} {prog_name} 15 750 0 2 {input_files[2][0]} {input_files[2][1]}")!=general_error:
        print("\t\tError in 2.13")
        tests_passed=False
    cmd_out = run_cmd(f"{python_cmd} {prog_name} 15 750 0.1 {input_files[2][0]} {input_files[2][1]}")
    if cmd_out in errors:
        print("\t\tError in 2.14")#checks programs works with float input
        tests_passed=False
    if run_cmd(f"{python_cmd} {prog_name} 15 750 -0.1 {input_files[2][0]} {input_files[2][1]}")!= epsilon_error:
        print("\t\tError in 2.15")
        tests_passed=False
    if run_cmd(f"{python_cmd} {prog_name} 15 750 -1 {input_files[2][0]} {input_files[2][1]}")!= epsilon_error:
        print("\t\tError in 2.16")
        tests_passed=False
    if run_cmd(f"{python_cmd} {prog_name} 15 750 0.1s {input_files[2][0]} {input_files[2][1]}")!= epsilon_error:
        print("\t\tError in 2.17")
        tests_passed=False
    if tests_passed:
        print("\t\tPassed!")
    else:
        print("\t\tFailed!")

    tests_passed=True
    print("3)\tTesting program with csv")
    if run_cmd(f"{python_cmd} {prog_name} 15 750 0.0 {csv_input_files[2][0]} {csv_input_files[2][1]}")!= outputs[2]:
        print("\t\tError in 3")
        tests_passed=False
    if tests_passed:
        print("\t\tPassed!")
    else:
        print("\t\tFailed!")

    tests_passed=True
    print("4)\tTesting with absolute path")
    cmd_out = run_cmd(f"{python_cmd} {prog_name} 7 0 \"{os.path.abspath(input_files[1][0])}\" \"{os.path.abspath(input_files[1][1])}\"")
    if cmd_out != outputs[1]:
        print("\t\tError in 4")
        tests_passed=False
    if tests_passed:
        print("\t\tPassed!")
    else:
        print("\t\tFailed!")

    if args.cmp:#Add flag --cmp
        print("5)\tComparing with refrence (takes a few minutes)")
        for num_clusters in range(3,12):
            cmd_out = run_cmd(f"{python_cmd} {prog_name} {num_clusters} 0 {input_files[1][0]} {input_files[1][1]}")
            ref=get_kmeanspp_str(*kmeanspp(load_data_points(input_files[1][0],input_files[1][1]),num_clusters,300,0))
            if cmd_out != ref:
                print(f"\t\tError in 5 : clusters={num_clusters}, epsilon={0}")
                tests_passed=False
                break
            cmd_out = run_cmd(f"{python_cmd} {prog_name} {num_clusters} 0.1 {input_files[1][0]} {input_files[1][1]}")
            ref=get_kmeanspp_str(*kmeanspp(load_data_points(input_files[1][0],input_files[1][1]),num_clusters,300,0.1))
            if cmd_out != ref:
                print(f"\t\tError in 5 : clusters={num_clusters}, epsilon={0.1}")
                tests_passed=False
                break
            cmd_out = run_cmd(f"{python_cmd} {prog_name} {num_clusters} 0.2 {input_files[1][0]} {input_files[1][1]}")
            ref=get_kmeanspp_str(*kmeanspp(load_data_points(input_files[1][0],input_files[1][1]),num_clusters,300,0.2))
            if cmd_out != ref:
                print(f"\t\tError in 5 : clusters={num_clusters}, epsilon={0.2}")
                tests_passed=False
                break

        df1 = pd.read_csv(input_files[2][0],header=None)
        df2 = pd.read_csv(input_files[2][1],header=None)
        df1 = pd.merge(df1,df2,how="inner",left_on=0,right_on=0)
        # (range of points from input3 ({low}:{high}), num_clusters, max_iter, epsilon)
        params = [(300,700,10,300,0.001),(1000,1500,15,400,0.0),(1100,1200,7,50,0.01),(4444,4899,20,450,0.1)]
        split_col = df1.shape[1]//2 -1
        new_csv_1 = "cmp_test_1.csv"
        new_csv_2 = "cmp_test_2.csv"
        for r in params:

            df1.iloc[r[0]:r[1],:split_col].to_csv(new_csv_1,header=None)
            df1.iloc[r[0]:r[1],split_col:].to_csv(new_csv_2,header=None)
            cmd_out = run_cmd(f"{python_cmd} {prog_name} {r[2]} {r[3]} {r[4]} {new_csv_1} {new_csv_2}")
            ref=get_kmeanspp_str(*kmeanspp(load_data_points(new_csv_1,new_csv_2),r[2],r[3],r[4]))
            if cmd_out != ref:
                print(f"\t\tError in 5 : params={r}")
                tests_passed=False
                break
        run_cmd(f"{rmv_file_cmd} {new_csv_1}")
        run_cmd(f"{rmv_file_cmd} {new_csv_2}")
        if tests_passed:
            print("\t\tPassed!")
        else:
            print("\t\tFailed!")
    if args.mem:#Add flag --mem
        #requires psutil module and requires that your call to the c extention
        #is mykmeanssp.fit and in its own line (end of line is closing parenthesis of the call).
        #Also assumes not prints from c extention.
        print("6)\tChecking for memory leak")
        create_mem_test_file("mem_test.py",500)
        tests_passed = True
        try:
            cmd_out = run_cmd(f"{python_cmd} mem_test.py 15 750 0.5 {input_files[2][0]} {input_files[2][1]}")
            mem_ratio = float(cmd_out)
            if mem_ratio > 1.05:
                print(f"\t\tError in 6, Memory leak likely (mem_end/mem_start)={mem_ratio}")
                tests_passed = False
        except:
            tests_passed = False
        run_cmd(f"{rmv_file_cmd} mem_test.py")
        if tests_passed:#if no big memory leaks test for small ones
            create_mem_test_file("mem_test.py",20000)
            try:
                cmd_out = run_cmd(f"{python_cmd} mem_test.py 15 750 0.5 {input_files[2][0]} {input_files[2][1]}")
                mem_ratio = float(cmd_out)
                if mem_ratio > 1.05:
                    print(f"\t\tError in 6, Memory leak likely (mem_end/mem_start)={mem_ratio}")
                    tests_passed = False
            except:
                tests_passed = False
            run_cmd(f"{rmv_file_cmd} mem_test.py")
        if tests_passed:
            print("\t\tPassed!")
        else:
            print("\t\tFailed!")
    #file cleanup
    for inputs in csv_input_files:
        for fp in inputs:
            run_cmd(f"{rmv_file_cmd} {fp}")
    print("---------All tests are done!---------")

def run_cmd(cmd,stderr=False):
    s=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read().decode()
    if platform.system() == "Windows":
        s = s.replace("\r","")
    return s
def get_ret_code(cmd):
    return subprocess.run(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).returncode


def print_diff(output,expected_output):
    if output == expected_output:
        return
    print(f"len(Your output)={len(output)}, len(Expected output)={len(expected_output)}")
    for i in range(min(len(expected_output),len(output))):
        if expected_output[i]!=output[i]:
            print("first difference between your output and the expected output:")
            print(f"---> {output[i:]}")
            print(f"---> {expected_output[i:]}")
            return
    print("Reached end of the shorter output without finding a differnce,")
    
def output_file_formatter(output_files):
    for file_p in output_files:
        with open(file_p) as f:
            s=""
            s+=f.readline()
            csv_reader = csv.reader(f,delimiter=",")
            outputs = [tuple([float(f) for f in l]) for l in csv_reader if '' not in l]
            for m in outputs:
                for x in m:
                    s+="{:.4f},".format(x)
                s=s[:len(s)-1]+"\n"
        with open(file_p,"w",newline="\n") as f:
            f.write(s)

#### Refrence Kmeans++ ####
def get_kmeanspp_str(indices,means):
    return indices_str(indices) + kmeans_str(means)
def indices_str(indices):
    output=""
    for i in indices:
        output+= f"{i},"
    return output[:len(output)-1]+"\n"
def kmeans_str(means):
    output=""
    for m in means:
        for x in m:
            output+="{:.4f},".format(x)
        output=output[:len(output)-1]+"\n"
    return output

def kmeanspp(data_points,num_clusters,max_iter,epsilon):
    init_means, init_indices = get_init_kmeanspp(data_points,num_clusters)
    return init_indices,kmeans(num_clusters,data_points,init_means,max_iter,epsilon)

def get_init_kmeanspp(data_points, num_clusters):
    np.random.seed(0)
    centers = []
    centers_i = []
    for i in range(num_clusters):
        if i==0:
            index_choice = np.random.choice(len(data_points))
        else:
            index_choice = np.random.choice(len(data_points),p=probability)
        centers_i.append(index_choice)
        centers.append(data_points[index_choice])
        min_dist_arr = get_min_dist(np.array(centers),data_points)
        probability = min_dist_arr/np.sum(min_dist_arr)
    return np.array(centers,dtype=np.float64), centers_i

def get_min_dist(centers,data_points):
    return np.array([np.min(np.sqrt(np.sum((centers-data_points[i])**2,axis=1)),axis=0) for i in range(len(data_points))])

def load_data_points(db_file_1,db_file_2):
    df1 = pd.read_csv(db_file_1,header=None)
    df2 = pd.read_csv(db_file_2,header=None)
    df1 = pd.merge(df1,df2,how="inner",left_on=0,right_on=0)
    df1 = df1.sort_values(by=[0],ascending=True)
    df1 = pd.DataFrame(df1.drop(df1.columns[0],axis=1))
    data_points = df1.to_numpy(dtype=np.float64)
    return data_points

def kmeans(k,data_points,init_means,n_iterations,epsilon):
    k_means = init_means
    for _ in range(n_iterations):
        clusters=[[] for i in range(k)]
        for x in data_points:
            dist = distances_sqr_to_kmeans(k_means,x)
            clusters[np.argmin(dist)].append(x)

        new_k_means = np.array([calc_mean(np.array(cluster)) for cluster in clusters])
        max_delta_sqr=max(np.sum((k_means-new_k_means)**2,axis=1))
        k_means=new_k_means
        if max_delta_sqr < (epsilon**2):
            break
    return k_means
def distances_sqr_to_kmeans(k_means,point):
    return np.sum((k_means-point)**2,axis=1)
def calc_mean(iter_points):
    return iter_points.mean(axis=0)
#### End of Refrence Kmeans++ ####

def create_mem_test_file(file_name,iterations):
    file_contents=""
    with open("kmeans_pp.py") as f:
        file_contents = f.read()
    file_contents.replace("\r","")
    file_contents = file_contents.replace("\tprint(","\tpass#")
    file_contents = file_contents.replace("\nprint(","\npass#")
    file_contents = file_contents.replace(" print("," pass#")

    for line in file_contents.split("\n"):
        if "mykmeanssp.fit" in line:
            l = line[line.find("mykmeanssp.fit"):]
            white_space = line[:len(line)-len(line.lstrip())]
            inject=    f"""
{white_space}global args_fit
{white_space}global start_mem
{white_space}start_mem = current_process.memory_info().rss
{white_space}for child in current_process.children(recursive=True):
{white_space}   start_mem += child.memory_info().rss
{white_space}args_fit = """
            file_contents = file_contents.replace(line,white_space+l.replace("mykmeanssp.fit",inject)+"\n"+line)


    file_contents =    """
import psutil
import os
args_fit = tuple()
current_process = psutil.Process(os.getpid())
start_mem = current_process.memory_info().rss
""" + file_contents+f"""
for i in range({iterations}):
    mykmeanssp.fit(*args_fit)
end_mem = current_process.memory_info().rss
for child in current_process.children(recursive=True):
    end_mem += child.memory_info().rss
print(end_mem/start_mem)
"""

    with open(file_name,"w") as f:
        f.write(file_contents)
if __name__=="__main__":
    main()