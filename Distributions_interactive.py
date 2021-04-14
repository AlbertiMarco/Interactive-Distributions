import pandas as pd
from bokeh.plotting import figure
from bokeh.io import output_file, show,output_notebook, push_notebook
from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, DataRange1d, Select, CheckboxButtonGroup
from bokeh.palettes import Blues4
from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application
from bokeh.transform import factor_cmap
from bokeh.palettes import Set2

#Read data from dropbox

panel_dataset = pd.read_csv('https://www.dropbox.com/s/jolb750wierrt0h/panel_dataset.csv?dl=1')


# In[5]:


str_status={1:'Low',2:'Middle-Low',3:'Upper-middle',4:'Upper'}
panel_dataset.status.replace(to_replace=str_status,inplace=True)


# In[6]:


panel_dataset.sex.replace(to_replace={'V':'F'},inplace=True)


# In[7]:


def get_dataset(src, sex, year):
    df1 = src[src.sex == sex][src.year == year]
    r=pd.DataFrame(data=df1.groupby(['age','status'])['health_expenditure_under_deductible'].sum()/df1.groupby(['age','status'])['number_citizens'].sum(),columns=['health_exp'])
    df=df1.merge(r,left_on=['age','status'], right_on=['age','status'],how='left')
    df.sort_values(['age'])
    df=pd.DataFrame(df.groupby(['age','sex','status','year'])['health_exp'].mean().reset_index())
    return ColumnDataSource(data=df)

def make_plot(source, title):
    plot = figure(plot_width=1000, x_axis_label='Age', y_axis_label='Health expenditure €')
    plot.title.text = title
    colors=['darkblue','cornflowerblue','forestgreen', 'yellowgreen']
    df=source.to_df()
    for status,color in zip(sstatus,colors):
        temp_source=ColumnDataSource(data=df[df['status']==status])
        plot.line(x='age',y='health_exp',source=temp_source,line_width=2,line_color=color,legend_label=status)

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

    return plot

sex='F'
year=2016
years=[2011,2012,2013,2014,2015,2016]
genders=['M','F']
sstatus=['Low', 'Middle-Low','Upper-middle', 'Upper']

year_select = Select(value='2011' , title='Year', options=[str(i) for i in years])
sex_select = Select(value='F' , title='Sex', options=genders)

def update_plot(attrname, old, new):
    year=int(year_select.value)
    sex=sex_select.value
    title=plot.title.text="Health expenditure per head by socio-economic status in "+str(year)+' for '+sex
    src=get_dataset(panel_dataset,sex,year)
    source.data.update(src.data)

source=get_dataset(panel_dataset,sex, year)
plot=make_plot(source,"Health expenditure per socio-economic status in "+str(year))

year_select.on_change('value', update_plot)
sex_select.on_change('value',update_plot)

controls = column(year_select,sex_select)

layout=(row(plot,controls))
curdoc().add_root(layout)

#Display plot inline in Jupyter notebook
output_notebook()

#Display plot
show(layout)
