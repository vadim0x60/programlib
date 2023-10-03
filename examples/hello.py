from programlib import Program

hw = """
#include <vector>
#include <iostream>
#include <string>
#include <cstring>
#include <queue>
#include <stdio.h>
#include <math.h>
#include <map>
#include <set>
#include <stack>
#include <climits>
using namespace std;
/*
A program that outputs "Hello World"
For example,
input:

output:
Hello World
*/
int main() {
    cout << "Hello World!" << endl;
    return 0;
}
"""

program = Program(hw, language='C++')
tests = program.test([
    ([], ['Hello World!'])
])

print(tests)