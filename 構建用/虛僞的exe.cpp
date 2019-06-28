#include <iostream>
#include <fstream>
#include <string>
using namespace std;
int main(int argc, char *argv[]) {
    string s = string(argv[0]);
    string ss = s.substr(s.rfind('\\') + 1, s.rfind('.') - s.rfind('\\') - 1);

    cout << s << endl;
    cout << "<" << ss << ">" << endl;

    ifstream t("_" + ss + ".kuzu");
    std::string q((std::istreambuf_iterator<char>(t)),
        std::istreambuf_iterator<char>());

    system(q.c_str());
}
