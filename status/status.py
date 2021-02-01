JudgeStatus = {
    'WAITING': 0,    # waiting
    'COMPILING': 1,  # compiling
    'JUDGING': 2,    # judging
    'INPROCESS': 3,  # doing (but the judger did not return judging or compiling yet)
    'AC': 10,        # Answer Correct
    'PC': 11,        # Partly Correct
    'TLE': 12,       # Time Limit Exceed
    'MLE': 13,       # Memory Limit Exceed
    'RE': 14,        # Runtime Error
    'WA': 15,        # Wrong Answer
    'UKE': 16,       # Unknown Error
    'CE': 17,        # Compile Error
    'OLE': 18,       # Output Limit Exceed
    'SE': 20,        # System Error
    'FE': 21,        # File Error
    'JCE': 22,       # Judge Configuration Error
    'JRLE': 23,      # Judger Resource Limit Exceed
    'SLU': 24,       # Unsupported Language
}