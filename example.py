from math import factorial
from programlib import Program

factorial_tests = [
    (['6'], ['720']),
    (['5'], ['120']),
    (['4'], ['24']),
    (['8'], ['40320'])
]

factorial_cpp = """
using namespace std;
#include <iostream>

int main() {

    int n;
    cin >> n;
    int fact = 1;
    for (int i = 1; i <= n; i++) {
        fact *= i;
    }
    cout << fact << endl;
    return 0;
}

"""

print('C++ score')
print(Program(source=factorial_cpp, language='C++').score(factorial_tests))

factorial_clj = """
(defn factorial [n] (if (< n 1) 1 (* n (factorial (- n 1)))))
(-> (read-line) (read-string) (factorial) (println))
"""

print('Clojure score')
print(Program(source=factorial_clj, language='Clojure').score(factorial_tests))