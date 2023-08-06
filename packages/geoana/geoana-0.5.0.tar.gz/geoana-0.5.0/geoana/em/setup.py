def configuration(parent_package="", top_path=None):
    from numpy.distutils.misc_util import Configuration

    config = Configuration("em", parent_package, top_path)

    config.add_subpackage("fdem")
    config.add_subpackage("tdem")
    config.add_subpackage("static")

    return config
