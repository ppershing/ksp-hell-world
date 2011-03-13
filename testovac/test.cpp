#include "testovac.h"
#include <stdio.h>

int main() {
    Testovac::initialize(".");
    CompileSettings compile_settings;
    TestSettings test_settings;
    vector<string> program;
    vector<string> output;
    vector<string> compile_output;
    vector<string> input;
    vector<string> tasklist;

    tasklist = Testovac::get_task_list();
    printf("Mozes submitovat nasledujuce ulohy:\n");
    for (int i=0; i<(int)tasklist.size(); i++) {
        printf("%s\n", tasklist[i].c_str());
    }

    vector<string> desc;
    desc = Testovac::get_task_description("01_zero");
    printf("zadanie ulohy:\n");
    for (int i=0; i<(int)desc.size(); i++) {
        printf("%s\n", desc[i].c_str());
    }
    printf("\n");

    compile_settings.compiler = CompileSettings::COMPILER_CPP;
    compile_settings.compile_with_warnings = 0;

    test_settings.memory_limit = 1000;
    test_settings.time_limit = 1000;
    test_settings.full_test_log = 1;

    program.push_back("#include <stdio.h>");
    program.push_back("int main() {");
    program.push_back(" int nepouzivana;");
    program.push_back(" int a,b;");
    program.push_back(" scanf(\"%d %d\", &a,&b);");
    program.push_back(" printf(\"x%d\\n\", a+b);");
    program.push_back("}");
/*    program.push_back("var nepouzivana,cislo: integer;");
    program.push_back("begin");    
    program.push_back("writeln('zadaj cislo:');");
    program.push_back("readln(cislo);");
    program.push_back("writeln('Hello world!', cislo);");
    program.push_back("end.");*/


    int retval = Testovac::submit_solution("01_zero", program,
            compile_settings,test_settings,
            &compile_output, &output);

    printf("Testing returned value %d\n", retval);
    printf("Data from compilation:\n");
    for (int i=0; i<(int)compile_output.size(); i++) {
        printf("%s\n", compile_output[i].c_str());
    }
    printf("\n");
    printf("Data from log:\n");
    for (int i=0; i<(int)output.size(); i++) {
        printf("%s\n", output[i].c_str());
    }
}
