# From R2 to R6 of the Japanese income tax table

# 丸め誤差処理
def floor_to_4000(yen: int) -> int:
    """4,000円刻みの切り捨て（整数演算のみでより安全）"""
    return (yen // 4_000) * 4_000

# 給与所得控除の計算 (丸め誤差対策済み)
def calc_salary_deduction(salary:int) -> int:
    """
    給与所得控除額（令和2年から6年までの計算方法）
    ・6,600,000円未満は「給与/4→千円未満切捨て→×4」を入れてから区分式に当てる
    ・6,600,000円以上は1円未満切捨て（整数演算で自然に満たす）
    出典：https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1410.htm
    """
    if salary <= 1625000:
        return max(0, salary - 550000)
    elif salary <= 1800000:
        return salary * 0.4 - 100000
    elif salary <= 3600000:
        salary_r4 = floor_to_4000(salary)
        return salary_r4 * 0.3 + 80000
    elif salary <= 6600000:
        salary_r4 = floor_to_4000(salary)
        return salary_r4 * 0.2 + 440000
    elif salary <= 8500000:
        return salary * 0.1 + 1100000
    else:# max salary deduction
        return 1950000 

# 課税される所得金額に対する所得税の税率速算表
# (min, max, tax_rate, tax_deduction)を格納
brackets = [
    (0,        1949000, 0.05, 0),
    (1950000,  3299000, 0.10, 97500),
    (3300000,  6949000, 0.20, 427500),
    (6950000,  8999000, 0.23, 636000),
    (9000000, 17999900, 0.33, 1536000),
    (18000000,39999900, 0.40, 2796000),
    (40000000,float('inf'),0.45,4796000),
]

def determine_tax_rate(taxable):
    for lb, ub, tax_rate, tax_deduction in brackets:
        if lb <= taxable <= ub:
            return tax_rate, tax_deduction
    return None, None

def format_num(n: int) -> str:
    #数値nをカンマ区切りにするために、3桁ごとにカンマを挿入した文字列に変換
    return f"{n:,}"
