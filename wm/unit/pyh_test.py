from pyh import *

page = PyH('pyh_test')

page.addCSS('http://www.fanyoyo.cn/css/base.css')
page.addJS('http://www.fanyoyo.cn/js/core.js')

page << h1('pyh_h1', cl='test_h1')
page << div(cl='test_div', id='div_id') << p('div p date')
page << script(type='text/javascript', src='http://www.fanyoyo.cn/js/test.js')
page << script('function(){}', type='text/javascript')
page.printOut()
print page.render()



