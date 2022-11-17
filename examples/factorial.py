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
program = Program(source=factorial_cpp, language='C++')
program.test(factorial_tests)
print(program.avg_score)

factorial_clj = """
(defn factorial [n] (if (< n 1) 1 (* n (factorial (- n 1)))))
(-> (read-line) (read-string) (factorial) (println))
"""

print('Clojure score')
program = Program(source=factorial_clj, language='Clojure')
program.test(factorial_tests)
print(program.avg_score)
