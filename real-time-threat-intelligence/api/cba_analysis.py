# cba_analysis.py

def calculate_cba(ale_prior, ale_post, acs):
    """
    Calculate Cost-Benefit Analysis (CBA)
    CBA = ALE_prior - ALE_post - ACS
    """
    return ale_prior - ale_post - acs


#Example with values
ale_prior = 50000    # Annual loss expected before security control
ale_post = 10000     # Annual loss expected after security control
acs = 15000          # Annual cost of the control

cba_result = calculate_cba(ale_prior, ale_post, acs) # calls function & calculates

print(f" ALE Before: ${ale_prior}")
print(f" ALE After: ${ale_post}")
print(f" Annual Cost of Security (ACS): ${acs}")
print(f" Cost-Benefit Analysis Result: ${cba_result}")

if cba_result > 0:
    print(" This security implementation is cost-effective.")
elif cba_result < 0:
    print(" This security implementation might cost more than it saves.")
else:
    print(" This security implementation is equal. It remains even.")


'''
ALE_prior = how much money the organization would lose each year without any saftey/protection
ALE_post = how much money you would lose each year after implementing a control
ACS = the cost of security control itself ,each year
The output should show the net value gain or loss of using that control.

This file should let us calculate if you implement a security control will save more money than it will cost
Note: this was from week 6, task 3
'''