JUDGE_STATUS_WAITING = 0  # waiting
JUDGE_STATUS_COMPILING = 1  # compiling
JUDGE_STATUS_JUDGING = 2  # judging
JUDGE_STATUS_INPROCESS = 3 # doing (but the judger did not return judging or compiling yet)
JUDGE_STATUS_AC = 10  # Answer Correct
JUDGE_STATUS_PC = 11  # Partly Correct
JUDGE_STATUS_TLE = 12  # Time Limit Exceed
JUDGE_STATUS_MLE = 13  # Memory Limit Exceed
JUDGE_STATUS_RE = 14  # Runtime Error
JUDGE_STATUS_WA = 15  # Wrong Answer
JUDGE_STATUS_UKE = 16  # Unknown Error
JUDGE_STATUS_CE = 17  # Compile Error
JUDGE_STATUS_OLE = 18 # Output Limit Exceed
JUDGE_STATUS_SE = 20  # System Error
JUDGE_STATUS_FE = 21  # File Error
JUDGE_STATUS_CFGE = 22  # Configuration Error
JUDGE_STATUS_JRLE = 23  # Judger Resource Limit Exceed
JUDGE_STATUS_UL = 24  # Unsupported Language