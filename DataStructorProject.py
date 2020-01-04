
import time                             # algoritmanın çalışma süresini bilmek için dahil ettim.
import docx                             # Word belgesini okumak için docx modülünü dahil ettim.
import PyPDF2                           # pdf     ""       ""    ""  PyPDF2 ""      ""     ""      
from re import findall                  # sadece kelimeri almak için re modülünden findall metodunu kullandım.

class Stack:                       
                    
    def __init__(self):
        self.items = []
        self.similar_matches = []               # Benzer eşleşmelerin tutulduğu liste
        self.same_matches = []                  # Tam eşleşmelerin tutulduğu liste
    def push(self,item):                        # Stack içerisine eleman ekleyen metod
        self.items.append(item)
    def pop(self):                              # Stack içerisinden eleman silen metod
        return self.items.pop()
    def getStack(self):                         # Staği döndüren metod
        return self.items
    def Lenght(self):                           # Stack boyutunu döndüren metod
        return len(self.items)

    def PreLoading_file(self,file:str):     # Önyükleme metodu txt dosyasındaki kelimeleri liste içerisine ekler.
        
        if "txt" in file.split("."):        # Eğer dosya txt dosyası ise
            with open(file,"r",encoding="utf-8") as f: 
                copy = f.read()
                copy = findall(r"[\w']+",copy)                
                for text in copy:
                    self.push(text.lower())

        if "docx" in file.split("."):               # eğer dosya docx dosyası ise
            doc = docx.Document(file)
            fulltext = []
            for i in doc.paragraphs:
                fulltext.append(i.text)
                data = "\n".join(fulltext)
            for i in findall(r"[\w']+",data):
                self.push(i.lower())

        if "pdf" in file.split("."):                # eğer dosya pdf dosyası ise
            pdf_file = open(file,"rb")              
            pdfReader = PyPDF2.PdfFileReader(pdf_file)
            
            for i in range(pdfReader.numPages):
                page = pdfReader.getPage(i)
                page = page.extractText()
                for j in findall(r"[\w']+",page):
                     self.push(j.lower())

        if "html" in file.split("."):
            with open(file,"r",encoding="utf-8") as f:
                copy = f.read()
                copy = findall(r"[\w']+",copy)
                for text in copy:
                    self.push(text.lower())

    def BCL(self,word:list,lenght_:int):                 # BCL metodu kötü karakter tablosunu liste halinde döndürür.
        no_of_chars = 256
        badChar = [-1]*no_of_chars

        for i in range(lenght_):
            badChar[ord(word[i])] = i     
        return badChar

    def search(self,txt:str,pat:str):       # method içerisinde boyer moore arama algoritması çalışır
        m = len(pat)                # aranacak olan kelime 
        n = len(txt)                # Metnin içerisinde aradığımız kelime
        
        badChar = self.BCL(pat,m)   # Aranacak olan kelimenin kötü karakter tablosunu oluşturuyoruz.
        s = 0                       

        while(s <= n-m ):
            j = m-1
            while j>=0 and pat[j] == txt[s+j]:
                j -= 1
            if j<0:                     
                if m == n:   # Eğer aranan boyut(kelime) = boyut(aranacak kelime)
                    self.same_matches += [txt]
                    #print("tam eşleşme sağlandı: {}".format(txt))  
                    break
                else:
                    self.similar_matches += [txt]                  
                    #print("Yaklaşan eşleşme sağlandı: {}".format(txt))
                    break
            else:
                s += max(1,j-badChar[ord(txt[s+j])])
        return self.same_matches,self.similar_matches

    def search_analysis_txt(self,pat:str): 
        start_time = time.time()
        for i in self.getStack():
            self.search(i,pat)
        end_time = time.time()
        with open("search_analysis_txt","a",encoding="utf-8") as f:
            f.write("\n\t\tTXT FILE \t\t\t\tNumber of words--> {}\n\t\t\tSIMILAR MATCHES\t\t Pattern ->> '{}'  Run Time ->> {} seconds\n"
            .format(self.Lenght(),pat,end_time-start_time))

            if len(self.similar_matches) == 0:
                f.write("\t\tNo similar matches\n")

            if len(self.similar_matches) != 0:
                for i in set(self.similar_matches):
                    counter = 0
                    for x in self.similar_matches:
                        if x == i:
                            counter += 1                    
                    f.write("\t\t{} matches found in {}\n".format(counter,i))

            if len(self.same_matches) == 0:
                f.write("\tNo same matches\n")
                
            if len(self.same_matches) != 0:
                f.write("\t\t\tSAME MATCHES\n")         
                f.write("\t\t{} matches found in {}\n".format(len(self.same_matches),self.same_matches[0]))

    def search_analysis_docx(self,pat:str):
        start_time = time.time()
        for i in self.getStack():
            self.search(i,pat)
        end_time = time.time()
        

        with open("search_analysis_txt","a",encoding="utf-8") as f:
            f.write("\n\t\tDOCX FILE \t\t\t\tNumber of words->> {} \n\t\t\tSIMILAR MATCHES\t\t Pattern->> '{}'  Run Time->> {} seconds\n"
            .format(self.Lenght(),pat,end_time-start_time))

            if len(self.similar_matches) == 0:
                f.write("\tNo similar matches\n")

            if len(self.similar_matches) != 0:
                for i in set(self.similar_matches):
                    counter = 0
                    for x in self.similar_matches:
                        if x == i:
                            counter += 1                    
                    f.write("\t\t{} matches found in {}\n".format(counter,i))

            if len(self.same_matches) == 0:
                f.write("\t\t\tSAME MATCHES\n")
                f.write("\t\tNo same matches\n")
                
            if len(self.same_matches) != 0:
                f.write("\t\t\tSAME MATCHES\n")         
                f.write("\t\t{} matches found in {}\n".format(len(self.same_matches),self.same_matches[0]))

    def search_analysis_pdf(self,pat:str):
        start_time = time.time()
        for i in self.getStack():
            self.search(i,pat)
        end_time = time.time()
        

        with open("search_analysis_txt","a",encoding="utf-8") as f:
            f.write("\n\t\tPDF FILE \t\t\t\tNumber of words->> {} \n\t\t\tSIMILAR MATCHES\t\t Pattern->> '{}'  Run Time->> {} seconds\n"
            .format(self.Lenght(),pat,end_time-start_time))

            if len(self.similar_matches) == 0:
                f.write("\tNo similar matches\n")

            if len(self.similar_matches) != 0:
                for i in set(self.similar_matches):
                    counter = 0
                    for x in self.similar_matches:
                        if x == i:
                            counter += 1                    
                    f.write("\t\t{} matches found in {}\n".format(counter,i))

            if len(self.same_matches) == 0:
                f.write("\t\t\tSAME MATCHES\n")
                f.write("\t\tNo same matches\n")
                
            if len(self.same_matches) != 0:
                f.write("\t\t\tSAME MATCHES\n")         
                f.write("\t\t{} matches found in {}\n".format(len(self.same_matches),self.same_matches[0]))

    def search_analysis_html(self,pat:str): 
        start_time = time.time()
        for i in self.getStack():
            self.search(i,pat)
        end_time = time.time()
        
        with open("search_analysis_txt","a",encoding="utf-8") as f:
            f.write("\n\t\tHTML FILE \t\t\t\tNumber of words--> {}\n\t\t\tSIMILAR MATCHES\t\t Pattern ->> '{}'  Run Time ->> {} seconds\n"
            .format(self.Lenght(),pat,end_time-start_time))

            if len(self.similar_matches) == 0:
                f.write("\t\tNo similar matches\n")

            if len(self.similar_matches) != 0:
                for i in set(self.similar_matches):
                    counter = 0
                    for x in self.similar_matches:
                        if x == i:
                            counter += 1                    
                    f.write("\t\t{} matches found in {}\n".format(counter,i))

            if len(self.same_matches) == 0:
                f.write("\tNo same matches\n")
                
            if len(self.same_matches) != 0:
                f.write("\t\t\tSAME MATCHES\n")         
                f.write("\t\t{} matches found in {}\n".format(len(self.same_matches),self.same_matches[0]))

if __name__ == "__main__":

    # .Txt File 
    Stack_txt = Stack()
    Stack_txt.PreLoading_file("example.txt") 
    Stack_txt.search_analysis_txt("rain".lower())

    # .Docx File
    Stack_docx = Stack()
    Stack_docx.PreLoading_file("example.docx")
    Stack_docx.search_analysis_docx("rain".lower())  

    # .Html file
    Stack_html = Stack()
    Stack_html.PreLoading_file("example.html")
    Stack_html.search_analysis_html("rain".lower())

    # .Pdf File
    Stack_pdf = Stack()
    Stack_pdf.PreLoading_file("example.pdf")
    Stack_pdf.search_analysis_pdf("rain".lower())
    
    
    
    
    
    
    
