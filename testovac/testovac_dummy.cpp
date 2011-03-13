#include "testovac.h"
#include <cstdlib>
#include <fstream>
#include <cassert>
#include <time.h>

string Testovac::testdir;
int Testovac::initialized;

void Testovac::initialize(const char* testdir){
    Testovac::testdir = testdir;
    Testovac::initialized = 1;
    srand(time(NULL));
}

string Testovac::get_sandbox_dir(){
    return testdir+"/sandbox";
}

string Testovac::get_tasks_dir(){
    return testdir+"/tasks";
}

string Testovac::get_wrapper_dir(){
    return testdir;
}

string Testovac::get_program_bin(){
    return get_sandbox_dir()+"/program";
}

string Testovac::get_program_source(string ext){
    return get_program_bin()+"."+ext;
}

void Testovac::clean_sandbox() {
    assert(initialized);
}

void Testovac::copy_wrapper() {
    assert(initialized);
}

void Testovac::copy_test_data(const char* taskname) {
    assert(initialized);
}

int Testovac::compile(vector<string>& program,
            CompileSettings& settings,
            vector<string> *output) {
    // {{{
    string programName;
    int retval;

    assert(initialized);
    assert (settings.compiler == CompileSettings::COMPILER_CPP ||
            settings.compiler == CompileSettings::COMPILER_PAS);

    if (settings.compiler == CompileSettings::COMPILER_CPP) {
        programName = get_program_source("cpp");
    } else 
    if (settings.compiler == CompileSettings::COMPILER_PAS) {
        programName = get_program_source("pas");
    }

    output->push_back("compiling "+programName);
    if (settings.compile_with_warnings) {
        output->push_back("Showing warnings");
    }
    retval = rand()%4==0;
    if (retval) {
        output->push_back("the compile was unsuccesfull");
    } else {
        output->push_back("compilation OK");
    }
    return retval;
    // }}}
}

void Testovac::write_to_file(const char * filename, vector<string>& lines) {
}

void Testovac::read_from_file(const char * filename, vector<string> *lines) {
    lines->push_back("This is dummy tester, lines will be random");
    for (int i=0; i < 5; i++) {
        lines->push_back("line "+inttostr(i)+": "+inttostr(rand()));
    }
}

string Testovac::inttostr(int i){
    // {{{
    char tmp[100];
    sprintf(tmp,"%d",i);
    return string(tmp);
    // }}}
}

int Testovac::test_on_input(vector<string> &program,
        vector<string>& input,
        CompileSettings& compile_settings,
        TestSettings& test_settings,
        vector<string> *compile_output,
        vector<string> *test_output) {
    // {{{
    int compile_ret;
    compile_ret = Testovac::compile(program, compile_settings, compile_output);
    if (compile_ret) return compile_ret;

    test_output->push_back("Dummy test will be sucesfull if input");
    test_output->push_back("will have at least 5 lines");
    test_output->push_back("and now output:");
    int retval = input.size()>=5;;
    read_from_file("", test_output);
    return retval;
    // }}}
}

int Testovac::submit_solution(const char* taskname,
        vector<string> &program,
        CompileSettings& compile_settings,
        TestSettings& test_settings,
        vector<string> *compile_output,
        vector<string> *test_log) {
    // {{{
    int compile_ret;
    compile_ret = Testovac::compile(program, compile_settings, compile_output);
    if (compile_ret) return compile_ret;

    test_log->push_back("This is test log for task");
    test_log->push_back(taskname);
    test_log->push_back("Now I'm testing ... (this is complete log)");
    test_log->push_back("(please, show this log to contestant only");
    test_log->push_back(" if he have upgrade)");
    int retval=rand()%2;
    read_from_file("", test_log);
    if (retval) {
        test_log->push_back("WA/TLE/EXE");
    } else {
        test_log->push_back("all OK");
    }
    return retval;
    // }}}
}

vector<string> Testovac::get_task_description(const char* taskname) {
    // {{{
    vector<string> result;
    result.push_back("Task description for "+string(taskname));
    read_from_file("", &result);
    return result;
    // }}}
}

vector<string> Testovac::get_task_list() {
    vector<string> result;
    result.push_back("task1");
    result.push_back("task2");
    return result;
}
