import json
import sys

def parseResultFile(outputFile):
    handler = open(outputFile, "r")
    content = handler.readlines()
    handler.close()
    
    result_dict = {}
    
    for item in content:
        items = item.split(",")
        number = int(items[0])
        temp_dict = {}
        for i in range(1, len(items), 2):
            car = items[i]
            objnumber = int(items[i+1])
            temp_dict[car] = objnumber
        result_dict[number] = temp_dict
    
    return result_dict
    
def validate_solution(outputResult, expectedResult):
    output_result = parseResultFile(outputResult)
    expected_result = parseResultFile(expectedResult)
    
    errors = {}
    
    for i in range(0, len(output_result)):
        ioutput = output_result[i]
        iexpected = expected_result[i]
        #if ioutput != iexpected:
            #print(ioutput, iexpected)
            
        false_positive = 0
        false_negative = 0
        
        true_positive = 0
        true_negative = 0
        incorrect_number_of_objects = 0
        
        for item in ioutput:
            if item not in iexpected:
                false_positive += 1
            else:
                true_positive += 1
                incorrect_number_of_objects += abs(ioutput[item] - iexpected[item])
        
        for item in iexpected:
            if item not in ioutput:
                false_negative += 1
            else:
                true_negative += 1

        if false_negative != 0:
            false_negative = false_negative / len(iexpected)
            #print(false_negative, len(iexpected))
        
        if false_positive != 0:
            false_positive = false_positive / len(ioutput)
            #print(false_positive, len(ioutput))
        
        accuracy = (true_positive + true_negative) / (true_positive + true_negative + false_negative + false_positive)
        
        #if incorrect_number_of_objects:
            #print(false_negative, false_positive)
            
        errors[i] = {'fp':false_positive, 'fn': false_negative, 'diff_objects':incorrect_number_of_objects, 'acc':accuracy}
    
    handler = open("resultFile", "w")
    json.dump(errors, handler, indent=4)
    handler.close()

validate_solution(sys.argv[1], sys.argv[2])
