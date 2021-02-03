JUDGE_LANG_C = 1 # C
JUDGE_LANG_CPP = 2 # C++
JUDGE_LANG_PYTHON = 3 # Python/PyPy
JUDGE_LANG_RUST = 4 # Rust
JUDGE_LANG_JS = 5 # Node.js
JUDGE_LANG_GO = 6 # Golang
JUDGE_LANG_JAVA = 7 # Java
JUDGE_LANG_RUBY = 8 # Ruby
JUDGE_LANG_PASCAL = 9 # Pascal
JUDGE_LANG_SUBMIT_ANSWER = 10 # For submit answer problem

DEFAULT_LANG_INFO = {
    JUDGE_LANG_C: '89,clang,O0', # standard, compiler, optimize level
    JUDGE_LANG_CPP: '17,clang,O0', # standard, compiler, optimize level
    JUDGE_LANG_PYTHON: 'python,36', # runner, version
    JUDGE_LANG_JAVA: 'java', # frontend
    JUDGE_LANG_PASCAL: 'O2', # optimize level
    JUDGE_LANG_SUBMIT_ANSWER: 'sha256', # hash algorithm
    JUDGE_LANG_RUST: '',
    JUDGE_LANG_JS: '',
    JUDGE_LANG_GO: '',
    JUDGE_LANG_RUBY: '',
}