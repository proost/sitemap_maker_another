def get_input():
    raw_input = input(">>>")
    parsed_input = _parser(raw_input)
    return parsed_input

def show_selection(selection_list):
    list_str = "--------input site--------\n"
    for selection in selection_list:
        list_str += selection +"\n"
    print(list_str)

def _parser(input_str):
    if 'y' in input_str.lower():
        return 'y'
    elif 'n' in input_str.lower():
        return 'n'
    else:
        return 'w'

def wrong_input():
    print('You typed wrong input')

def continue_question():
    print('Continue?[Y/N]')

def download_question():
    print('Download File [Y/N]')

        




        
        
            

