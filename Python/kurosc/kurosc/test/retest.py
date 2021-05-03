import re
ti = 2
tf = 7

plot_title = 'Oscillator Phase $\in$ [${0}$,${1}$)'.format(ti,tf)
plot_title +='at t = 99.999'
fldr = plot_title.replace('at t = ','').replace('\d\.\d*','')
test = re.sub('\d*\.\d*','',fldr)
print(test)
print(fldr)
