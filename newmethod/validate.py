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
    
    general_accuracy = 0
    general_precision = 0
    general_recall = 0
    
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

        accuracy = (true_positive + true_negative) / (true_positive + true_negative + false_negative + false_positive)

        precision = true_positive / (true_positive + false_positive)
        recall = true_positive / (true_positive + false_negative)

        false_negative_procent = 0

        if false_negative != 0:
            false_negative_procent = round(false_negative / len(iexpected), 2)
            #print(false_negative, len(iexpected))
        
        false_positive_procent = 0
        
        if false_positive != 0:
            false_positive_procent = round(false_positive / len(ioutput),  2)
            #print(false_positive, len(ioutput))
        
        
        
        #if incorrect_number_of_objects:
            #print(false_negative, false_positive)
            
            
        general_accuracy += accuracy
        general_precision += precision
        general_recall += recall
        
        errors[i] = {'fp_count':false_positive, 'fp':false_positive_procent, 'fn_count': false_negative, 'fn': false_negative_procent,'diff_objects':incorrect_number_of_objects, 'acc':accuracy, 'precision':precision, 'recall':recall}
    
    general_accuracy /= len(output_result)
    general_precision /= len(output_result)
    general_recall /= len(output_result)
    
    general_accuracy = round(general_accuracy, 2)
    general_precision = round(general_precision, 2)
    general_recall = round(general_recall, 2)
    
    print("Accuracy: {} Precision: {} Recall: {}".format(general_accuracy, general_precision, general_recall))
    
    errors["general_values"] = {'general_accuracy':general_accuracy, 'general_precision': general_precision, 'general_recall':general_recall}
    
    handler = open("detailed_resultFile", "w")
    json.dump(errors, handler, indent=4)
    handler.close()

validate_solution(sys.argv[1], sys.argv[2])    