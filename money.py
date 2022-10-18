from math import floor 

# Έστω μισθός 23800 μικτά ΕΤΗΣΙΑ έσοδα.
# - ασφαλιστικές εισφορές = 23800*13.867% = 3300.346
# - φορολογητέο εισόδημα = 23800 - 3300.346 =  20499.654
# - φόρος εισοδήματος = 10000*9% + 10000*22% + 499.654*28% = 3239.90312
# - έκπτωση φόρου = 777−20×floor((20499.654−12000)÷1000) = 617
# - καθαρό εισόδημα = 20499.654 − 3239.90312 + 617 = 17876.75088
# Οι ασφαλιστικές κατηγορίες για ελεύθερους επαγγελματίες είναι: 210 252 302 363 435 566 ευρώ ανά μήνα

EFKA = 13.867
INSURANCE_CATEGORIES = [210, 252, 302, 363, 435, 566]
OAEE_PENSION_CATEGORIES = [791, 892, 1003, 1163, 1353, 1697]
INCOME_TAX_CATEGORIES = {
    10000: 9, 
    20000: 22, 
    30000: 28,
    40000: 36,
    1000000: 44
}
MAX_NATIONAL_PENSION = 384
MAX_CONTRIBUTORY_PENSION_FACTOR = 56.7 # after 45 years of work

category = int(input('1. Υπάλληλος\n2. Ελεύθερος επαγγελματίας\n3. Εταιρία\nΔιάλεξε: '))
beforeTaxIncome = int(input('Μεικτά έσοδα: '))

# taxable income and pension before tax
if category == 1:
    insuranceContributions = min(beforeTaxIncome, 91000) * EFKA / 100 # 91000 = 6500 * 14 months
    beforeTaxPension = MAX_NATIONAL_PENSION * 12 + beforeTaxIncome * MAX_CONTRIBUTORY_PENSION_FACTOR / 100
elif category == 2 or category == 3:
    INSURANCE_CATEGORIES = [item * 12 for item in INSURANCE_CATEGORIES]
    expectedContributions = min(beforeTaxIncome, 91000) * EFKA / 100
    distances = [abs(expectedContributions-i*12) for i in INSURANCE_CATEGORIES]
    min_index = distances.index(min(distances))
    insuranceContributions = INSURANCE_CATEGORIES[min_index]
    beforeTaxPension = OAEE_PENSION_CATEGORIES[min_index] * 12

taxableIncome = beforeTaxIncome - insuranceContributions

# Income Tax
def income_tax_calc(income):
    incomeTax = 0
    Low = 0
    for High, Factor in INCOME_TAX_CATEGORIES.items():
        if (income < High): 
            incomeTax += (income - Low) * Factor / 100
            break

        incomeTax += (High - Low) * Factor / 100
        Low = High
    return incomeTax
incomeTax = income_tax_calc(taxableIncome)
pensionTax = income_tax_calc(beforeTaxPension)

# Tax Deduction
if category == 1:
    incomeTaxDeduction = max(0, 777 - 20 * floor((taxableIncome - 12000) / 1000))
    pensionTaxDeduction = max(0, 777 - 20 * floor((beforeTaxPension - 12000) / 1000))
elif category == 2 or category == 3:
    incomeTaxDeduction = 0
    pensionTaxDeduction = 0

# After-tax income
afterTaxIncome = taxableIncome - incomeTax + incomeTaxDeduction
afterTaxPension = beforeTaxPension - pensionTax + pensionTaxDeduction

print('\nΦορολογητέο εισόδημα =',taxableIncome)
print('Φόρος εισοδήματος =',incomeTax)
print('Έκπτωση φόρου =',incomeTaxDeduction)
print('Καθαρό εισόδημα =',afterTaxIncome)
print('\nΣύνταξη =',beforeTaxPension)
print('Φόρος εισοδήματος  =',pensionTax)
print('Έκπτωση φόρου =',pensionTaxDeduction)
print('Καθαρό εισόδημα =',afterTaxPension)