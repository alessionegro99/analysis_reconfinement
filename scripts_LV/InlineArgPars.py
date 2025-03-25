import sys
import itertools

class ParsingError(Exception):
    pass

class InlineArgPars:
    def __init__(self) -> None:
        self.count: int = 0
        self.maxused: int = 0

        first_opt = next(i for i, arg in enumerate(sys.argv + ['-']) if arg.startswith('-'))
        self.passed_argv = list(sys.argv[:first_opt])
        self.passed_argc = len(self.passed_argv)
        
        self.passed_optv = []
        for opt in list(sys.argv[first_opt:]):
            if opt[0] != '-' \
            or opt[1] == '-' \
            or len(opt) == 2:
                self.passed_optv.append(opt)
                continue
            
            # multiple options called by short 
            for o in opt[1:]:
                self.passed_optv.append(f'-{o}')

        self.first_error = 0

        self.passd_dict = dict()
        self.usage_dict = dict()
        self.inter_dict = dict()

        self.used_opt_names = ['help']
        self.used_opt_shorts = ['h']

    def parsing_error_occur(self, name: str, type: type, value: str):
        if self.first_error == 0 or self.first_error > self.count:
            self.first_error = self.count
            self.name_error = name
            self.type_error = type
            self.valu_error = value
        return type()

    def next_arg(self, name: str, type: type=str, default=None):

        if default is not None:
            name = f'{name}={default}'

        tp_n = type.__name__

        curr_usage = ' ' + name
        curr_interpr_str = ' ' + tp_n
        if len(name) < len(tp_n): curr_usage += ' ' * (len(tp_n) - len(name))
        else: curr_interpr_str += ' ' * (len(name) - len(tp_n))

        self.count += 1
        if self.count > self.maxused: self.maxused = self.count
        if self.count < self.passed_argc:
            
            curr_passed = self.passed_argv[self.count] + ' '
            if len(curr_usage) < len(curr_passed):
                white_space = ' ' * (len(curr_passed) - len(curr_usage))
                curr_usage += white_space
                curr_interpr_str += white_space
            else: curr_passed += ' ' * (len(curr_usage) - len(curr_passed))

            self.passd_dict[self.count] = curr_passed
            self.usage_dict[self.count] = curr_usage
            self.inter_dict[self.count] = curr_interpr_str

            try:
                return type(self.passed_argv[self.count])
            except ValueError:
                return self.parsing_error_occur(name, type, self.passed_argv[self.count])
        
        else:
            self.passd_dict[self.count] = ''
            self.usage_dict[self.count] = curr_usage
            self.inter_dict[self.count] = curr_interpr_str

            if default is None:
                return self.parsing_error_occur(name, type, None)
            return default
        
    def parse_arg(self, arg_num: int, name: str, type: type=str, default=None, update_count: bool=False):
        '''
        returns argv[arg_num] interpreted as type
        '''
        old_count = self.count
        self.count = arg_num - 1

        to_ret = self.next_arg(name, type, default)

        if not update_count: self.count = old_count
        return to_ret
            
    def build_usage_str(self, omit_argv=False):
        usage = 'usage: ' + self.passed_argv[0]
        interpr_str = 'interpreted as: '

        if len(usage) < len(interpr_str): usage += ' ' * (len(interpr_str) - len(usage))
        else: interpr_str = ' ' * (-len(interpr_str) + len(usage)) + interpr_str

        passed = ' ' * len(usage) + ' '

        for k in range(1, self.maxused+1):
            try:
                passed +=      self.passd_dict[k]
                usage +=       self.usage_dict[k]
                interpr_str += self.inter_dict[k]
            except KeyError:
                try:
                    curr_passed = self.passed_argv[k]
                except IndexError:
                    curr_passed = ''

                curr_usage = ' UNUSED'
                curr_interpr_str = ' ' * len(curr_usage)
                
                if len(curr_usage) < len(curr_passed):
                    white_space = ' ' * (len(curr_passed) - len(curr_usage))
                    curr_usage += white_space
                    curr_interpr_str += white_space
                else: curr_passed += ' ' * (len(curr_usage) - len(curr_passed))
                
                passed +=      curr_passed
                usage +=       curr_usage
                interpr_str += curr_interpr_str

        if omit_argv: return '\n'.join([usage, interpr_str, ''])

        if self.maxused < len(self.passed_argv):
            passed += ' '.join(self.passed_argv[self.maxused+1 :])

        return '\n'.join([passed, usage, interpr_str, ''])
    
    def look_for_option(self, name: str, short: str = None):
        
        if name in self.used_opt_names: raise ValueError(f'Name --{name} used more than onece for options')

        self.used_opt_names.append(name)

        if '--' + name in self.passed_optv:
            self.passed_optv.remove('--' + name)
            return True

        if short is not None:
            if short in self.used_opt_shorts: raise ValueError(f'Short -{short} used more than onece for options')
            self.used_opt_shorts.append(short)

            if '-' + short in self.passed_optv:
                self.passed_optv.remove('-' + short)
                return True

        return False

    def checkout(self):
        
        if '-h' in self.passed_optv or '--help' in self.passed_optv:
            print(self.build_usage_str(True))
            raise ParsingError('Helper was requested')

        current_error = self.first_error
        current_maxused = self.maxused

        current_usage = self.build_usage_str()

        # init again for further try
        self.count = 0
        self.maxused = 0
        self.first_error = 0

        self.passd_dict.clear()
        self.usage_dict.clear()
        self.inter_dict.clear()

        if current_error != 0:
            print(current_usage)

            if self.valu_error is None: # error caused by missing argument
                raise ParsingError(f'Argument {current_error} ({self.name_error}) is not specified and has no default')
            
            # error caused by misinterpreted argument
            raise ParsingError(f'Argument {current_error} ({self.name_error}) "{self.valu_error}" cannot be interpreted as {self.type_error}')
        
        if current_maxused < self.passed_argc - 1:
            print(current_usage)
            raise ParsingError(f'{self.passed_argc - 1} arguments were passed, but only {current_maxused} were read')
        
        if len(self.passed_optv) > 0:
            raise ParsingError(f'Unrecognised option {self.passed_optv[0]}')
        
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.checkout()

if __name__ == '__main__':
    # parser = InlineArgPars()

    with InlineArgPars() as parser:
        z_befor = parser.parse_arg(3, 'z_v', float)
        x = parser.next_arg('x_val', float)
        y = parser.next_arg('y_val', int)
        z = parser.next_arg('z_v', float)
        n = parser.next_arg('n_num', int)
        s = parser.next_arg('string', default='cosa')

        take_root = parser.look_for_option('take_root', 'r')
        useless_opt = parser.look_for_option('useless', 'u')

    if take_root: exponent = 1. / n
    else:         exponent = 1.
    print(s, '=', (x**n + y**n + z**n)**exponent)

    # try:
    #     parser.checkout()
    #     if take_root: exponent = 1. / n
    #     else:         exponent = 1.
    #     print(s, '=', (x**n + y**n + z**n)**exponent)

    # except ParsingError as err:
    #     print('catched:', err)
    #     print('second try at parsing')

    #     n_again = parser.parse_arg(4, 'n_num', int, default=2, update_count=True)
    #     s_again = parser.next_arg('string', default='cosa')
    #     y_again = parser.parse_arg(2, 'y_val', int)
    #     x_again = parser.parse_arg(1, 'x_val', float, update_count=True)

    #     parser.checkout()

    #     print(x_again, y_again, z_befor, n_again, s_again)
