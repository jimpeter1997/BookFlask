from flask import Flask, render_template, abort, request
from books import Book
from settings import BOOK_CATES, BOOK_LIST, TITLES
from flask_wtf import CSRFProtect
from forms import SearchForm
import re


app = Flask(__name__)
app.config["SECRET_KEY"] = "0451392aa##"  # 或者 app.secret_key = '123456'
scrf = CSRFProtect(app)

# 检查是否含有特殊字符
def is_string_validate(str):
    sub_str = re.sub(u'^[_a-zA-Z0-9\u4e00-\u9fa5]+$',"",str)
    if len(str) == len(sub_str):
        # 说明合法
        return False
    else:
        # 不合法
        return True

@app.errorhandler(404)
def handler_404_error(err):  # 必须接受一个参数，名称随意
    """自定义的处理错误的方法"""
    # 这个函数的返回值会是前端用户看到的结果
    return '出现了404错误， 错误信息：{}<br>欢迎回到<a href="http://www.mingyueshuba.com/">明月书吧</a>'.format(err)

# 首页
@app.route('/index', methods=['POST', 'GET'])
@app.route('/')
def index():
    if request.method == 'POST':
        print("我接到了post请求")
        form = SearchForm()
        if form.validate_on_submit():
            keyword=form.keyword.data
        else:
            abort(404)
        print("keyword = ", keyword)
        if is_string_validate(keyword):
            messages = "输入有误，请确认后重新输入"
            search_data = ""
            seo = {
                "title": "搜索结果页面",
                "keywords" : "首页关键词",
                "description" : "首页描述"
            }
            return render_template(
                "search.html",
                seo = seo,
                books_cates = BOOK_CATES,
                form = SearchForm(),
                messages = messages,
                search_data = search_data
            )
        book = Book()
        search_data = book.search_infos_by_key(keyword)
        if len(search_data) == 0:
            messages = ""
            search_data = ""
            seo = {
                "title": "搜索结果页面",
                "keywords" : "首页关键词",
                "description" : "首页描述"
            }
            return render_template(
                "search.html",
                seo = seo,
                books_cates = BOOK_CATES,
                form = SearchForm(),
                messages = messages,
                search_data = search_data
            )
        else:
            messages = ""
            seo = {
                "title": "搜索结果页面",
                "keywords" : "首页关键词",
                "description" : "首页描述"
            }
            return render_template(
                "search.html",
                seo = seo,
                books_cates = BOOK_CATES,
                form = SearchForm(),
                messages = messages,
                search_data = search_data
            )
    book = Book()
    xuanhuan_data = book.get_xuanhuan_top5()
    xiuzhen_data = book.get_xiuzhen_top5()
    dushi_data = book.get_dushi_top5()
    lishi_data = book.get_lishi_top5()
    wangyou_data = book.get_wangyou_top5()
    kehuan_data = book.get_kehuan_top5()
    yanqing_data = book.get_yanqing_top5()
    quanben_data = book.get_quanben_top5()
    print("用这个去区分每个不同的域名给他不同的关键词和描述 ------------------------>", request.path)
    seo = {
        "title": TITLES[request.path][0],
        "keywords" : TITLES[request.path][1],
        "description" : TITLES[request.path][2]
    }
    return render_template(
        "index.html",
        seo = seo,
        books_cates = BOOK_CATES,
        form = SearchForm(),
        xuanhuan_data = xuanhuan_data,
        xiuzhen_data = xiuzhen_data,
        dushi_data = dushi_data,
        lishi_data = lishi_data,
        wangyou_data = wangyou_data,
        kehuan_data = kehuan_data,
        yanqing_data = yanqing_data,
        quanben_data = quanben_data
    )


"""
request的说明：
    1 request.path: /test/a
    2 request.host: 127.0.0.1:5000
    3 request.host_url: http://127.0.0.1:5000/
    4 request.full_path: /test/a?x=1
    5 request.script_root:
    6 request.url: http://127.0.0.1:5000/test/a?x=1
    7 request.base_url: http://127.0.0.1:5000/test/a
    8 request.url_root: http://127.0.0.1:5000/
"""
# 小说分类页
@app.route('/<string:book_cate>',methods=['GET'])
def show_book_cates(book_cate):
    # 判断请求是否合法
    if book_cate in BOOK_LIST:
        print("请求合法")
        pass
    else:
        print("请求不合法")
        abort(404)
    print("用这个去区分每个不同的域名给他不同的关键词和描述 ", request.path)
    seo = {
        "title": TITLES[request.path][0],
        "keywords" : TITLES[request.path][1],
        "description" : TITLES[request.path][2]
    }
    book = Book()
    # 最新更新的30章内容
    sql_newest_data = book.get_cates_newst_books_30(book_cate)
    # 最多阅读的30张内容
    sql_most_data = book.get_cates_most_books_30(book_cate)
    return render_template(
        "book_cate.html",
        seo = seo,
        books_cates = BOOK_CATES,
        sql_newest_data = sql_newest_data,
        sql_most_data = sql_most_data,
        form = SearchForm()
    )

# 图书首页信息
@app.route('/book/<int:book_id>')
def show_book_index(book_id):
    book = Book()
    # 获取图书信息
    sql_book_infos = book.get_book_infos_by_book_id(book_id)
    if len(sql_book_infos) == 0:
        # 说明图书并不存在
        abort(404)
    cap_20_data = book.get_book_newest_20_caps_by_book_id(book_id)
    all_cap_data = book.get_book_all_caps_by_book_id(book_id)
    seo = {
        "title": sql_book_infos[0]['book_name']+'('+sql_book_infos[0]['book_author']+")最新章节_"+ sql_book_infos[0]['book_name']+TITLES['bookindex'][0], # 大道朝天(猫腻)最新章节_大道朝天在线阅读 _笔趣阁
        "keywords" : sql_book_infos[0]['book_name']+"最新章节列表,"+sql_book_infos[0]['book_name']+"无弹窗广告,"+sql_book_infos[0]['book_name']+"全文阅读,"+sql_book_infos[0]['book_author'],
        # 大道朝天最新章节列表,大道朝天无弹窗广告,大道朝天全文阅读,猫腻
        "description" : TITLES['bookindex'][2]+sql_book_infos[0]['book_author']+"大神最新作品《"+sql_book_infos[0]['book_name']+"》最新章节全文免费阅读，"+sql_book_infos[0]['book_name']+"全集，"+ \
            sql_book_infos[0]['book_name']+"5200，"+sql_book_infos[0]['book_name']+"无弹窗！请关注"+sql_book_infos[0]['book_name']+"吧，明月书吧最新最快更新"+sql_book_infos[0]['book_name']+"最新章节。"
        # 笔趣阁提供猫腻大神最新作品《大道朝天》最新章节全文免费阅读，大道朝天全集，大道朝天5200，大道朝天无弹窗！请关注大道朝天吧，本站最新最快更新大道朝天最新章节。
    }
    return render_template(
        "book_index.html",
        seo = seo,
        books_cates = BOOK_CATES,
        sql_book_infos = sql_book_infos,
        cap_20_data = cap_20_data,
        all_cap_data = all_cap_data,
        form = SearchForm()
    )

# 图书详情页
@app.route('/book/<int:book_id>/<int:sort_id>')
def show_book_detail(book_id,sort_id):
    book=Book()
    sql_book_id_data = book.get_book_infos_by_book_id(book_id)
    if len(sql_book_id_data) == 0:
        abort(404)
    print("图书信息：------",sql_book_id_data)
    book_name = sql_book_id_data[0]['book_name']
    sql_detail_data = book.get_book_detail_by_book_id_sort_id(book_id, sort_id)
    if len(sql_detail_data) == 0:
        abort(404)
    next_data = book.get_next_cap_id(book_id, sort_id)
    if next_data == None:
        next_sort_id = ''
    else:
        next_sort_id = next_data['sort_id']
    before_data = book.get_before_cap_id(book_id, sort_id)
    if before_data == None:
        before_sort_id = ''
    else:
        before_sort_id = before_data['sort_id']
    seo = {
        "title": sql_detail_data[0]['detail_title']+'_'+book_name+TITLES['bookdetail'][0],
        # 第二十七章来了_大道朝天 - 笔趣阁
        "keywords" : book_name+','+sql_book_id_data[0]['book_author']+','+sql_detail_data[0]['detail_title'],
        # 大道朝天,猫腻,第二十七章来了
        "description" : book_name+"无弹窗,是作者"+sql_book_id_data[0]['book_author']+"所著的好看的小说"+TITLES['bookdetail'][2]
        # 大道朝天无弹窗,是作者猫腻所著的玄幻小说类小说，本站提供无弹窗阅读环境
    }
    return render_template(
        "book_detail.html",
        seo = seo,
        books_cates = BOOK_CATES,
        sql_detail_data = sql_detail_data,
        next_sort_id = next_sort_id,
        before_sort_id = before_sort_id,
        book_name = book_name,
        form = SearchForm()
    )




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8989, debug=True)
