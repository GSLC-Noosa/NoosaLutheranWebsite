from glob import glob
from pathlib import Path
import os

# `cwd`: current directory is straightforward
script = Path(__file__).parent.resolve()
script = script.as_posix()

base_folder = str(script).rsplit('/', 1)[0]+"/"
content_folder = base_folder+"content/base_content/"

def fill_template(template_text, title, current, contents_text):
    header,footer = template_text.split('!!main!!')

    new_text = template_text.replace('!!title!!', title
        ).replace('!!main!!', contents_text)
    
    ## REPLACE FILENAMES
    bulletin_fnames = glob(base_folder+"content/bulletin/*")
    latest_bulletin_file = max(bulletin_fnames, key=os.path.getctime).replace(base_folder,"")

    theme_fnames = glob(base_folder+"content/theme/*")
    latest_theme_file = max(theme_fnames, key=os.path.getctime).replace(base_folder,"")

    new_text = new_text.replace('!!THEME!!',latest_theme_file).replace('!!BULLETIN!!',latest_bulletin_file)

    for tab in ["!!current_home!!","!!current_cong!!","!!current_worship!!","!!current_ministry!!","!!current_events!!","!!current_contact!!"]:
        if tab == current:
            new_text = new_text.replace(tab,' class="current"')
        else:
            new_text = new_text.replace(tab,"")

    if title == 'Weddings':
        slideshow_text = slideshow_filler(base_folder+"content/wedding_slideshow")
        new_text = new_text.replace("!!SLIDESHOW!!",slideshow_text)
    if title == 'Our Congregation':
        slideshow_text = slideshow_filler(base_folder+"content/congregation_slideshow")
        new_text = new_text.replace("!!SLIDESHOW!!",slideshow_text)

    return new_text

def make_template(name: str, current: str, title: str):
    with open(content_folder+'_template.html') as f_template:
        template_text = f_template.read()
        with open(content_folder+f'_{name}', encoding="utf8") as f_contents:
            with open(base_folder+f'{name}', 'w', encoding="utf8") as f_to:
                print(f"compiling {title}")
                f_to.write(fill_template(
                    template_text,
                    title,
                    current,
                    f_contents.read()))

def slideshow_filler(folder):

    txt = """<div>
              <h2 class="imgholder"><div class="slideshow-container">
          """

    files = glob(folder+"/*")
    total = len(files)
    for i,f in enumerate(files):

        f = f.replace(base_folder,"")

        elem = f"""<div class='mySlides fade'>
               <div class='numbertext'>{i+1} / {total}</div>
               <h2 class='imgholder', style='height:30vw'>
               <img src={f} style='max-height:100%'></h2>
               </div>"""
        txt+=elem

    txt+="""<!-- Next and previous buttons -->
                <a class="prev" onclick="plusSlides(-1)">&#10094;</a>
                <a class="next" onclick="plusSlides(1)">&#10095;</a>
              </div>
              <div style="text-align:center;margin-top:-2.2em">
               """

    for i in range(total):
        elem = f"<span class='dot' onclick='currentSlide({i+1})'></span>"
        txt+=elem

    txt+="</div>"

    return txt


names = ['childsafe.html',
         'congregation.html',
         'contact.html',
         'facilities.html',
         'faithink.html',
         'index.html',
         'lutheran.html',
         'ministry.html',
         'purpose.html',
         'events.html',
         'weddings.html',
         'worship.html'
        ]

currents = ["!!current_ministry!!",
"!!current_cong!!",
"!!current_contact!!",
"!!current_events!!",
"!!current_ministry!!",
"!!current_home!!",
"!!current_cong!!",
"!!current_ministry!!",
"!!current_cong!!",
"!!current_events!!",
"!!current_events!!",
"!!current_worship!!",
]
titles = ['Child Safe Standards',
         'Our Congregation',
         'Contact Us',
         'Facilities Hire',
         'Faith Inkubators',
         'Good Shepherd Lutheran Church - Noosa',
         "What's a Lutheran?",
         'Ministry Areas',
         'Our Purpose',
         "Events",
         "Weddings",
         'Worship'
        ]

for name, current, title in zip(names, currents, titles):
    make_template(name, current, title)
