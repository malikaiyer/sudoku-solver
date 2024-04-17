arr4x4 = [[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]]
#part 1: constraints for 4x4 sudoku
constraint4x4 = {
                ('C11', 'C12'): arr4x4,
                ('C11', 'C13'): arr4x4,
                ('C11', 'C14'): arr4x4,
                ('C11', 'C22'): arr4x4,
                ('C11', 'C21'): arr4x4,
                ('C11', 'C31'): arr4x4,
                ('C11', 'C41'): arr4x4,

                ('C12', 'C13'): arr4x4,
                ('C12', 'C14'): arr4x4,
                ('C12', 'C22'): arr4x4,
                ('C12', 'C21'): arr4x4,
                ('C12', 'C32'): arr4x4,
                ('C12', 'C42'): arr4x4,

                ('C13', 'C14'): arr4x4,
                ('C13', 'C23'): arr4x4,
                ('C13', 'C33'): arr4x4,
                ('C13', 'C43'): arr4x4,
                ('C13', 'C24'): arr4x4,

                ('C14', 'C24'): arr4x4,
                ('C14', 'C34'): arr4x4,
                ('C14', 'C44'): arr4x4,
                ('C14', 'C23'): arr4x4,

                ('C21', 'C22'): arr4x4,
                ('C21', 'C23'): arr4x4,
                ('C21', 'C24'): arr4x4,
                ('C21', 'C31'): arr4x4,
                ('C21', 'C41'): arr4x4,

                ('C22', 'C23'): arr4x4,
                ('C22', 'C24'): arr4x4,
                ('C22', 'C32'): arr4x4,
                ('C22', 'C42'): arr4x4,

                ('C23', 'C24'): arr4x4,
                ('C23', 'C33'): arr4x4,
                ('C23', 'C43'): arr4x4,

                ('C24', 'C34'): arr4x4,
                ('C24', 'C44'): arr4x4,
                    
                ('C31', 'C32'): arr4x4,
                ('C31', 'C33'): arr4x4,
                ('C31', 'C34'): arr4x4,
                ('C31', 'C41'): arr4x4,
                ('C31', 'C42'): arr4x4,

                ('C32', 'C33'): arr4x4,
                ('C32', 'C34'): arr4x4,
                ('C32', 'C42'): arr4x4,
                ('C32', 'C41'): arr4x4,

                ('C33', 'C34'): arr4x4,
                ('C33', 'C43'): arr4x4,
                ('C33', 'C44'): arr4x4,

                ('C34', 'C44'): arr4x4,
                ('C34', 'C43'): arr4x4,

                ('C41', 'C42'): arr4x4,
                ('C41', 'C43'): arr4x4,
                ('C41', 'C44'): arr4x4,

                ('C42', 'C43'): arr4x4,
                ('C42', 'C44'): arr4x4,

                ('C43', 'C44'): arr4x4
                }

#make a CSP: consists of a set of variables, a set of domains (one for each variable), and a set of constraints over the variables
var4x4 = ['C11', 'C12', 'C13', 'C14', 'C21', 'C22', 'C23', 'C24', 'C31', 'C32', 'C33', 'C34', 'C41', 'C42', 'C43', 'C44']
domain4x4 = {'C11': [1, 2, 3, 4], 'C12': [1, 2, 3, 4], 'C13': [1, 2, 3, 4], 'C14': [1, 2, 3, 4], 'C21': [1, 2, 3, 4], 
             'C22': [1, 2, 3, 4], 'C23': [1, 2, 3, 4], 'C24': [1, 2, 3, 4], 'C31': [1, 2, 3, 4], 'C32': [1, 2, 3, 4], 
             'C33': [1, 2, 3, 4], 'C34': [1, 2, 3, 4], 'C41': [1, 2, 3, 4], 'C42': [1, 2, 3, 4], 'C43': [1, 2, 3, 4], 
             'C44': [1, 2, 3, 4]}
testdomain4x4 = {'C11': [1], 'C12': [1,2,3,4], 'C13': [1,2,3,4], 'C14': [1,2,3,4], 
                 'C21': [1, 2, 3, 4],'C22': [2], 'C23': [1, 2, 3, 4], 'C24': [1, 2, 3, 4], 
                 'C31': [1, 2, 3, 4], 'C32': [1, 2, 3, 4], 'C33': [3], 'C34': [1, 2, 3, 4], 
                 'C41': [1, 2, 3, 4], 'C42': [1, 2, 3, 4], 'C43': [1, 2, 3, 4], 'C44': [4]}
CSP4x4 = [var4x4, domain4x4, constraint4x4]
