#!/usr/bin/env python
# coding: utf-8

# In[58]:


import random

LINE ="""{Existing_account} {Duration_month} {Credit_history} {Purpose} {Credit_amount} {Saving} {Employment_duration} {Installment_rate} {Personal_status} {Debtors} {Residential_Duration} {Property} {Age} {Installment_plans} {Housing} {Number_of_credits} {Job} {Liable_People} {Telephone} {Foreign_worker}"""
def generate_log():
    existing_account = [0,1,2,3]
    Existing_account = random.choice(existing_account)
    
    duration_month = []
    for i  in range(6, 90 , 3):
        duration_month.append(i)
    Duration_month = random.choice(duration_month)
    
    credit_history = [0,1,2,3,4]
    Credit_history = random.choice(credit_history)
    
    purpose = [ 0,1,2,3,4,5,6,7,8,9]
    Purpose = random.choice(purpose)
    
    credit_amount = []
    for i in range(0 ,20000):
        credit_amount.append(i)
    Credit_amount = random.choice(credit_amount)
    
    saving = [0,1,2,3,4]
    Saving = random.choice(saving)
    
    employment_duration = [0,1,2,3,4]
    Employment_duration = random.choice(employment_duration)
    
    installment_rate = [1,2,3,4]
    Installment_rate = random.choice(installment_rate)
    
    personal_status = [0,1,2,3]
    Personal_status = random.choice(personal_status)
    
    debtors = [0,1,2]
    Debtors = random.choice(debtors)
    
    residential_Duration = [1,2,3,4]
    Residential_Duration = random.choice(residential_Duration)
    
    Proprty = [0,1,2,3,4,5,6,8,9]
    Property = random.choice(Proprty)
    
    age = []
    for i in range(20 , 60):
        age.append(i)
    Age = random.choice(age)
    
    installment_plans = [0,1,2]
    Installment_plans = random.choice(installment_plans)
    
    housing = [0,1,2]
    Housing = random.choice(housing)
    
    number_of_credits = []
    for i in range(1,3):
        number_of_credits.append(i)
    Number_of_credits = random.choice(number_of_credits)
    
    job = [0,1,2,3]
    Job = random.choice(job)
    
    liable_People = [1,2]
    Liable_People = random.choice(liable_People)
    
    telephone = [0,1]
    Telephone = random.choice(telephone)
    
    foreign_worker = [0,1]
    Foreign_worker = random.choice(foreign_worker)
    
    log_line = LINE.format(
        Existing_account=Existing_account,
        Duration_month=Duration_month,
        Credit_history=Credit_history,
        Purpose=Purpose,
        Credit_amount=Credit_amount,
        Saving=Saving,
        Employment_duration=Employment_duration,
        Installment_rate=Installment_rate,
        Personal_status=Personal_status,
        Debtors=Debtors,
        Residential_Duration=Residential_Duration,
        Property=Property,
        Age=Age,
        Installment_plans=Installment_plans,
        Housing=Housing,
        Number_of_credits = Number_of_credits,
        Job= Job,
        Liable_People=Liable_People,
        Telephone=Telephone,
        Foreign_worker=Foreign_worker
    )

    return log_line
if __name__ == '__main__':
    while True:
        line = generate_log()
        print(line)
