#include <vector>
#include <string>
using namespace std;

class CompileSettings {
public:
    static const int COMPILER_CPP=1;
    static const int COMPILER_PAS=2;
    int compiler;
    int compile_with_warnings;
};

class TestSettings {
public:
    int memory_limit; // in kB
    int time_limit; // in msec
    int full_test_log; // if enabled, in the diffs will appear in test log
};

class Testovac {
private:
    // {{{
    static void clean_sandbox();
    static void copy_wrapper();
    static void copy_test_data(const char* taskname);
    static void write_to_file(const char * filename, vector<string>& lines);
    static void read_from_file(const char * filename, vector<string> *lines);
    static int initialized;
    static string testdir;
    static string get_sandbox_dir();
    static string get_wrapper_dir();
    static string get_program_bin();
    static string get_backup_dir();
    static string get_tasks_dir();
    static string get_program_source(string ext);
    static string inttostr(int i);
    static void backup_sandbox();
    // }}}
public:
    /* you must initialize library before any other call,
       @testdir is path to directory, where Testovac is rooted
       */
    static void initialize(const char* testdir);

    /* returns task description
       @taskname - name of task directory, like "sucet", "fibonacci", ...
       @returns - line by line content od "desc" file within task directory
       */
    static vector<string> get_task_description(const char* taskname);

    /* try to compile a program
        @program - line by line listing of program
        @compile_settings - set program language, level of compiler
            warnings
        @output - line by line output of compiler
        @returns - 0 on success, nonzero otherwise
    */
    static int compile(vector<string>& program,
            CompileSettings& settings,
            vector<string> *output);

    /* tests solution of input given by contestant
        @program - line by line listing of program
        @input - line by line listing of input on which program
            should be tested
        @compile_settings - see submit_solution()
        @test_setting - see submit_solution()
        @compile_output - see submit_solution()
        @test_output - line by line output of program running on input data
        @returns - 0 on succes, nonzero value otherwise
        */
    static int test_on_input(vector<string>& program,
            vector<string>& input,
            CompileSettings& compile_settings,
            TestSettings& test_setting,
            vector<string> *compile_output,
            vector<string> *test_output);

    /* tests solution on all prepared input/output data
        @taskname - name of task directory, like "sucet", "fibonacci", ...
        @program - line by line listing of program to be submitted
        @compile_settings - set program compile settings (language, warning
            levels)
        @test_settings - set memory and time limit
        @compile_output - will be filled with line by line output of compiler
        @test_log - will be filled with line by line output of tester
        @returns - 0 on success, nonzero value otherwise
        */
    static int submit_solution(const char* taskname,
            vector<string>& program,
            CompileSettings& compile_settings,
            TestSettings& test_settings,
            vector<string> *compile_output,
            vector<string> *test_log);

    static vector<string> get_task_list();
};
