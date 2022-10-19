from math import floor 

# Έστω μισθός 23800 μικτά ΕΤΗΣΙΑ έσοδα.
# - ασφαλιστικές εισφορές = 23800*13.867% = 3300.346
# - φορολογητέο εισόδημα = 23800 - 3300.346 =  20499.654
# - φόρος εισοδήματος = 10000*9% + 10000*22% + 499.654*28% = 3239.90312
# - έκπτωση φόρου = 777−20×floor((20499.654−12000)÷1000) = 617
# - καθαρό εισόδημα = 20499.654 − 3239.90312 + 617 = 17876.75088
# Οι ασφαλιστικές κατηγορίες για ελεύθερους επαγγελματίες είναι: 210 252 302 363 435 566 ευρώ ανά μήνα

EFKA = 13.867
INCOME_TAX_CATEGORIES = {
    10000: 9, 
    20000: 22, 
    30000: 28,
    40000: 36,
    1000000: 44
}
INSURANCE_CATEGORIES = [210, 252, 302, 363, 435, 566]
MAX_NATIONAL_PENSION = 384
MAX_CONTRIBUTORY_PENSION_FACTOR_1 = 56.7 # after 45 years of work as an employee
MAX_CONTRIBUTORY_PENSION_FACTOR_2 = 52.51 # after 45 years of work as an employer!
GREEK_CATEGORIES = {
    'employee': 'ΥΠΑΛΛΗΛΟΣ', 
    'freelancer': 'ΕΛΕΥΘΕΡΟΣ ΕΠΑΓΓΕΛΜΑΤΙΑΣ', 
    'company': 'ΕΤΑΙΡΙΑ'
}

# taxable income and pension before tax
def insurance_calc(category, beforeTaxIncome):
    if category == 'employee':
        insuranceContributions = min(beforeTaxIncome, 91000) * EFKA / 100 # 91000 = 6500 * 14 months
        beforeTaxPension = MAX_NATIONAL_PENSION * 12 + beforeTaxIncome * MAX_CONTRIBUTORY_PENSION_FACTOR_1 / 100
    elif category == 'freelancer' or category == 'company':
        expectedContributions = min(beforeTaxIncome, 91000) * EFKA / 100
        distances = [abs(expectedContributions-i*12) for i in INSURANCE_CATEGORIES]
        min_index = distances.index(min(distances))
        insuranceContributions = INSURANCE_CATEGORIES[min_index] * 12
        beforeTaxPension = MAX_NATIONAL_PENSION * 12 + insuranceContributions / 0.2 * MAX_CONTRIBUTORY_PENSION_FACTOR_2 / 100
    taxableIncome = beforeTaxIncome - insuranceContributions
    return insuranceContributions, beforeTaxPension, taxableIncome

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

# Tax Deduction
def tax_detuction_calc(category, taxableIncome, beforeTaxPension):    
    if category == 'employee':
        incomeTaxDeduction = max(0, 777 - 20 * floor((taxableIncome - 12000) / 1000))
        pensionTaxDeduction = max(0, 777 - 20 * floor((beforeTaxPension - 12000) / 1000))
    elif category == 'freelancer' or category == 'company':
        incomeTaxDeduction = 0
        pensionTaxDeduction = max(0, 777 - 20 * floor((beforeTaxPension - 12000) / 1000))
    return incomeTaxDeduction, pensionTaxDeduction

def calculator(beforeTaxIncome, category):
    # insurance
    insuranceContributions, beforeTaxPension, taxableIncome = insurance_calc(category, beforeTaxIncome)

    # income tax
    if category == 'company':
        incomeTax = taxableIncome * 22 / 100
    else: 
        incomeTax = income_tax_calc(taxableIncome)
    pensionTax = income_tax_calc(beforeTaxPension)

    # tax detuction
    incomeTaxDeduction, pensionTaxDeduction = tax_detuction_calc(category, taxableIncome, beforeTaxPension)

    # After-tax income
    afterTaxIncome = taxableIncome - incomeTax + incomeTaxDeduction
    afterTaxPension = beforeTaxPension - pensionTax + pensionTaxDeduction

    return insuranceContributions, beforeTaxPension, taxableIncome, incomeTax, pensionTax, incomeTaxDeduction, afterTaxIncome, pensionTaxDeduction, afterTaxPension

def main():
    beforeTaxIncome = int(input('Μεικτά έσοδα: '))

    for category in ['employee','freelancer','company']:
        insuranceContributions, beforeTaxPension, taxableIncome, incomeTax, pensionTax, incomeTaxDeduction, afterTaxIncome, pensionTaxDeduction, afterTaxPension = calculator(beforeTaxIncome, category)
        print('\n---',GREEK_CATEGORIES[category])
        print('Καθαρό εισόδημα =',int(afterTaxIncome))
        print('Καθαρή σύνταξη =',int(afterTaxPension))
        print('-- Ανάλυση εισοδήματος')
        print('Ασφαλιστικές εισφορές =',int(insuranceContributions))
        print('Φορολογητέο εισόδημα =',int(taxableIncome))
        print('Φόρος εισοδήματος =',int(incomeTax))
        print('Έκπτωση φόρου =',int(incomeTaxDeduction))
        print('-- Ανάλυση σύνταξης')
        print('Φόρος εισοδήματος =',int(pensionTax))
        print('Έκπτωση φόρου =',int(pensionTaxDeduction))

if __name__ == "__main__":
    main()
