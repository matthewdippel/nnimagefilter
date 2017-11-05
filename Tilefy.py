import ImageKNN
import logging
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)#, filename="debug.log")
    import sys
    t_f = sys.argv[1]
    i_f = sys.argv[2]
    o_f = sys.argv[3]

    ImageKNN.retile(t_f, i_f, o_f)
