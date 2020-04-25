def parse_text(data):
    lines = []
    i = 0
    while True:
        start = f'\n{i}\t'
        end = f'\n{i + 1}\t'
        start_index = data.find(start)
        end_index = data.find(end)
#         print (start_index, end_index)
#         print ("lines", data[start_index: end_index])
        if end_index == -1:
            extra = f'\n{i + 2}\t'
            extra_1 = f'\n{i + 3}\t'
            extra_2 = f'\n{i + 4}\t'

            # print(lines_b[start_index:])
            lines.append(data[start_index:])
            # print('What?')
            # print(lines_b)
            # print(extra, extra_1)
            # print(lines_b.find(extra))
            # print(lines_b.find(extra_1))
            # print(not (lines_b.find(extra) == -1 and lines_b.find(extra_1) == -1))

            if not (data.find(extra) == -1
                    and data.find(extra_1) == -1
                    and data.find(extra_2) == -1):
                print(data)
                print(extra, extra_1)
                print('Error')
            break

        lines.append(data[start_index:end_index])
        i += 1
    return lines


def lines_to_items(page_id, lines):
    lines_list = []

    for i, line in enumerate(lines):
        line_item = dict()

        line_item_list = line.split('\t')

        line_num = line_item_list[0]
        if not line_num.isdigit():
            print("None digit")
            print(page_id)

            print(lines)
            # print(k)
        else:
            line_num = int(line_num)

        if int(line_num) != i:
            print("Line num mismath")
            print(int(line_num), i)
            print(page_id)

            # print(k)

        line_item['line_num'] = line_num
        line_item['sentences'] = ''
        line_item['h_links'] = []

        if len(line_item_list) <= 1:
            lines_list.append(line_item)
            continue

        sent = line_item_list[1].strip()
        h_links = line_item_list[2:]

        if 'thumb' in h_links:
            h_links = []
        else:
            h_links = list(filter(lambda x: len(x) > 0, h_links))

        line_item['sentences'] = sent
        line_item['h_links'] = h_links
        # print(line_num, sent)
        # print(len(h_links))
        # print(sent)
        # assert sent[-1] == '.'

        if len(h_links) % 2 != 0:
            print(page_id)
            for w in lines:
                print(w)
            print("Term mod 2 != 0")

            print("List:", line_item_list)
            print(line_num, sent)
            print(h_links)
            print()

        lines_list.append(line_item)
    return lines_list
