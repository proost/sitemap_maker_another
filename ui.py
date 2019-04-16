from progress.bar import IncrementalBar

class ProgressBar():
    def __init__(self):
        self.bar = IncrementalBar("searching")
    
    def update(self,update_value):
        if self.bar.remaining > 1:
            self.bar.next(update_value)
        if update_value == 100:
            full = 100 - self.bar.remaining
            self.bar.next(full)

def get_input():
    raw_input = input(">>>")
    parsed_input = _parser(raw_input)
    return parsed_input

def show_selection(selection_list):
    """show site list in excel file to user"""
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

def done():
    """alarm to user finish job"""
    print('모든 과정이 끝났습니다. 파일을 확인해주세요.')

        




        
        
            

