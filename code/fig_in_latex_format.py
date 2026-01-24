def apply_figure_settings():
    import seaborn as sns

    sns.set(
        style="whitegrid",
        rc={
            "text.usetex": True,
            "font.family": "fourier",
            "axes.labelsize": 10,
            "font.size": 10,
            "legend.fontsize": 8,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
        },
    )
