import os
import datetime as dt
from pathlib import Path

class calendar:
    def __init__(self,begining,end,pdf=False):
        self.beg = begining
        self.end = end
        self.events = []
        self.pdf=pdf

    def add_event(self, evt):
        self.events += [evt]


    def generate(self):
        #Read header and footer
        self.events.sort(key=lambda event: event.date)
        with open(Path(os.path.dirname(__file__),"template","latex_general","header.tex"), 'r') as f:
            header = f.read()
        with open(Path(os.path.dirname(__file__),"template","latex_general","footer.tex"), 'r') as f:
            footer = f.read()

        d = dt.timedelta(days=1)
        tex = header

        texday = tpl_day()

        cur = self.beg
        #row
        i=0
        #col
        j=0
        #event counter
        if len(self.events)==0:
            next_evt = event(dt.date(1,1,1))
        else:
            e=0
            next_evt = self.events[e]
        #event buffer for ranges
        buffer = []
        while cur <= self.end:
            tex += texday.generate(i,j,date=cur.isoformat())

            #Process event
            #Checking for mutliple deadlines on the same day
            dtxt = ""
            dead_today = False
            while next_evt.date == cur:
                if next_evt.type==1:
                    #In the next_evt title we put every deadline title for the day
                    if dtxt!="":
                        dtxt += "/"
                    dtxt += next_evt.title
                    next_evt.set_title(dtxt)
                    dead = next_evt
                    dead_today=True
                    print(dtxt)
                elif next_evt.range:
                    buffer += [next_evt]
                else:
                    print("oooo")
                    tex += next_evt.generate(i,j,mixte=evt_in_buf!=0)
                #Selecting the next event
                if len(self.events) > e+1:
                    e += 1
                    next_evt = self.events[e]
                else:
                    next_evt = event(dt.date(1,1,1))

            #Processing deadlines
            evt_in_buf = len(buffer)
            if dead_today:
                tex += dead.generate(i,j,mixte=evt_in_buf!=0)

            #Processing buffer of events
            poplst = []
            evt_in_buf = len(buffer)
            for bi,b in enumerate(buffer):
                tex += b.generate(i,j,p=bi,n=evt_in_buf)
                if b.end==cur:
                    poplst += [bi]
            for bi in poplst:
                buffer.pop(bi)

            #Select next position in the board
            j += 1
            if cur.month != (cur+d).month:
                i+=1
                j = 0
                if i>4:
                    tex += "\\end{tikzpicture}\n"
                    tex += "\\newpage\n\n"
                    tex += "\\begin{tikzpicture}\n"
                    i=0
            cur += d

        tex += footer


        #Write final string and generate pdf
        if not os.path.exists("output"):
            os.makedirs("output")
        with open(Path("output","main.tex"), 'w') as f:
            f.write(tex)

        if self.pdf:
            os.system("pdflatex --output-directory output output/main.tex")


#Events 
class event:
    def __init__(self, date, title=""):
        self.date = date
        self.title = title
        self.range=False
        self.type=0
    
    def __repr__(self):
        return repr(self.title)

class deadline(event):
    def __init__(self, date, title=""):
        super().__init__(date=date)
        self.title=title
        self.template = tpl_deadline(title)
        self.template_mixte = tpl_deadline_mixte(title)
        self.type=1

    def set_title(self,title):
        self.title = title
        self.template.title = title
        self.template_mixte.title = title

    def generate(self,i,j,mixte=False):
        if mixte:
            return self.template_mixte.generate(i,j)
        else:
            return self.template.generate(i,j)
    
class holiday(event):
    def __init__(self, bgn, end):
        super().__init__(date=bgn)
        self.bgn = bgn
        self.end = end
        self.template = tpl_holiday()
        self.range=True

    def generate(self,i,j,p=0,n=1):
        return self.template.generate(i,j,p=p,n=n)
    
class redaction(event):
    def __init__(self, bgn, end):
        super().__init__(date=bgn)
        self.bgn = bgn
        self.end = end
        self.template = tpl_redaction()
        self.range=True

    def generate(self,i,j,p=0,n=1):
        return self.template.generate(i,j,p=p,n=n)

class conf(event):
    def __init__(self, bgn, end, title=""):
        super().__init__(date=bgn)
        self.bgn = bgn
        self.end = end
        self.title=title
        self.template = tpl_conf(title=title)
        self.range=True

    def generate(self,i,j,p=0,n=1):
        return self.template.generate(i,j,p=p,n=n)

class formation(event):
    def __init__(self, bgn, end, title=""):
        super().__init__(date=bgn)
        self.bgn = bgn
        self.end = end
        self.title=title
        self.template = tpl_formation(title=title)
        self.range=True

    def generate(self,i,j,p=0,n=1):
        return self.template.generate(i,j,p=p,n=n)


#Templates
class template:
    def __init__(self, path):
        self.path = path
        with open(path, 'r') as f:
            self.tex = f.read()

    def generate(self):
        return self.tex

class tpl_day(template):
    def __init__(self):
        super().__init__(path=Path(os.path.dirname(__file__),"template","tikz","day.tex"))

    def generate(self,i,j,date):
        return self.tex.format(i=i,j=j,date=date)

class tpl_deadline(template):
    def __init__(self,title):
        super().__init__(path=Path(os.path.dirname(__file__),"template","tikz","deadline.tex"))
        self.title = title

    def generate(self,i,j):
        return self.tex.format(i=i,j=j,text=self.title)
    
class tpl_deadline_mixte(template):
    def __init__(self,title):
        super().__init__(path=Path(os.path.dirname(__file__),"template","tikz","deadline_mixte.tex"))
        self.title = title

    def generate(self,i,j):
        return self.tex.format(i=i,j=j,text=self.title)

class tpl_holiday(template):
    def __init__(self):
        super().__init__(path=Path(os.path.dirname(__file__),"template","tikz","holiday.tex"))

    def generate(self,i,j,p=0,n=1):
        return self.tex.format(i=i,j=j,p=p,n=n)
    
class tpl_redaction(template):
    def __init__(self):
        super().__init__(path=Path(os.path.dirname(__file__),"template","tikz","redaction.tex"))

    def generate(self,i,j,p=0,n=1):
        return self.tex.format(i=i,j=j,p=p,n=n)
    
class tpl_conf(template):
    def __init__(self,title):
        super().__init__(path=Path(os.path.dirname(__file__),"template","tikz","conf.tex"))
        self.title=title

    def generate(self,i,j,p=0,n=1):
        return self.tex.format(i=i,j=j,p=p,n=n,text=self.title)

class tpl_formation(template):
    def __init__(self,title):
        super().__init__(path=Path(os.path.dirname(__file__),"template","tikz","formation.tex"))
        self.title=title

    def generate(self,i,j,p=0,n=1):
        return self.tex.format(i=i,j=j,p=p,n=n,text=self.title)

