from pipedi import piped




if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1 or sys.argv[1] == '-':
        inp = "/dev/stdin"
    else:
        inp = sys.argv[1]

    with open(inp, 'r') as input_file:
        coll = list(input_file \
                    | strip('\n') \
                    | tail(10) \
                    | rev() \
                    | grep('x', invert=True) \
                    | cut(delimiter=';', fields=[1, 0, 3]) \
                    | sort(delimiter=';', fields=[2, 1]) \
                    | tac()
                )
        print(coll)
