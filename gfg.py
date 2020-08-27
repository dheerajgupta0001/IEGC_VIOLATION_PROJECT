# Python3 code to demonstrate  
# to delete dictionary in list 
# using del + loop  
  
# initializing list of dictionaries 
test_list = [{"id" : 1, "data" : "HappY"}, 
             {"id" : 2, "data" : "BirthDaY"}, 
             {"id" : 3, "data" : "Rash"}] 
  
# printing original list  
print ("The original list is : " + str(test_list)) 
  
# using del + loop  
# to delete dictionary in list 
for i in range(len(test_list)): 
    if test_list[i]['id'] == 2: 
        del test_list[i] 
print ("The original list is : " + str(test_list)) 