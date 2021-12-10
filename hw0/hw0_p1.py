question = input('input the polynomials: ')
#question = '(X+2*Y)(2*X^2-Y^2+Z)'
#question = '(A+2*B^2)(B+3C^3)(2*A+B+C)'
#question = '(2*X+3*Y+4*Z)(XY^2+X^2Y+Z^2)'
#print(f'question: {question}')

count = 0
for i in question:
    if i == '(':
        count += 1

question = question.split(')(')

if count == 2:
    first = question[0].replace('(', '')
    second = question[1].replace(')', '')
    all_group = [first, second]
if count == 3:
    first = question[0].replace('(', '')
    second = question[1]
    third = question[2].replace(')', '')
    all_group = [first, second, third]


def complete_split(count):
    all_in_one = []
    for i in range(count):
        all_in_one.append([])

    for i in range(len(all_group)):
        splited_plus = all_group[i].split('+')

        for j in splited_plus:
            if '-' in j:
                splited_minus = j.split('-')

                len_splites_minus = len(splited_minus)
                for m in range(1, len_splites_minus):
                    splited_minus[m-len_splites_minus] = '-' + \
                        splited_minus[m-len_splites_minus]

                for k in splited_minus:
                    all_in_one[i].append(k)
            else:
                all_in_one[i].append(j)
    return all_in_one


complete = complete_split(count)
print(complete, '\n')

finish = []
for i in range(len(complete)-1):
    for j in range(len(complete[i])):
        for k in range(len(complete[i+1])):
            finish.append(f'({complete[i][j]})({complete[i+1][k]})')

end_finish = ''
for i in finish:
    end_finish += f'+{i}'

print(end_finish)
