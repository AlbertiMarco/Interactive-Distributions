import pandas as pd
from bokeh.plotting import figure
from bokeh.io import output_file, show,output_notebook
from bokeh.io import curdoc
from bokeh.layouts import row,column
from bokeh.models import ColumnDataSource, CDSView, GroupFilter, Select , MultiChoice
from bokeh.palettes import Blues4
from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application
from bokeh.transform import factor_cmap
from bokeh.palettes import Set2

panel_dataset = pd.read_csv('https://www.dropbox.com/s/pwmuo4d4675rvww/data_interactive_distribution.csv?dl=1')

sex='F'
year=2016
years=[2011,2012,2013,2014,2015,2016]
genders=['M','F']
sstatus=['Low', 'Middle-Low','Upper-middle', 'Upper']
year_select = Select(value=str(year) , title='Year', options=[str(i) for i in years])
sex_select = Select(value=sex , title='Sex', options=genders)


def make_plot(sources, title):
    lines = {}
    plot = figure(plot_width=1000, x_axis_label='Age', y_axis_label='Health expenditure €')
    colors=['darkblue','cornflowerblue','forestgreen', 'yellowgreen']
    for status,color,source in zip(sstatus,colors,sources):
        lines[status]=plot.line(x='age',y='health_exp',source=source,line_width=2,line_color=color,legend_label=status)
        lines[status].visible = True if (status == 'Low' or status=='Upper') else False

    # fixed attributes
    plot.legend.location = "top_left"
    plot.legend.click_policy="hide"
    plot.toolbar.autohide = True
    plot.xaxis.axis_label ='Age'
    plot.yaxis.axis_label = "Health expenditure per head"
    plot.axis.axis_label_text_font_style = "bold"
    plot.title.text_font_size = '16pt'
    plot.title.text_font_style='bold'
    plot.title.align='center'
    plot.axis.axis_label_text_font_size='12pt'
    plot.title.text = title

    return plot

def update_plot(attrname, old, new):
    year=int(year_select.value)
    sex=sex_select.value
    title="Health expenditure per head by socio-economic status in "+str(year)+' for '+sex
    plot.title.text=title
    src1 = ColumnDataSource(data=panel_dataset[(panel_dataset.sex == sex) & (panel_dataset.year == year) & (panel_dataset['status']==sstatus[0])])
    src2 = ColumnDataSource(data=panel_dataset[(panel_dataset.sex == sex) & (panel_dataset.year == year) & (panel_dataset['status']==sstatus[1])])
    src3 = ColumnDataSource(data=panel_dataset[(panel_dataset.sex == sex) & (panel_dataset.year == year) & (panel_dataset['status']==sstatus[2])])
    src4 = ColumnDataSource(data=panel_dataset[(panel_dataset.sex == sex) & (panel_dataset.year == year) & (panel_dataset['status']==sstatus[3])])
    source1.data.update(src1.data)
    source2.data.update(src2.data)
    source3.data.update(src3.data)
    source4.data.update(src4.data)

source1 = ColumnDataSource(data=panel_dataset[(panel_dataset.sex == sex) & (panel_dataset.year == year) & (panel_dataset['status']==sstatus[0])] )
source2 = ColumnDataSource(data=panel_dataset[(panel_dataset.sex == sex) & (panel_dataset.year == year) & (panel_dataset['status']==sstatus[1])] )
source3 = ColumnDataSource(data=panel_dataset[(panel_dataset.sex == sex) & (panel_dataset.year == year) & (panel_dataset['status']==sstatus[2])] )
source4 = ColumnDataSource(data=panel_dataset[(panel_dataset.sex == sex) & (panel_dataset.year == year) & (panel_dataset['status']==sstatus[3])] )
sources=[source1,source2,source3,source4]
title = "Health expenditure per head by socio-economic status in "+str(year)+' for '+sex
plot = make_plot(sources,title)

year_select.on_change('value', update_plot)
sex_select.on_change('value',update_plot)

controls = column(year_select,sex_select)

layout=(row(plot,controls))
curdoc().add_root(layout)
