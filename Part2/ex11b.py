def calc(num1,operation,num2):
    if operation=="+":
        return num1+num2
    elif operation=="-":
        return num1-num2
    elif operation=="*":
        return num1*num2
    elif operation=="/":
        return num1/num2
    else:
        return "Invalid operation"
    
num1=12
num2=23

print(calc(num1, "+", num2))
print(calc(num1, "-", num2))
print(calc(num1, "*", num2))
print(calc(num1, "/", num2))