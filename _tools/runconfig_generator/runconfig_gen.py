import os

tests_file = '_tools/runconfig_generator/_test_list.txt'
template_file = '_tools/runconfig_generator/pytest_for_{}_{}.xml'


def get_configuration(module, fun):
    with open(template_file, 'r') as template:
        temp = template.readlines()
    print(template_file.format(module, fun))
    conf_lines = []
    for t in temp:
        if 'APPROLE_ROLE_ID' in t:
            conf_lines.append(
                t.format(os.environ['APPROLE_ROLE_ID']))
        elif 'APPROLE_SECRET_ID' in t:
            conf_lines.append(
                t.format(os.environ['APPROLE_SECRET_ID']))
        else:
            conf_lines.append(t.format(module, fun))
        print(t.format(module, fun).replace('\n', ''))
    with open(os.path.join('_tools/runconfig_generator/confs',
                           'pytest_for_{}_{}.xml'.format(module, fun)),
              'w') as new_conf:
        new_conf.writelines(conf_lines)


with open(tests_file, 'r') as list_tests:
    tests = list_tests.readlines()
    for test in tests:
        if test.startswith('<Module'):
            module = test.replace('<Module tests/', '').replace(
                '.py>',
                '').replace(
                '\n', '')
        if test.startswith('<Function'):
            fun = test.replace('<Function ', '').replace('>',
                                                         '').replace(
                '\n',
                '')
            # print(module, fun)
            get_configuration(module, fun)
