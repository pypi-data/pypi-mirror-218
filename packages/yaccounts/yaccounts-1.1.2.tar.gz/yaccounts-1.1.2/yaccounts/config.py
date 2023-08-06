CODES_STUDENT_WAGES = (
    5510,
    5599,
    5610,
    5720,
    5812,
    5572,
    5570,
    5672,
    5600,
    5750,
    8905,
)

# These student benefits aren't attached to an individual student
# name, so they must be separated out
CODES_STUDENT_BENEFITS = (5670, 5699, 5950, 5960, 5970, 5999)

CODES_STUDENT_TUITION = (6300, 6303, 6304, 6309, 6319, 6390)
CODES_FACULTY_SPRING_SUMMER = (5920, 5260, 5220)
CODES_TRAVEL = (6190, 7000, 7010, 7030, 7050, 7060, 7070, 7080)
CODES_SUPPLIES = (
    2200,
    5980,
    6000,
    6005,
    6100,
    6109,
    6110,
    6120,
    6125,
    6130,
    6140,
    6160,
    6180,
    6185,
    6192,
    6200,
    6210,
    6220,
    6250,
    6255,
    6270,
    6403,
    6405,
    6600,
    6610,
    6480,
    6490,
    6499,
    8940,
)
CODES_CAPITAL = (1625, 1725, 8930, 9126, 9127, 9136, 9137)
CODES_OVERHEAD = (8990, 8991)

CODES_INTEREST = (4711,)

# Income only applies to non-budgeted accounts
CODES_INCOME = (9250, 9260, 3500)

# Non-budgeted accounts, don't normally use BUDGET lines and they
# can be removed, except for these codes
CODES_NON_BUDGETED_BUDGET_CODES = (10,)

# These codes aren't used by anything and can be removed from the data
CODES_IGNORED = (1010, 1235, 2000, 2210, 4220, 4200)

COL_NAME_AMOUNT = "JRNL Monetary Amount -no scrn aggregation"

COLOR_STUDENT_WAGES = "rosybrown"
COLOR_STUDENT_BENEFITS = "moccasin"
COLOR_STUDENT_TUITION = "moccasin"
COLOR_FACULTY = "lightskyblue"
COLOR_TRAVEL = "plum"
COLOR_SUPPLIES = "khaki"
COLOR_CAPITAL = "khaki"
COLOR_OVERHEAD = "silver"
COLOR_TOTAL_EXPENSES = "tomato"
COLOR_TOTAL_INCOME = "limegreen"


def all_expense_codes():
    return (
        CODES_STUDENT_WAGES
        + CODES_STUDENT_BENEFITS
        + CODES_STUDENT_TUITION
        + CODES_FACULTY_SPRING_SUMMER
        + CODES_TRAVEL
        + CODES_SUPPLIES
        + CODES_OVERHEAD
        + CODES_CAPITAL
    )


def all_handled_codes():
    return all_expense_codes() + CODES_INTEREST + CODES_IGNORED + CODES_INCOME
