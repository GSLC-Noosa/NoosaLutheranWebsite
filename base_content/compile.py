from glob import glob

def fill_template(template_text, title, current, contents_text):
    header,footer = template_text.split('!!main!!')

    new_text = template_text.replace('!!title!!', title
        ).replace('!!main!!', contents_text)
    
    ## REPLACE FILENAMES
    bulletin_fname = glob("../content/bulletin/*")[0].split("..")[1][1:]
    theme_fname = glob("../content/theme/*")[0].split("..")[1][1:]
    new_text = new_text.replace('!!THEME!!',theme_fname).replace('!!BULLETIN!!',bulletin_fname)

    for tab in ["!!current_home!!","!!current_cong!!","!!current_worship!!","!!current_ministry!!","!!current_events!!","!!current_contact!!"]:
        if tab == current:
            new_text = new_text.replace(tab,' class="current"')
        else:
            new_text = new_text.replace(tab,"")

    if title == 'Weddings':
        slideshow_text = slideshow_filler("../content/wedding_slideshow")
        new_text = new_text.replace("!!SLIDESHOW!!",slideshow_text)
    if title == 'Our Congregation':
        slideshow_text = slideshow_filler("../content/congregation_slideshow")
        new_text = new_text.replace("!!SLIDESHOW!!",slideshow_text)

    return new_text

def make_template(name: str, current: str, title: str):
    with open('_template.html') as f_template:
        template_text = f_template.read()
        with open(f'_{name}', encoding="utf8") as f_contents:
            with open(f'../{name}', 'w', encoding="utf8") as f_to:
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
        f_name = f.split("..")[1][1:]
        elem = f"""<div class='mySlides fade'>
               <div class='numbertext'>{i+1} / {total}</div>
               <h2 class='imgholder', style='height:30vw'>
               <img src={f_name} style='max-height:100%'></h2>
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
