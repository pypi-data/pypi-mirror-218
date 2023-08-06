"""
操作主类
"""
from .layout import LayOut
from .chart import Chart
from IPython.display import display, HTML
import tempfile
import os

# 获取当前脚本文件的绝对路径
script_path = os.path.abspath(__file__)

# 获取当前脚本文件所在的目录
script_directory = os.path.dirname(script_path)

# 获取父级目录
parent_directory = os.path.dirname(script_directory)


class Stack:
    """
    实现 stackviz 的主类
    """
    def __init__(self, rows_span=None, cols_span=None, css=''):
        """
        构造函数

        Parameters:
        -----------
        css : str
            css信息：若传文件路径 ，则读取对应文件的内容；否则直接将该信息作为内容
        """
        if os.path.exists(css):
            with open(css, 'r', encoding='utf-8') as css_file:
                self.css = css_file.read()
        else:
            self.css = css
        with open(os.path.join(parent_directory, 'resources/echarts.min.js'), "r", encoding="UTF-8") as echarts_file:
            self.echarts_js = echarts_file.read()
        with open(os.path.join(parent_directory, 'resources/template.tpl'), "r", encoding="UTF-8") as tpl_file:
            self.html = tpl_file.read()
        self.html = self.html.replace("${style}", css)
        self.rows_span = rows_span
        self.cols_span = cols_span
        self.layout = LayOut(rows_span, cols_span)
        self.layout_settings = []
        self.scripts = []
        
    def add_layout(self, row, col, layout_object: LayOut):
        self.layout_settings.append((row, col, layout_object.html))
        
    def add_chart(self, row, col, chart_object: Chart):
        w = str(self.rows_span[col - 1])
        h = str(self.cols_span[row - 1])
        self.layout_settings.append((row, col, chart_object.get_div().replace('[w]',w).replace('[h]',h)))
        self.scripts.append(chart_object.get_script())
        if '${echarts}' in self.html:
            self.html = self.html.replace('${echarts}', self.echarts_js)
        
    def add_text(self, row, col, text):
        self.layout_settings.append((row, col, text))

    def __display_html(self, content):
        current_dir = os.getcwd()
        target_file = os.path.join(current_dir, 'stackviz.html')
        if os.path.exists(target_file):
            os.remove(target_file)
        with open(target_file, 'w', encoding='utf-8') as temp_file:
            temp_file.write(content)
        # TODO: 当前仅支持从工作目录根目录访问 ，不支持从子级目录访问 
        return """
            <style>
                /* 设置容器 div 的宽度和高度 */
                .iframe-container {
                width: 100%;
                height: 0;
                padding-bottom: 56.25%; /* 设置宽高比为 16:9，如果需要其他比例，可以调整此值 */
                position: relative;
                }

                /* 设置 iframe 的样式 */
                .iframe-container iframe {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                }
            </style>
            <div class="iframe-container">
                <iframe src="[link]" frameborder="0" allowfullscreen></iframe>
            </div>
        """.replace('[link]', '/files/stackviz.html')

    def show_chart(self, chart_object: Chart, w, h):
        if '${echarts}' in self.html:
            self.html = self.html.replace('${echarts}', self.echarts_js)
        display(HTML(self.__display_html(
            self.html.replace("${body}",chart_object.get_div().replace('[w]',str(w)).replace('[h]',str(h))).\
                      replace("${script}", chart_object.get_script())
        )))
        
    def show(self):
        self.layout.load(self.layout_settings)
        display(HTML(self.__display_html(
            self.html.replace("${body}", self.layout.html).\
                      replace("${script}","\n\n".join(self.scripts))
        )))
