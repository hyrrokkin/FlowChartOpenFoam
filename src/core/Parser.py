def check_text(text):
    if text is None:
        raise ValueError('')

    if not isinstance(text, str):
        raise TypeError('')


def parse_text(text, **kwargs):
    check_text(text)

    new_text = text

    for parameter in kwargs:
        new_text = new_text.replace('$' + str(parameter), str(kwargs[parameter]))

    return new_text


def parse_file(template_path, file_path, **kwargs):
    f = open(template_path, 'r')
    text = parse_text(f.read(), **kwargs)
    f.close()

    f = open(file_path, 'w')
    f.write(text)
    f.close()

    print text

#print parse_file('../template/controlDictTemplate', 's.txt', application=5)
