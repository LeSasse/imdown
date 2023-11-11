import seaborn as sns
import matplotlib.pyplot as plt

# analysis 1

tips = sns.load_dataset("tips")
g = sns.FacetGrid(tips, col="time")
g.savefig("figures/analysis1/fig1.png")


g = sns.FacetGrid(tips, col="time")
g.map(sns.histplot, "tip")
g.savefig("figures/analysis1/fig2.pdf")


g = sns.FacetGrid(tips, col="sex", hue="smoker")
g.map(sns.scatterplot, "total_bill", "tip", alpha=0.7)
g.add_legend()
g.savefig("figures/analysis1/fig3.png")


# analysis 2
g = sns.FacetGrid(tips, row="smoker", col="time", margin_titles=True)
g.map(
    sns.regplot, "size", "total_bill", color=".3", fit_reg=False, x_jitter=0.1
)
g.savefig("figures/analysis2/fig4.pdf")


g = sns.FacetGrid(tips, col="day", height=4, aspect=0.5)
g.map(sns.barplot, "sex", "total_bill", order=["Male", "Female"])
g.savefig("figures/analysis2/fig5.pdf")

ordered_days = tips.day.value_counts().index
g = sns.FacetGrid(
    tips,
    row="day",
    row_order=ordered_days,
    height=1.7,
    aspect=4,
)
g.map(sns.kdeplot, "total_bill")
g.savefig("figures/analysis2/fig5.png")


# analysis 3
ordered_days = tips.day.value_counts().index
g = sns.FacetGrid(
    tips,
    row="day",
    row_order=ordered_days,
    height=1.7,
    aspect=4,
)
g.map(sns.kdeplot, "total_bill")
g.savefig("figures/analysis3/fig6.png")


pal = dict(Lunch="seagreen", Dinner=".7")
g = sns.FacetGrid(tips, hue="time", palette=pal, height=5)
g.map(sns.scatterplot, "total_bill", "tip", s=100, alpha=0.5)
g.add_legend()
g.savefig("figures/analysis3/fig7.pdf")


attend = sns.load_dataset("attention").query("subject <= 12")
g = sns.FacetGrid(attend, col="subject", col_wrap=4, height=2, ylim=(0, 10))
g.map(sns.pointplot, "solutions", "score")
g.savefig("figures/analysis3/fig8.pdf")


with sns.axes_style("white"):
    g = sns.FacetGrid(
        tips, row="sex", col="smoker", margin_titles=True, height=2.5
    )
    g.map(sns.scatterplot, "total_bill", "tip", color="#334488")
    g.set_axis_labels("Total bill (US Dollars)", "Tip")
    g.set(xticks=[10, 30, 50], yticks=[2, 6, 10])
    g.figure.subplots_adjust(wspace=0.02, hspace=0.02)
    g.savefig("figures/analysis3/fig9.pdf")


g = sns.FacetGrid(tips, col="smoker", margin_titles=True, height=4)
g.map(
    plt.scatter,
    "total_bill",
    "tip",
    color="#338844",
    edgecolor="white",
    s=50,
    lw=1,
)
for ax in g.axes_dict.values():
    ax.axline((0, 0), slope=0.2, c=".2", ls="--", zorder=0)
g.set(xlim=(0, 60), ylim=(0, 14))
g.savefig("figures/analysis3/fig10.pdf")
