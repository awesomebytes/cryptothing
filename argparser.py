import argparse
import os


class setBool(argparse.Action):
    """extends Action to enable parsing of `fuzzy` boolean user inputs"""
    def __call__(self, parser, namespace, values, option_string=None):
        fuzzy_true = ("yes", "true", "t", "1")
        boolean = (values.lower() in fuzzy_true)
        setattr(namespace, self.dest, boolean)


def parse_args():
    parser = argparse.ArgumentParser()
    DEFAULTS = {"k": 50,
                "rounds": 5,
                "outdir": "kmeansstuff",
                "scale": True,
                "generate_all": False,
                "data_saving": False}

    # positional args
    parser.add_argument("input", help = "path/to/input/file")

    # optional args
    parser.add_argument("-k", "--k", type = int, default = DEFAULTS["k"],
                        help = "number of centroids (default={})".\
                        format(DEFAULTS["k"]))
    parser.add_argument("-r", "--rounds", type = int, default = DEFAULTS["rounds"],
                        help = "number of rounds of clustering (default={})".\
                        format(DEFAULTS["rounds"]))
    parser.add_argument("-o", "--outdir", default = DEFAULTS["outdir"],
                        help = "path/to/output/directory (default={})".\
                        format(DEFAULTS["outdir"]))
    parser.add_argument("-s", "--scale", default = DEFAULTS["scale"],
                        help = "T/F: scale pixel location to be equitable with RGB vals? \
                        (default={})".format(DEFAULTS["scale"]), action = setBool)
    parser.add_argument("-g", "--generate_all", default = DEFAULTS["generate_all"],
                        help = "T/F: generate image after each round? (slower) \
                        (default={})".format(DEFAULTS["generate_all"]), action = setBool)
    parser.add_argument("-d", "--data_saving", default = DEFAULTS["data_saving"],
                        help = "T/F: save clustering data as .txt? \
                        (centroids, cluster sizes, dimensions) (default={})".\
                        format(DEFAULTS["data_saving"]), action = setBool)

    d_args = vars(parser.parse_args())
    positional_args = [arg.dest for arg in parser._get_positional_actions()]
    args = [d_args[k] for k in positional_args]
    kwargs = {k: v for k,v in d_args.iteritems() if k not in positional_args}

    return (args, kwargs)
