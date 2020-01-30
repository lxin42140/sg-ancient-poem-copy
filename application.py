from flask import Flask, render_template
from Util import Util

application = Flask(__name__, template_folder='templates', static_folder='static')
IMG_PATH = '/static/images/'
PDF_PATH = '/static/pdf/'
title_prefix = '新加坡舊體詩庫-'
util = Util(IMG_PATH, PDF_PATH, title_prefix)


@application.route('/')
@application.route('/home')
def home():
    logo_path = IMG_PATH + 'logo.png'
    title = '新加坡舊體詩庫'
    sliders = [  # fake array of posts
        {
            'path': IMG_PATH + 'slider-3.jpg',
            'comments': ['Singapore Chinese Cultural Centre', '新加坡華族文化中心', '贊助'],
            'link': 'https://www.singaporeccc.org.sg/zh/'
        },
        {
            'path': IMG_PATH + 'slider-1.jpg',
            'comments': ['星洲四大才子', '李俊承, 邱菽園, 釋瑞于, 葉季允', ' ']
        },
        {
            'path': IMG_PATH + 'slider-2.jpg',
            'comments': ['烏敏島油畫', '何自力  作', '新加坡國立大學中文系講師']
        }
    ]
    return render_template('homepage.html',
       title = title,
       logo_path = logo_path,
       sliders = sliders)

@application.route('/about-us')
def about_us():
    return render_template('about-us.html')

@application.route('/shirenfangtan')
def shirenfangtan():
    return render_template('shirenfangtan.html')

@application.route('/shiji')
def shiji():
    return render_template('shiji.html')

@application.route('/shitanjinkuang')
def shitanjinkuang():
    return render_template('shitanjinkuang.html')

# @application.route('/yanjiulunwen')
# def paper():
#     return render_template('yanjiulunwen.html')

@application.route('/category/<name>', methods=['GET'])
def topic(name):
    para_dict = util.get_parameters_for_blog_from_db(name)
    isPaper = False

    if name == "yanjiulunwen":
        isPaper = True
        topic_dict = util.get_parameters_for_topic_from_db(name, "paper")
    else:
        topic_dict = util.get_parameters_for_topic_from_db(name, "poem")

    blog_dict = para_dict['blog_dict']

    return render_template('slider-poem-list.html',
       category=name,
       logo_path=para_dict['logo_path'],
       title=para_dict['title'],
       blog_title = blog_dict['blog_title'],
       blog_content = blog_dict['blog_content'],
       blog_img = blog_dict['blog_img'],
       blog_link = blog_dict['blog_link'],
       sliders=topic_dict['sliders'],
       main_content=topic_dict['main_content'],
       isPaper=isPaper
    )

@application.route('/<category>/<author_name>/<poem_name>', methods=['GET'])
def poem_content_page(category, poem_name, author_name):
    para_dict = util.get_parameters_for_poem_content_page(category, poem_name, author_name)
    full_poem = para_dict['main_content']['content']
    introduction = util.process_text(para_dict['main_content']['introduction'])
    poem_content_list = util.format_poem_content(full_poem)
    comment_list = util.format_poem_content(para_dict['main_content']['comments'])

    return render_template('poem-content.html',
       title = para_dict['title'],
       logo_path = para_dict['logo_path'],
       main_content = para_dict['main_content'],
       introduction = introduction,
       poem_content_list = poem_content_list,
       comment_list = comment_list,
    )

@application.route('/paper/<author_name>/<paper_title>', methods=['GET'])
def paper_content_page(paper_title, author_name):
    para_dict = util.get_parameters_for_paper_content_page(paper_title, author_name)

    return render_template('paper-content.html',
       title = para_dict['title'],
       logo_path = para_dict['logo_path'],
       paper_title = paper_title,
       author_name = author_name,
       pdf_location = para_dict['main_content']['link']
    )


@application.route('/favicon.ico', methods=['GET'])
def favicon():
    return ""

@application.route("/<any>", methods=['GET', 'POST'])
def any_to_404(any):
    return render_template('base_slider.html'), 404

# @application.errorhandler(404)
# def notfound():
#     """Serve 404 template."""
#     return make_response(render_template("404.html"), 404)


if __name__ == '__main__':
    application.run(host="0.0.0.0", port=5000, debug=False)