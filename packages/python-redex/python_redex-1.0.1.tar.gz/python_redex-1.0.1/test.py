import redex as rd

rd.info()

string = """

The names John Doe for males, Jane Doe or Jane Roe for females, or Jonnie Doe and Janie Joe for children, or just Doe non-gender-specifically are used as placeholder names for a party whose true identity is unknown or must be withheld in a legal action, case, or discussion. The names are also used to refer to acorpse or hospital patient whose identity is unknown. This practice is widely used in the United States and Canada, but is rarely used in other English-speaking countries including the United Kingdom itself, from where the use of John Doe in a legal context originates. mail123@email.com mailmain.com.
""".replace('\n','')

print(rd.find('startswith:*upper and contains:-', string))
print(rd.find('(location:{o,1} or location:{a,1}) and proximity:{*upper,n}3', string))
print(rd.find('count:{*upper,2}', string, granularity=2))
print(rd.find('sequence:{*alpha,*num,@,.com}', string))

rd.wildcard['*country'] = ['United States','Canada','United Kingdom']

print(rd.find('contains:*country', string, split=['.']))